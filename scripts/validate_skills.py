#!/usr/bin/env python3
"""Validate skill packaging and evaluation data; this does not run agent evals."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    skills = sorted(root.glob('*/SKILL.md'))
    if not skills:
        errors.append('No skills found')
    names = set()
    case_count = 0
    for path in skills:
        label = str(path.relative_to(root))
        text = path.read_text()
        match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
        if not match:
            errors.append(f'{label}: missing YAML frontmatter')
            continue
        try:
            meta = yaml.safe_load(match[1])
        except yaml.YAMLError as exc:
            errors.append(f'{label}: {exc}')
            continue
        if not isinstance(meta, dict):
            errors.append(f'{label}: metadata must be a mapping')
            continue
        name = meta.get('name')
        if (not isinstance(name, str) or len(name) > 64
                or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)):
            errors.append(f'{label}: invalid name')
        elif name != path.parent.name or name in names:
            errors.append(f'{label}: name must be unique and match directory')
        else:
            names.add(name)
        desc = meta.get('description')
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            errors.append(f'{label}: description must be 1–1024 characters')
        if len(text.splitlines()) >= 500:
            errors.append(f'{label}: split conditional detail into references')
        if '[TODO:' in text:
            errors.append(f'{label}: unfinished skill scaffold')
        ep = path.parent / 'evals/evals.json'
        try:
            data = json.loads(ep.read_text())
            cases = data['evals']
            if data['skill_name'] != name or not isinstance(cases, list) or len(cases) < 2:
                raise ValueError('expected matching skill_name and at least two evals')
            ids = set()
            for case in cases:
                cid = case['id']
                if type(cid) is not int or cid in ids:
                    raise ValueError('eval ids must be unique integers')
                ids.add(cid)
                for key in ('prompt', 'expected_output'):
                    if not isinstance(case[key], str) or not case[key].strip():
                        raise ValueError(f'empty {key}')
                files = case.get('files', [])
                if not isinstance(files, list):
                    raise ValueError('files must be a list')
                for item in files:
                    if not (path.parent / item).is_file():
                        raise ValueError(f'missing fixture: {item}')
                checks = case.get('expectations', [])
                if not isinstance(checks, list) or any(not isinstance(x, str) or not x.strip() for x in checks):
                    raise ValueError('invalid expectations')
            case_count += len(cases)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{ep.relative_to(root)}: {exc}')

    # Check Markdown file links only; external links and fragments need other checks.
    docs = [root / 'README.md', *root.glob('docs/*.md')]
    for skill in skills:
        docs.extend(skill.parent.rglob('*.md'))
    for path in docs:
        if not path.is_file():
            errors.append(f'{path.relative_to(root)}: missing document')
            continue
        for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            url = urlsplit(link.strip('<>'))
            if url.scheme or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.exists():
                errors.append(f'{path.relative_to(root)}: broken link {link}')
    workflows = [*root.glob('.github/workflows/*.yml'),
                 *root.glob('project-bootstrap/assets/workflows/*.yml')]
    for path in workflows:
        try:
            # BaseLoader avoids YAML 1.1 interpreting the Actions "on" key as True.
            doc = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
            if not isinstance(doc, dict) or 'on' not in doc or not doc.get('jobs'):
                raise ValueError('expected workflow triggers and jobs')
        except (yaml.YAMLError, ValueError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return errors, len(skills), case_count


if __name__ == '__main__':
    problems, skill_count, eval_count = validate()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print(f'Validated {skill_count} skills, {eval_count} authored eval cases, and local Markdown links. Agent evals were not executed by this check.')
