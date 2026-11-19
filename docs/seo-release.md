# Releasing kk-seo-growth

Maintainer steps for versioning the SEO skill. Users of an installed copy only need `identity`; see the skill's `references/versioned-evaluation.md`.

## Identity, contents, and status

[VERSION](../kk-seo-growth/VERSION) is the release label and [CHANGELOG.md](../kk-seo-growth/CHANGELOG.md) defines increments: major for incompatible experiment/data contracts or workflow changes, minor for compatible capabilities and guidance, patch for compatible corrections. Use `major.minor.patch-dev.N` for work in progress.

[PACKAGE_FILES.json](../kk-seo-growth/PACKAGE_FILES.json) lists every bundled file. Review new entries rather than auto-adding files. The helper hashes sorted relative paths and their file hashes, ignores Python/tool caches and OS metadata, and rejects internal symlinks. This controls file inclusion, not secrets accidentally written into a declared file.

`identity` reports `released`, `modified-release`, `unregistered`, or `development`, and tolerates undeclared files with a warning (installers may add metadata). `verify`, `snapshot`, and `publish` are strict: an undeclared or missing file stops them before any contents are packaged. The repository validator runs `verify` with development versions allowed, so stable working contents must match their registered fingerprint.

## Release a new version

From the repository root:

```bash
python3 kk-seo-growth/scripts/skill_release.py identity
python3 kk-seo-growth/scripts/skill_release.py verify --allow-development
```

1. While editing released guidance, keep a new `-dev.N` VERSION and describe the change in CHANGELOG.
2. Update PACKAGE_FILES.json for added or removed files.
3. Validate the package, helper tests, and realistic evaluations (`scripts/validate_skills.py` and the unittest commands in the README). Run matched prior/candidate model evaluations where feasible; distinguish authored cases, deterministic tests, and executed model evaluations.
4. Set the stable VERSION, then publish:

   ```bash
   python3 kk-seo-growth/scripts/skill_release.py publish
   python3 kk-seo-growth/scripts/skill_release.py verify
   ```

   `publish` writes a new `releases/kk-seo-growth/<version>.zip` and `.json` pair with exclusive writes and rejects reuse of a registered version.
5. Run repository validation again and commit the release pair with the skill changes.

Never regenerate or edit existing release pairs, including the legacy 1.0.0 archive. SHA-256 verifies consistency, not authenticity; repository history is the audit trail.

## Snapshot for experiment evidence

To keep the exact package beside a site's experiment evidence:

```bash
python3 kk-seo-growth/scripts/skill_release.py snapshot --out <project-evidence-dir>/kk-seo-growth-<version>.zip
```

A stable package must match a registry entry before it can be snapshotted; a copied standalone package needs `--registry <path>`. Store snapshots outside the skill folder and never inside a public repository together with private exports. Existing matching release archives can be reused instead.
