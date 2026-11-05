"""Offline proof for every package and deliberate destination changes."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import skills as s


class CollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = s.load_collection(ROOT, deep_yaml=True)
        cls.by_name = {r['name']: r for r in cls.rows}

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hermes-skill-test-')
        self.addCleanup(self.temp.cleanup)
        self.scratch = Path(self.temp.name).resolve()
        self.home = self.scratch / 'profile'

    def subset(self, name='git-remote-ref-recovery'):
        return [self.by_name[name]]

    def clone(self):
        target = self.scratch / 'collection'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
        return target

    def rewrite_manifest(self, clone, data):
        (clone / 'skills-manifest.json').write_text(json.dumps(data))

    def test_all_skills_and_payloads(self):
        self.assertEqual(len(self.rows), 27)
        self.assertEqual(sum(len(r['files']) for r in self.rows), 98)
        self.assertEqual(Counter(r['classification'] for r in self.rows), {'local-custom': 17, 'modified-bundled': 10})
        for row in self.rows:
            with self.subTest(skill=row['name']):
                self.assertEqual(s.file_map(ROOT / row['path']), row['files'])
                self.assertTrue((ROOT / row['path'] / 'SKILL.md').is_file())

    def test_plan_is_read_only_even_for_missing_home(self):
        result = s.install(ROOT, self.rows, self.home)
        self.assertEqual(result['mode'], 'plan')
        self.assertEqual(result['installed'], [])
        self.assertFalse(self.home.exists())

    def test_full_install_roundtrip(self):
        result = s.install(ROOT, self.rows, self.home, apply=True)
        self.assertEqual(result['installed'], [r['name'] for r in self.rows])
        self.assertEqual(result['status'], 'installed')
        for row in self.rows:
            with self.subTest(skill=row['name']):
                self.assertEqual(s.file_map(self.home / row['path']), row['files'])
        self.assertTrue(Path(result['receipt']).is_file())
        self.assertTrue((Path(result['receipt']).parent / 'notices' / 'THIRD_PARTY.md').is_file())

    def test_single_skill_does_not_copy_others(self):
        result = s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(result['installed'], ['git-remote-ref-recovery'])
        self.assertFalse((self.home / self.by_name['claude-code']['path']).exists())

    def test_second_install_refuses_without_writes(self):
        s.install(ROOT, self.subset(), self.home, apply=True)
        target = self.home / self.subset()[0]['path']
        before = s.file_map(target)
        receipts = set((self.home / 'skill-install-receipts').iterdir())
        with self.assertRaisesRegex(s.CollectionError, 'No files written'):
            s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(s.file_map(target), before)
        self.assertEqual(set((self.home / 'skill-install-receipts').iterdir()), receipts)

    def test_one_collision_blocks_entire_batch_before_writes(self):
        s.install(ROOT, self.subset(), self.home, apply=True)
        with self.assertRaises(s.CollectionError):
            s.install(ROOT, self.rows, self.home, apply=True)
        self.assertFalse((self.home / self.by_name['claude-code']['path']).exists())

    def test_backup_preserves_modified_file_and_mode(self):
        s.install(ROOT, self.subset(), self.home, apply=True)
        target = self.home / self.subset()[0]['path']
        sentinel = target / 'user-note.txt'
        sentinel.write_text('irreplaceable local edits')
        sentinel.chmod(0o600)
        before = s.file_map(target)
        result = s.install(ROOT, self.subset(), self.home, apply=True, backup_existing=True)
        backup = Path(result['backups']['git-remote-ref-recovery'])
        self.assertFalse(backup.is_relative_to(self.home / 'skills'))
        self.assertEqual(s.file_map(backup), before)
        self.assertEqual((backup / 'user-note.txt').stat().st_mode & 0o777, 0o600)
        self.assertEqual(s.file_map(target), self.subset()[0]['files'])

    def test_existing_identity_under_other_category_is_backed_up(self):
        original = self.home / 'skills' / 'other' / 'git-remote-ref-recovery'
        original.parent.mkdir(parents=True)
        shutil.copytree(ROOT / self.subset()[0]['path'], original)
        result = s.install(ROOT, self.subset(), self.home, apply=True, backup_existing=True)
        self.assertFalse(original.exists())
        self.assertTrue(Path(result['backups']['git-remote-ref-recovery']).is_dir())
        self.assertTrue((self.home / self.subset()[0]['path']).is_dir())

    def test_duplicate_installed_identity_refuses(self):
        for category in ['one', 'two']:
            target = self.home / 'skills' / category / 'git-remote-ref-recovery'
            target.parent.mkdir(parents=True)
            shutil.copytree(ROOT / self.subset()[0]['path'], target)
        with self.assertRaisesRegex(s.CollectionError, 'Ambiguous'):
            s.install(ROOT, self.subset(), self.home, apply=True, backup_existing=True)

    def test_symlink_home_refuses(self):
        real = self.scratch / 'actual'
        real.mkdir()
        self.home.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(s.CollectionError, 'symlink'):
            s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(list(real.iterdir()), [])

    def test_symlink_destination_refuses(self):
        self.home.mkdir()
        real = self.scratch / 'actual'
        real.mkdir()
        (self.home / 'skills').symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(s.CollectionError, 'symlink'):
            s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(list(real.iterdir()), [])

    def test_selected_installed_symlink_refuses(self):
        p = self.home / 'skills' / 'git-remote-ref-recovery'
        p.parent.mkdir(parents=True)
        p.symlink_to(ROOT / self.subset()[0]['path'], target_is_directory=True)
        with self.assertRaisesRegex(s.CollectionError, 'symlink'):
            s.install(ROOT, self.subset(), self.home, apply=True, backup_existing=True)

    def test_unrelated_installed_skill_unchanged(self):
        foreign = self.home / 'skills' / 'unrelated'
        foreign.mkdir(parents=True)
        (foreign / 'SKILL.md').write_text('---\nname: unrelated\n---\nOriginal\n')
        before = s.file_map(foreign)
        s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(s.file_map(foreign), before)

    def test_destination_overlap_refuses(self):
        with self.assertRaisesRegex(s.CollectionError, 'overlaps'):
            s.install(ROOT, self.subset(), ROOT, apply=False)

    def test_unsafe_relative_paths(self):
        for value in ['/etc/passwd', '../outside', 'skills/../../outside', 'C:/outside', 'skills\\outside', './skills', 'skills//thing']:
            with self.subTest(value=value), self.assertRaises(s.CollectionError):
                s.safe_relative(value)

    def test_unknown_cli_selection_refuses_without_writes(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/skills.py'), 'install', '--home', str(self.home), '--skill', '../bad', '--apply'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.home.exists())

    def test_malformed_frontmatter_refuses(self):
        p = self.scratch / 'SKILL.md'
        for value in ['no header', '---\nname: example\nBody', '---\nname: ../escape\n---\nBody']:
            with self.subTest(value=value):
                p.write_text(value)
                with self.assertRaises(s.CollectionError):
                    s.entry_name(p)

    def test_changed_payload_refuses(self):
        clone = self.clone()
        (clone / self.subset()[0]['path'] / 'SKILL.md').write_text('changed')
        with self.assertRaisesRegex(s.CollectionError, 'integrity'):
            s.load_collection(clone)

    def test_extra_payload_refuses(self):
        clone = self.clone()
        (clone / self.subset()[0]['path'] / 'unexpected.txt').write_text('extra')
        with self.assertRaisesRegex(s.CollectionError, 'integrity'):
            s.load_collection(clone)

    def test_symlink_payload_refuses(self):
        clone = self.clone()
        p = clone / self.subset()[0]['path'] / 'escape'
        p.symlink_to(self.scratch)
        with self.assertRaisesRegex(s.CollectionError, '(?i)symlink'):
            s.load_collection(clone)

    def test_missing_asset_refuses_even_after_hash_refresh(self):
        clone = self.clone()
        row = self.by_name['leanrea']
        directory = clone / row['path']
        (directory / 'references/upstream-guide.md').unlink()
        data = json.loads((clone / 'skills-manifest.json').read_text())
        for r in data['skills']:
            if r['name'] == 'leanrea':
                r['files'] = s.file_map(directory)
        self.rewrite_manifest(clone, data)
        with self.assertRaisesRegex(s.CollectionError, 'Missing linked asset'):
            s.load_collection(clone)

    def test_stale_catalog_refuses(self):
        clone = self.clone()
        with (clone / 'CATALOG.md').open('a') as handle:
            handle.write('stale edit\n')
        with self.assertRaisesRegex(s.CollectionError, 'catalog'):
            s.load_collection(clone)

    def test_coverage_totals_refuse_inconsistency(self):
        clone = self.clone()
        p = clone / 'coverage.json'
        coverage = json.loads(p.read_text())
        coverage['included_count'] += 1
        p.write_text(json.dumps(coverage))
        with self.assertRaisesRegex(s.CollectionError, 'Coverage totals'):
            s.load_collection(clone)

    def test_duplicate_manifest_identity_refuses(self):
        clone = self.clone()
        data = json.loads((clone / 'skills-manifest.json').read_text())
        data['skills'].append(data['skills'][0])
        self.rewrite_manifest(clone, data)
        with self.assertRaisesRegex(s.CollectionError, 'Duplicate'):
            s.load_collection(clone)

    def test_private_absolute_path_refuses_after_hash_refresh(self):
        clone = self.clone()
        data = json.loads((clone / 'skills-manifest.json').read_text())
        row = next(r for r in data['skills'] if r['name'] == 'git-remote-ref-recovery')
        directory = clone / row['path']
        with (directory / 'SKILL.md').open('a') as handle:
            handle.write('/home/' + 'typhoon/private\n')
        row['files'] = s.file_map(directory)
        self.rewrite_manifest(clone, data)
        with self.assertRaisesRegex(s.CollectionError, 'Machine-specific'):
            s.load_collection(clone)

    def test_cloudflare_original_files_match_import_provenance(self):
        directory = ROOT / self.by_name['security-audit']['path']
        data = json.loads((directory / 'references/import-manifest.json').read_text())
        self.assertEqual(data['source_revision'], 'c1c8a8c1471069fb0e188eeaff69b8e8db6564a8')
        for row in data['files']:
            p = directory / 'references/upstream' / row['relative_path']
            with self.subTest(file=row['relative_path']):
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), row['sha256'])
                self.assertEqual(p.stat().st_size, row['bytes'])
        self.assertEqual(len(data['files']), 22)

    def test_leanrea_restored_upstream_guide_is_exact(self):
        p = ROOT / self.by_name['leanrea']['path'] / 'references/upstream-guide.md'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), '53581bd7fb1fae4352ab43252e67b84667b68895a68e372b99d302b58d9c782d')
        self.assertEqual(p.stat().st_size, 8374)

    def test_existing_home_file_refuses_before_writes(self):
        self.home.write_text('not a directory')
        with self.assertRaises(s.CollectionError):
            s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(self.home.read_text(), 'not a directory')

    def test_existing_category_file_refuses_before_writes(self):
        p = self.home / 'skills' / 'software-development'
        p.parent.mkdir(parents=True)
        p.write_text('preserve category collision')
        with self.assertRaises(s.CollectionError):
            s.install(ROOT, self.subset(), self.home, apply=True)
        self.assertEqual(p.read_text(), 'preserve category collision')
        self.assertFalse((self.home / 'skill-install-receipts').exists())

    def test_unmanifested_loose_skill_file_refuses(self):
        clone = self.clone()
        (clone / 'skills' / 'unexpected.txt').write_text('not inventoried')
        with self.assertRaises(s.CollectionError):
            s.load_collection(clone)

    def test_catalog_regeneration_is_deterministic(self):
        before = {name: (ROOT / name).read_bytes() for name in ['skills-manifest.json', 'CATALOG.md']}
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/update_catalog.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name, data in before.items():
            self.assertEqual((ROOT / name).read_bytes(), data)


if __name__ == '__main__':
    unittest.main()
