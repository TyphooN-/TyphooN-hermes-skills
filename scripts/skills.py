#!/usr/bin/env python3
"""Offline verification and deliberate installation of the checked-in skills.

No network, provider calls, configuration edits, dependency installation or
execution of skill payloads. Run without --apply to inspect the installation.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = {'references', 'scripts', 'templates', 'assets'}
SLUG = re.compile(r'[a-z0-9][a-z0-9_-]{0,63}\Z')


class CollectionError(ValueError):
    pass


def safe_relative(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise CollectionError(f'Unsafe relative path: {value!r}')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or p.as_posix() != value or ':' in value:
        raise CollectionError(f'Unsafe relative path: {value!r}')
    return p


def no_symlinks(path):
    for p in (path, *path.parents):
        if p.is_symlink():
            raise CollectionError(f'Refusing symlink path: {p}')
        if p != path and p.exists() and not p.is_dir():
            raise CollectionError(f'Path parent is not a directory: {p}')


def file_map(directory):
    no_symlinks(directory)
    result = {}
    for cur, dirs, files in os.walk(directory, followlinks=False):
        for name in dirs + files:
            p = Path(cur) / name
            if p.is_symlink():
                raise CollectionError(f'Refusing payload symlink: {p}')
        for name in files:
            p = Path(cur) / name
            if not p.is_file():
                raise CollectionError(f'Refusing nonregular payload: {p}')
            data = p.read_bytes()
            result[p.relative_to(directory).as_posix()] = {
                'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                'executable': bool(p.stat().st_mode & 0o111),
            }
    return dict(sorted(result.items()))


def entry_name(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise CollectionError(f'Malformed frontmatter: {path}')
    header, body = text[4:].split('\n---\n', 1)
    if not body.strip():
        raise CollectionError(f'Empty skill body: {path}')
    match = re.search(r'^name:\s*([\w-]+)\s*$', header, re.M)
    if not match or not SLUG.fullmatch(match[1]):
        raise CollectionError(f'Invalid skill name: {path}')
    for field in ['description', 'version', 'author', 'license', 'platforms']:
        if not re.search(r'^' + field + r':\s*\S', header, re.M):
            # YAML block lists have their values on the following lines.
            if field != 'platforms' or not re.search(r'^platforms:\s*\n- ', header, re.M):
                raise CollectionError(f'Missing frontmatter {field}: {path}')
    if len(text) > 100_000:
        raise CollectionError(f'Skill exceeds Hermes content limit: {path}')
    return match[1], header


def check_links(directory, relative, text):
    """Check actual support-file links, not paths in illustrative shell code."""
    for target in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', text):
        target = target.split('#', 1)[0]
        if not target or '://' in target or target.startswith(('mailto:', '#')):
            continue
        if not target.startswith(('references/', 'scripts/', 'templates/', 'assets/')) and not relative.startswith('references/'):
            continue
        if '\\' in target or PurePosixPath(target).is_absolute():
            raise CollectionError(f'Unsafe linked asset: {relative} -> {target}')
        candidate = directory / Path(relative).parent / target
        if not candidate.resolve().is_relative_to(directory.resolve()):
            raise CollectionError(f'Escaping linked asset: {relative} -> {target}')
        if not candidate.is_file():
            raise CollectionError(f'Missing linked asset: {relative} -> {target}')
    # A literal skill_view file_path is part of this skill's package contract.
    for target in re.findall(r'file_path\s*=\s*[\'"]((?:references|scripts|templates|assets)/[^\'"<>]+)[\'"]', text):
        if '*' in target or '$' in target:
            continue
        safe_relative(target)
        if not (directory / target).is_file():
            raise CollectionError(f'Missing skill_view asset: {relative} -> {target}')


def load_collection(root=ROOT, deep_yaml=False):
    root = Path(root).resolve()
    manifest = json.loads((root / 'skills-manifest.json').read_text())
    if manifest.get('schema_version') != 1 or not isinstance(manifest.get('skills'), list):
        raise CollectionError('Unsupported manifest schema')
    rows = manifest['skills']
    if hashlib.sha256((root / 'CATALOG.md').read_bytes()).hexdigest() != manifest.get('catalog_sha256'):
        raise CollectionError('Generated catalog integrity mismatch')
    names = [r['name'] for r in rows]
    if len(names) != len(set(names)):
        raise CollectionError('Duplicate skill identity in manifest')
    observed = []
    for cur, dirs, files in os.walk(root / 'skills', followlinks=False):
        for name in dirs + files:
            if (Path(cur) / name).is_symlink():
                raise CollectionError('Symlink in collection')
        if 'SKILL.md' in files:
            observed.append(Path(cur).relative_to(root).as_posix())
            dirs[:] = []  # Supporting upstream SKILL.md files are not entry points.
    if set(observed) != {r['path'] for r in rows} or len(observed) != len(rows):
        raise CollectionError('Manifest and discovered skill roots differ')
    for row in rows:
        if not SLUG.fullmatch(row['name']):
            raise CollectionError('Unsafe skill identity')
        rel = safe_relative(row['path'])
        if not rel.parts or rel.parts[0] != 'skills' or len(rel.parts) != 3 or rel.name != row['name']:
            raise CollectionError(f'Invalid skill location: {rel}')
        directory = root / rel
        current = file_map(directory)
        if current != row.get('files'):
            raise CollectionError(f'Payload integrity mismatch: {row["name"]}')
        name, header = entry_name(directory / 'SKILL.md')
        if name != row['name']:
            raise CollectionError('Frontmatter identity mismatch')
        if not row['description'].endswith('.') or len(row['description']) > 60:
            raise CollectionError('Description must be <=60 characters and end with a period')
        for relative in current:
            text = (directory / relative).read_text(encoding='utf-8')
            if re.search(r'/home/(?:typhoon|typhon)/', text, re.I):
                raise CollectionError(f'Machine-specific home in {row["name"]}/{relative}')
            if re.search(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY', text):
                raise CollectionError(f'Private key marker in {relative}')
            if relative.endswith('.md'):
                check_links(directory, relative, text)
        if deep_yaml:
            try:
                import yaml
            except ImportError as exc:
                raise CollectionError('Full YAML checking needs requirements-dev.txt') from exc
            try:
                fields = yaml.safe_load(header)
            except yaml.YAMLError as exc:
                raise CollectionError(f'Invalid YAML: {name}') from exc
            for key in ['name', 'description', 'author', 'license', 'platforms']:
                if fields.get(key) != row[key]:
                    raise CollectionError(f'YAML/catalog mismatch for {name}:{key}')
            if not isinstance(fields['platforms'], list) or not fields['platforms']:
                raise CollectionError('Invalid platform list')
    expected_files = {r['path'] + '/' + name for r in rows for name in r['files']}
    observed_files = {p.relative_to(root).as_posix() for p in (root / 'skills').rglob('*') if p.is_file()}
    if observed_files != expected_files:
        raise CollectionError('Unmanifested or missing file in skills tree')
    coverage = json.loads((root / 'coverage.json').read_text())
    source = coverage['skills']
    if len({s['name'] for s in source}) != len(source):
        raise CollectionError('Duplicate coverage identity')
    if set(names) != {s['name'] for s in source if s['included']}:
        raise CollectionError('Coverage and collection differ')
    if dict(Counter(s['classification'] for s in source)) != coverage['counts']:
        raise CollectionError('Coverage class totals differ')
    if len(rows) != coverage['included_count'] or len(source) != coverage['profile_skill_count']:
        raise CollectionError('Coverage totals differ')
    for row in rows:
        for dependency in row.get('external_related_skills', []):
            if dependency in names:
                raise CollectionError('External dependency is included locally')
    return rows


def existing_skills(skills_root, wanted):
    result = {name: [] for name in wanted}
    for cur, dirs, files in os.walk(skills_root, followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'__pycache__', 'node_modules', 'venv'}]
        for name in dirs:
            p = Path(cur) / name
            if p.is_symlink() and name in wanted:
                raise CollectionError(f'Selected installed skill is a symlink: {p}')
        if 'SKILL.md' not in files:
            continue
        p = Path(cur)
        no_symlinks(p / 'SKILL.md')
        header = (p / 'SKILL.md').read_text(encoding='utf-8').split('---', 2)
        m = re.search(r'^name:\s*[\'"]?([\w-]+)[\'"]?\s*$', header[1], re.M) if len(header) > 2 else None
        name = m[1] if m else p.name
        if name in result:
            result[name].append(p)
        dirs[:] = []
    for name, matches in result.items():
        if len(matches) > 1:
            raise CollectionError(f'Ambiguous installed identity {name}: {matches}')
    return result


def install(root, rows, home, apply=False, backup_existing=False):
    root = Path(root).resolve()
    home = Path(home).expanduser().absolute()
    no_symlinks(home)
    skills_root = home / 'skills'
    no_symlinks(skills_root)
    if skills_root.exists() and not skills_root.is_dir():
        raise CollectionError('Destination skills root is not a directory')
    existing = existing_skills(skills_root, {r['name'] for r in rows})
    plans = []
    for row in rows:
        rel = safe_relative(row['path'])
        target = home / rel
        no_symlinks(target)
        old = existing[row['name']]
        if target.exists() and (not old or old[0] != target):
            raise CollectionError(f'Destination exists without matching skill identity: {target}')
        if target.resolve().is_relative_to(root) or root.is_relative_to(target.resolve()):
            raise CollectionError('Installation destination overlaps source collection')
        plans.append((row, target, old[0] if old else None))
    conflicts = [r['name'] for r, _, old in plans if old is not None]
    report = {'mode': 'apply' if apply else 'plan', 'home': str(home),
              'skills': [r['name'] for r in rows], 'conflicts': conflicts,
              'backup_existing': backup_existing, 'installed': [], 'backups': {}}
    if not apply:
        return report
    if conflicts and not backup_existing:
        raise CollectionError('No files written; existing skill identities: ' + ', '.join(conflicts) + '. Use --backup-existing only after reviewing the plan.')
    home.mkdir(parents=True, exist_ok=True)
    receipt_parent = home / 'skill-install-receipts'
    no_symlinks(receipt_parent)
    receipt_parent.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='install-', dir=receipt_parent))
    report['receipt'] = str(work / 'receipt.json')

    def receipt():
        (work / 'receipt.json').write_text(json.dumps(report, indent=2) + '\n')

    receipt()
    try:
        notices = work / 'notices'
        notices.mkdir()
        for name in ['LICENSE', 'THIRD_PARTY.md', 'PORTABILITY.md', 'README.md', 'coverage.json']:
            no_symlinks(root / name)
            shutil.copyfile(root / name, notices / name)
        file_map(root / 'licenses')
        shutil.copytree(root / 'licenses', notices / 'licenses')
        # Finish source copies and integrity proof before moving any originals.
        for row, _, _ in plans:
            stage = work / 'staged' / row['name']
            shutil.copytree(root / row['path'], stage)
            if file_map(stage) != row['files']:
                raise CollectionError('Staged copy integrity failure: ' + row['name'])
        for row, target, old in plans:
            target.parent.mkdir(parents=True, exist_ok=True)
            if old:
                backup = work / 'originals' / old.relative_to(skills_root)
                backup.parent.mkdir(parents=True, exist_ok=True)
                old.rename(backup)
                report['backups'][row['name']] = str(backup)
                receipt()
            (work / 'staged' / row['name']).rename(target)
            report['installed'].append(row['name'])
            receipt()
        report['status'] = 'installed'
    except (OSError, CollectionError) as exc:
        report.update(status='partial_failure', error=str(exc))
        receipt()
        raise CollectionError(f'Installation interrupted; preserve originals and read {report["receipt"]}: {exc}') from exc
    receipt()
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='Collection checkout (defaults to this script\'s repository)')
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('verify', help='Verify every package, catalog, coverage and linked support file offline')
    check.add_argument('--yaml', action='store_true', help='Also parse complete frontmatter with PyYAML (development dependency)')
    commands.add_parser('list', help='List every included skill')
    put = commands.add_parser('install', help='Preview or apply a deliberate copy into an explicit Hermes home')
    put.add_argument('--home', required=True, type=Path, help='Exact destination HERMES_HOME; never selected implicitly')
    put.add_argument('--skill', action='append', default=[], help='Install only this name; repeat to select several (default all)')
    put.add_argument('--apply', action='store_true', help='Actually write files (default is a read-only plan)')
    put.add_argument('--backup-existing', action='store_true', help='Preserve existing selected skill directories outside skills before replacement')
    args = parser.parse_args(argv)
    try:
        rows = load_collection(args.root, deep_yaml=getattr(args, 'yaml', False))
        if args.command == 'verify':
            result = {'status': 'verified', 'skills': len(rows), 'payload_files': sum(len(r['files']) for r in rows), 'full_yaml': args.yaml}
        elif args.command == 'list':
            result = [{'name': r['name'], 'classification': r['classification'], 'platforms': r['platforms']} for r in rows]
        else:
            if args.skill:
                unknown = set(args.skill) - {r['name'] for r in rows}
                if unknown:
                    raise CollectionError('Unknown skills: ' + ', '.join(sorted(unknown)))
                rows = [r for r in rows if r['name'] in args.skill]
            result = install(args.root, rows, args.home, args.apply, args.backup_existing)
        print(json.dumps(result, indent=2))
        return 0
    except (CollectionError, OSError, KeyError, json.JSONDecodeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
