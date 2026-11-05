#!/usr/bin/env python3
"""Regenerate tracked integrity metadata and CATALOG.md after deliberate edits."""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.skills import ROOT, file_map, safe_relative


def main():
    path = ROOT / 'skills-manifest.json'
    data = json.loads(path.read_text())
    names = {r['name'] for r in data['skills']}
    lines = ['# Skill catalog', '',
             'Generated from `skills-manifest.json` by `scripts/update_catalog.py`.', '',
             '| Skill | Kind | Platforms | License | Purpose |',
             '| --- | --- | --- | --- | --- |']
    for row in sorted(data['skills'], key=lambda r: r['name']):
        directory = ROOT / safe_relative(row['path'])
        row['files'] = file_map(directory)
        row['external_related_skills'] = sorted(set(row.get('related_skills', [])) - names)
        row['source'] = ('https://github.com/NousResearch/hermes-agent' if row['classification'] == 'modified-bundled'
                         else 'TyphooN local workflow/integration')
        if row['name'] == 'security-audit':
            row['source'] = 'https://github.com/cloudflare/security-audit-skill'
        if row['name'] == 'leanrea':
            row['source'] = 'https://github.com/aicodeking/leanrea'
        kind = 'Local/custom integration' if row['classification'] == 'local-custom' else 'Bundled override'
        lines.append(f'| [{row["name"]}]({row["path"]}/SKILL.md) | {kind} | {", ".join(row["platforms"])} | {row["license"]} | {row["description"]} |')
    lines.extend(['', f'Total: **{len(data["skills"])} skills**, **{sum(len(r["files"]) for r in data["skills"])} payload files**.', '',
                  '“Local/custom integration” includes original workflows and local wrappers around attributed upstream packages; it does not mean every line was authored here.', '',
                  'External related skills (install separately through their original distribution):', ''])
    for row in data['skills']:
        if row['external_related_skills']:
            lines.append(f'- `{row["name"]}`: ' + ', '.join('`' + x + '`' for x in row['external_related_skills']))
    catalog = '\n'.join(lines) + '\n'
    data['catalog_sha256'] = hashlib.sha256(catalog.encode()).hexdigest()
    path.write_text(json.dumps(data, indent=2) + '\n')
    (ROOT / 'CATALOG.md').write_text(catalog)
    print(json.dumps({'skills': len(data['skills']), 'payload_files': sum(len(r['files']) for r in data['skills'])}))


if __name__ == '__main__':
    main()
