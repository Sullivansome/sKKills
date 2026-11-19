# SEO skill releases

## 1.2.0-dev.1 — unreleased

- Removes instructions written for other agent hosts (Sites skills, Library workflow, OpenAI documentation workflow, personal context retrieval) and author-specific examples.
- `identity` works on installed copies: undeclared files produce a warning instead of failing, and a missing registry reports `unregistered`. Packaging commands stay strict. Tool caches (`.ruff_cache`, `.mypy_cache`, `.venv`, `.git`) are ignored; manifests are read as UTF-8.
- Maintainer release, snapshot, and publish steps move from `references/versioned-evaluation.md` to the repository's `docs/seo-release.md`.
- Traffic checker: treatment/control context matching is per cohort, so cohorts of one experiment may use different windows. Documents the Windows `tzdata` requirement.
- Page inventory (schema 2; regenerate both snapshots): honours a BOM or declared charset and warns on undecodable bytes, ignores SVG `<title>`, strips CDATA/comment wrappers around JSON-LD, closes an unclosed anchor at the next `<a>`, and records `<html lang>` and hreflang alternates.
- SKILL.md defers duplicated helper and measurement detail to references; the description names common SEO trigger terms.

## 1.1.0 — 2026-10-12

Adds explicit package contents, release-registry and archive verification, development identities, and rejection of reused release labels. Adds normalized traffic validation, verified-zero provenance, a complete synthetic experiment, and matched behavioral evaluation evidence recorded outside the package. Existing nonzero observation rows remain usable; ambiguous exported zeros must be reviewed before comparison. The immutable 1.0.0 archive is retained.

## 1.0.0 — 2026-10-12

First explicitly versioned release. Adds programmatic SEO eligibility, data and publishing guidance; HTML sitemap and category navigation checks; reproducible release snapshots; and traffic/outcome evaluation tied to skill identity, deployed changes, and fixed page cohorts.

Existing SEO, AI-discovery, scope, evidence, and static HTML inventory guidance is retained. Adds behavioral evaluation scenarios; authored scenarios are not executed model tests. See the repository evaluation record for actual validation.

Earlier uses were unversioned. Label their skill identity `legacy-unknown` unless an exact historical package can be recovered. Do not retroactively attribute their results to 1.0.0. No production traffic improvement is established by this release.

## Release policy

Use major.minor.patch: major for incompatible experiment/data contracts or workflow changes; minor for compatible capabilities and decision guidance; patch for compatible corrections. Update VERSION and this record for released changes. Never overwrite an existing release archive or relabel an old experiment. Intermediate edits retain their distinct package fingerprint and are unreleased until a new version is recorded. Compare fingerprints as well as version labels.
