#!/usr/bin/env python3
"""Reproducible SEO skill packages with explicit contents and release verification."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-dev\.[1-9][0-9]*)?'
IGNORED = {'__pycache__', '.pytest_cache', '.DS_Store'}


def valid_path(name):
    p = PurePosixPath(name)
    return isinstance(name, str) and bool(name) and not p.is_absolute() and '..' not in p.parts and str(p) == name and '\\' not in name


def manifest_for(payload):
    version = payload['VERSION'].decode('utf-8').strip()
    if not re.fullmatch(VERSION_RE, version):
        raise ValueError('VERSION must be major.minor.patch or major.minor.patch-dev.N')
    if 'SKILL.md' not in payload:
        raise ValueError('Missing SKILL.md')
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())}
    canonical = json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode()
    return {'schema_version': 1, 'skill_name': 'kk-seo-growth', 'skill_version': version,
            'skill_sha256': hashlib.sha256(canonical).hexdigest(),
            'hash_method': 'sha256 of UTF-8 JSON file-hash map, sorted keys, compact separators', 'files': hashes}


def collect(root):
    root = Path(root).resolve()
    listing = root / 'PACKAGE_FILES.json'
    if listing.is_symlink():
        raise ValueError('Package listing must not be a symlink')
    declared = json.loads(listing.read_text())
    if not isinstance(declared, list) or any(not isinstance(n, str) or not valid_path(n) for n in declared):
        raise ValueError('PACKAGE_FILES.json must list safe relative file paths')
    if len(set(declared)) != len(declared) or not {'VERSION', 'SKILL.md', 'PACKAGE_FILES.json'} <= set(declared):
        raise ValueError('Package listing has duplicates or missing required files')
    actual = set()
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(p in IGNORED for p in relative.parts) or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise ValueError(f'Internal symlinks are not supported: {relative}')
        if path.is_file():
            actual.add(relative.as_posix())
    if actual != set(declared):
        raise ValueError(f'Package contents differ: unexpected={sorted(actual-set(declared))}, missing={sorted(set(declared)-actual)}')
    payload = {name: (root / name).read_bytes() for name in sorted(declared)}
    return manifest_for(payload), payload


def archive_bytes(manifest, payload):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        files = {f'kk-seo-growth/{name}': data for name, data in payload.items()}
        files['release.json'] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def verify_registry(registry):
    registry = Path(registry)
    if not registry.is_dir():
        raise ValueError(f'Release registry does not exist: {registry}')
    records = {}
    manifests = {p.stem for p in registry.glob('*.json')}
    archives = {p.stem for p in registry.glob('*.zip')}
    if manifests != archives:
        raise ValueError('Registry requires a matching manifest and ZIP for every release')
    for version in sorted(manifests):
        if not re.fullmatch(VERSION_RE, version) or '-dev.' in version:
            raise ValueError(f'Invalid release name: {version}')
        saved = json.loads((registry / (version + '.json')).read_text())
        with zipfile.ZipFile(registry / (version + '.zip')) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError(f'Duplicate ZIP members: {version}')
            expected = {'release.json'} | {'kk-seo-growth/' + n for n in saved['files']}
            if set(names) != expected or any(not valid_path(n) for n in saved['files']):
                raise ValueError(f'Archive contents mismatch: {version}')
            payload = {n: archive.read('kk-seo-growth/' + n) for n in saved['files']}
            if json.loads(archive.read('release.json')) != saved or manifest_for(payload) != saved or saved['skill_version'] != version:
                raise ValueError(f'Release fingerprint mismatch: {version}')
        records[version] = saved
    return records


def status(manifest, records):
    if '-dev.' in manifest['skill_version']:
        return 'development'
    registered = records.get(manifest['skill_version'])
    if registered is None:
        return 'unregistered'
    return 'released' if registered == manifest else 'modified-release'


def verify(root, registry, allow_development=False):
    manifest, _ = collect(root)
    state = status(manifest, verify_registry(registry))
    if state != 'released' and not (state == 'development' and allow_development):
        raise ValueError(f'Package is {state}; use a new development version or publish a new stable release')
    return {'release_status': state, **manifest}


def snapshot(root, destination, registry=None):
    root, destination = Path(root).resolve(), Path(destination).absolute()
    if root == destination.resolve() or root in destination.resolve().parents:
        raise ValueError('Store release archives outside the skill directory')
    manifest, payload = collect(root)
    records = verify_registry(registry) if registry else {}
    state = status(manifest, records)
    if state not in {'released', 'development'}:
        raise ValueError(f'Cannot snapshot {state}; supply its release registry or use a development version')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as out:
        out.write(archive_bytes(manifest, payload))
    return manifest


def publish(root, registry):
    manifest, payload = collect(root)
    if '-dev.' in manifest['skill_version']:
        raise ValueError('Development packages cannot be published as stable releases')
    registry = Path(registry).resolve()
    root = Path(root).resolve()
    if registry == root or root in registry.parents:
        raise ValueError('Release registry must be outside the skill directory')
    registry.mkdir(parents=True, exist_ok=True)
    records = verify_registry(registry)
    version = manifest['skill_version']
    if version in records:
        raise ValueError(f'Release {version} already exists; never reuse a released version')
    archive = registry / (version + '.zip')
    record = registry / (version + '.json')
    # Exclusive creation: never replace an existing release. Clean up only files this call created.
    created = []
    try:
        with archive.open('xb') as out:
            created.append(archive)
            out.write(archive_bytes(manifest, payload))
        with record.open('x') as out:
            created.append(record)
            out.write(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    except BaseException:
        for path in created:
            path.unlink()
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('identity', 'snapshot', 'verify', 'publish'):
        cmd = commands.add_parser(name)
        cmd.add_argument('--registry', type=Path, default=ROOT.parent / 'releases/kk-seo-growth')
        if name == 'snapshot':
            cmd.add_argument('--out', type=Path, required=True)
        if name == 'verify':
            cmd.add_argument('--allow-development', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'identity':
            manifest, _ = collect(ROOT)
            records = verify_registry(args.registry) if args.registry.exists() else {}
            result = {'release_status': status(manifest, records), **manifest}
        elif args.command == 'verify':
            result = verify(ROOT, args.registry, args.allow_development)
        elif args.command == 'publish':
            result = publish(ROOT, args.registry)
        else:
            result = snapshot(ROOT, args.out, args.registry if args.registry.exists() else None)
        print(json.dumps(result, indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'Release failed: {exc}\n')


if __name__ == '__main__':
    main()
