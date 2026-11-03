# Evaluation record

Initial evaluation: 2026-09-10. Updated: 2026-10-13. These results distinguish package correctness, executable installer behavior, description selection, and limited behavioral skill samples. They are not a benchmark of general agent effectiveness. Skill links use the current `kk-` names; the initial runs preceded the namespace change.

## Authored cases

The initial collection had 27 prompts. It now has **57 behavioral cases**: eleven SEO-growth cases, twelve bootstrap cases, four distribution cases, three lifecycle cases, three release-delivery cases, and two per remaining skill. Every case has nonempty grading expectations. Four added bootstrap cases include raw fixtures for React Router/legacy React Query, Query-only usage in Next.js, scoped TanStack Router, and a generic Go CLI. The full suite has **not** been executed. The separate routing set now has 42 lead-skill selection cases; actual runtime automatic-selection precision/recall has not been measured.

## Idea critic imports — 2026-10-13

Imported the supplied `game-idea-critic.zip` and `ios-app-idea-critic.zip` as [kk-game-idea-critic](../kk-game-idea-critic/SKILL.md) and [kk-ios-app-idea-critic](../kk-ios-app-idea-critic/SKILL.md). Preserved all eight supplied files, changing only the skill names and the iOS skill's reference to the game skill. Added two behavioral cases per skill and four routing cases covering concept critique versus ordinary implementation. The collection now contains 17 skills.

Repository structural validation, both official metadata checks, all nine validator regression tests, archive-content comparison with the namespace substitutions, and diff whitespace checks passed. The new behavioral and routing cases have not received model runs. No global installation, commit, push, or publication was performed.

## Initial migration/release behavioral sample

Two independent subagents received the same synthetic [orders migration/release scenario](../kk-release-delivery/evals/files/orders-transition.md), with four rolling instances, old clients supported for 90 days, money-unit conversion, shared retrying jobs, untested nightly backups, and limited staging metrics. One read `kk-software-evolution`, its migration reference, and `kk-release-delivery`. The baseline was instructed not to read those skills or this repository. No production execution or customer communication was authorized or performed.

Both responses were reviewed for:

1. Rejecting the destructive rename during mixed-version operation.
2. Preserving old clients and defining compatible old/new writers.
3. Exact money conversion and data-invariant reconciliation.
4. Durable queue idempotency and crash/acknowledgement behavior.
5. Resumable backfill under concurrent writes.
6. Tested isolated restoration and explicit code/data rollback limits.
7. Baseline-dependent health gates without claiming staging samples prove success.
8. Preserving the preparation-only scope and reporting unexecuted checks honestly.

Both responses addressed all eight broad criteria. They chose different plausible transition mechanisms: the skill-assisted result proposed transactional synchronization covering old writers; the baseline proposed an intermediate compatibility release before enabling new-column reads. Neither implementation was executed or proven correct. Database semantics, full workload behavior, and tooling remain to be validated in an actual project.

The skill-assisted response was longer than necessary and included provisional sample/duration suggestions. The release skill was tightened to keep the runbook operationally concise and distinguish examples from approved thresholds. That wording refinement has not received a new independent behavioral run.

The baseline's output file was rejected twice by automatic approval review, which classified the synthetic runbook as unrelated to the skill-improvement task, including after scope evidence was supplied. Its final text was available and reviewed in the task; no filesystem workaround was attempted. This limits reproducibility of the baseline artifact. No complete paired artifact benchmark, repeated-run statistics, token/time comparison, or superiority claim is reported.

## Deterministic verification

Initial checks on 2026-09-10, locally on macOS:

- Official skill-creator metadata validation passed for all 11 skills.
- Repository validation passed for 11 skills, 27 authored cases, local Markdown links, and workflow YAML parsing.
- All 16 installer tests passed using local mocked downloads, including missing/malformed/mismatched checksums, archive traversal/symlinks, duplicates, and preservation of an existing installation.
- Shell syntax validation and the tracked-diff whitespace check passed.

See the repeatable commands in the [README](../README.md). Metadata validation and YAML parsing establish packaging/syntax properties only. Mocked downloads do not verify GitHub availability, artifact authenticity, cross-platform release success, signing, or hosted CI execution. The new Linux/macOS CI workflow is prepared but has not run on GitHub in this task.

## Description-selection smoke test, 2026-09-13

Two independent agents received the same 24 prompts and either the original or revised description catalog, with identifiers normalized to `kk-` for both. They did not receive skill bodies or expected labels, and they did not execute the tasks. Each chose one lead skill or no skill for a trivial request.

Both matched the expected lead on **24/24 cases**, including the tenant bug fix, review-only correctness request, active incident, old-client migration, AI feature readiness, and no-skill cases. [Catalogs, selections, and limitations](../evals/results/routing-2026-09-13.json) are retained. The original prompts and labels are cases 0–23 in [routing.json](../evals/routing.json); cases 24–26 were added later for distribution and were not part of this smoke test.

This supports a narrower conclusion than the review's prediction: broad implementation wording is a maintainability risk, but these samples did not show it stealing other tasks. There was no measured gain from the description edits on this set. One pass per catalog on curated prompts does not establish reliability, real automatic triggering, or performance on ambiguous unseen requests.

## Bootstrap fixture forward-test, 2026-09-13

An independent agent read the revised bootstrap skill and relevant references, then assessed cases 7–10 using their raw fixtures. It was instructed to read only the prompts and files, not the expected outcomes. All four selected appropriate guidance: generic Node for React Router/legacy React Query; Next.js with supplemental Query guidance; conditional routing setup for scoped TanStack Router; generic Go for the CLI. It added no unrequested release work and reported missing evidence rather than claiming execution.

The response met all nine authored expectations across those four assessment cases. [Recorded selections and reviewer evidence](../evals/results/bootstrap-detection-2026-09-13.json) distinguish direct response fields from reviewer summaries. No fixture application was built or run and there was no old-skill execution baseline for these cases. This is guidance/scope validation, not proof that a generated CI pipeline works.

## Updated deterministic checks, 2026-09-13

The renamed collection passed structural validation for all 11 `kk-` skills, 31 behavioral cases with required expectations, 24 routing cases with positive/negative coverage, resource links, and workflow YAML. All **25 local tests passed**: 16 installer tests and 9 validator regressions. The latter exercise unprefixed identifiers, missing/empty expectations, missing fixtures/resources, broken links, unknown routing labels, and missing negative routing coverage. Shell syntax and tracked-diff whitespace checks also passed. Hosted CI was not run in this follow-up.

## Signed distribution follow-up, 2026-09-13

Added `kk-distribution` with four behavioral cases and three new lead-selection cases. Structural validation passed for **12 skills, 35 behavioral cases, and 27 routing cases**, including namespace, required expectations, fixtures, local resources, and workflow YAML. Official metadata validation passed for the new skill. Shell syntax and tracked-diff whitespace checks passed.

All **33 local tests passed**: 24 installer tests and 9 validator regressions. The installer tests use real OpenSSL RSA/SHA-256 signing and verification with temporary test identities and mocked local downloads. They demonstrate successful installation with the expected key and rejection of missing signatures, untrusted artifact/manifest signers, altered payload/manifest bytes, and a signed wrong version, while preserving the previous installation. Existing checksum and archive-safety tests now use valid signatures so those checks remain exercised. These results validate local signature mechanics, not production publisher identity, certificate management, native OS signing, notarization, or network delivery.

One independent agent assessed the raw multi-platform inventory using the new skill without seeing expected outcomes or grading expectations. Its response met all **six** authored expectations for case 0: aggregate blocking, macOS signing/notarization distinctions, Chocolatey pre-execution trust, honest client-enforcement uncertainty, Linux repository/artifact trust, and final-byte signatures with truthful access limits. [Excerpts, reviewer grades and limitations](../evals/results/distribution-2026-09-13.json) are retained. This was an assessment-only sample, not an executed release or a measured improvement against a baseline. The other three distribution cases and new routing cases have not received model runs.

The Tauri release asset is an intentionally blocked scaffold until project-specific signing and verification are implemented, with no configured public upload path. No hosted CI, Apple signing/notarization, Windows/Chocolatey installation, Linux package-manager installation, or actual publication was performed.

## Follow-up evaluation

### Full lifecycle follow-up, 2026-09-13

Added experience design and platform infrastructure as distinct execution workflows, plus the lifecycle phase-contract reference and a Chinese relationship map. Existing product, implementation and operations skills now carry explicit planning, integration, documentation, support and feedback responsibilities. The source collection has **14 skills, 40 authored behavioral cases and 31 routing cases**. Structural validation and all **9 validator regression tests passed**. Official metadata validation passed for both new skills. The unchanged installer was not rerun in this documentation/skill follow-up; its most recent 24-test result is recorded above.

An independent agent assessed lifecycle case 2 from the raw team-workspace fixture using the revised router/reference and both new skill bodies. It met all **five** authored expectations: separate experience/infrastructure ownership; acceptance and integrated-revision evidence; signature and destructive-change gates; documentation/support/feedback/compatibility/retirement handoffs; and truthful local-preparation limits. [Response excerpts and reviewer grades](../evals/results/full-lifecycle-2026-09-13.json) retain the evidence and limitations. This one assessment does not prove that generated infrastructure or an application works. The four new focused cases and four new routing cases remain unexecuted.

Run each case in an isolated project with representative raw fixtures, record actual artifacts and commands, and grade behavior rather than matching headings. Include negative routing cases and held-out variants. Use repeated baseline/candidate runs before claiming improvement; calibrate subjective judgments with human review. Do not let evaluation agents access live services or incur external side effects merely because a scenario mentions them.

## Scope and concision follow-up, 2026-09-13

Narrowed implementation/security selection to the requested operation, clarified bootstrap/distribution/release ownership, and made tag-specific version and execution steps conditional throughout the shared release reference. Bootstrap now keeps pipeline wiring and the local installer contract while linking to existing stack recipes. Short publication gates remain in each entrypoint so individually installed skills retain the signing requirement. No skill was merged or made dependent on installing siblings.

The four revised entrypoints and bootstrap release reference contain 3,355 whitespace-delimited words, down from 4,451 at `2bcc302` (24.6%). This measures text reduction, not token savings or behavioral improvement. Added bootstrap case 11 with a raw manual-release contract and routing cases 31–32 for manual pipeline setup and a specified auth UI implementation. The collection now has 41 authored behavioral cases and 33 routing cases. These additions and the revised descriptions have not received model runs; earlier selection results apply only to their recorded catalogs.

Repository structural validation, official metadata checks for all four edited entrypoints, all 33 local tests, shell syntax, and diff whitespace checks passed. No hosted build, release, signing service or automatic skill-selection evaluation was executed in this follow-up.

## Bootstrap review fixes, 2026-10-02

Corrected project-reference typechecking guidance and its Electron/TanStack/Wails callers; supplied the Apple export archive path, ZIP creation and explicit app-stapling sequence; removed unconditional tag assumptions from platform recipes; and replaced the installer's line-based release parsing with Python 3 JSON parsing. Python is required only for latest-release discovery, not an explicit `VERSION` install. The README now describes selective installation and identifies generic implementation and lifecycle coordination as consolidation candidates; all 14 skill identifiers remain available.

Local macOS verification:

- All **37 tests passed**: 28 installer tests and 9 validator regressions. New installer checks cover compact/pretty/escaped JSON, nested misleading fields, malformed responses and invalid tag types, missing Python, and explicit-version installation without Python. Existing-install preservation remains checked on rejection.
- The realistic JSON test failed against the previous installer in all three subcases, confirming regression sensitivity. Downloads remained mocked and signatures used ephemeral test keys.
- An isolated TypeScript 5.9.3 fixture with two referenced source projects passed with valid code. Both `tsc -b --force` and per-project `tsc --noEmit -p` detected deliberate type errors in each project.
- Local `xcodebuild -help` confirmed the export argument contract. The documented `ditto` command preserved the root and content of a synthetic app bundle in a ZIP. No actual Xcode archive export, production signing, notarization or store submission was performed.
- Structural validation passed for 14 skills and 41 authored cases, along with shell syntax and diff whitespace checks. Hosted CI and model behavioral/routing evaluations were not run.

## Collection review fixes, 2026-10-02

- Scoped the signed-payload rule to direct distribution: downloads, install scripts, and repositories/feeds/taps the project operates. App stores and language registries (App Store/TestFlight, Play, PyPI, npm, crates.io) now use their required signing and provenance/attestations instead of being blocked on detached signatures no client verifies. Removed the signing clause from `kk-platform-infrastructure`. Added release-delivery case 2 (PyPI + Play without a detached key) as a regression case; it has not received a model run.
- Bootstrap detection now applies every matching row (desktop wrapper plus frontend framework), recognizes `@tauri-apps/cli` and Groovy `build.gradle`, and detects per workspace in monorepos.
- Electron's example Windows target is NSIS because electron-updater does not update MSI installs. Kotlin CI relies on `setup-gradle`'s default wrapper validation instead of contradictory duplicate advice. Python no longer hard-codes Ruff's `target-version`; PyPI publishing uses Trusted Publishing.
- The installer's exact asset names (`<BIN>-<uname -s>-<arch>.tar.gz`) are documented in the release and Go references.
- Action references in templates and references moved to current majors after confirming the used inputs exist: checkout v7, setup-node v7, pnpm/action-setup v6, setup-python v7, setup-java v6, setup-go v7, setup-gradle v6, action-gh-release v3, tauri-action v1, and setup-uv v10.2.0 (no floating major tag after v7). Templates still require resolving to verified SHAs.
- Narrowed `kk-security-review` and `kk-software-verification` descriptions where they overlap built-in diff review.

Structural validation, local tests and shell checks were rerun; no model behavior or routing evaluation was executed.

## SEO growth integration, 2026-10-03

Imported the reviewed `seo-growth` package as `kk-seo-growth`. Narrowed its discovery description, made workflow stages and templates conditional on the requested outcome, and kept the dated personal site snapshot in [optional project notes](seo-site-context.md) outside the reusable package. Added five behavioral cases with raw fixtures and five routing cases, bringing the collection to **15 skills, 47 authored behavioral cases, and 38 routing cases**. These new behavior and routing cases have not received model runs.

Fixed the offline HTML helper's optional row closures, nested-table scoping, inline word boundaries, and JSON-LD isolation from visible text. Its ten bundled tests are also discovered by the repository CI command. The regression suite failed against the original helper and passed after the corrections; it covers inventory output, actual before/after diffs, CLI execution, and missing-input handling.

Local macOS verification: all **47 tests passed** (28 installer, 9 validator, 10 SEO helper); repository structural validation, official skill metadata validation, local resource and icon paths, and tracked-diff whitespace checks passed. The helper remains a static UTF-8 HTML inventory, not a browser, complete HTML5 parser, crawler, or proof of preservation/indexing. No website deployment, live SEO result, hosted CI, or model behavioral evaluation is claimed.

## Versioned SEO release, 2026-10-12

Released the first explicitly versioned SEO package, 1.0.0. Added a programmatic SEO decision/data/publishing workflow, HTML sitemap and category-navigation guidance, a versioned traffic evaluation contract, and a reproducible snapshot helper. Release artifacts are stored under `releases/kk-seo-growth/`; the archive contains the exact package and a manifest of file hashes. Earlier unversioned activity is not assigned a fabricated release identity.

Five new authored scenarios cover record eligibility and repeat imports, unsupported city permutations, HTML versus machine-readable sitemaps, a synthetic confounded traffic comparison, and historical version attribution. The collection now contains **15 skills, 52 authored behavioral cases, and 38 routing cases**. The five new scenarios have not received model runs.

All **52 local tests passed** (28 installer, 9 validator, 10 HTML inventory, 5 release helper). New executable checks establish fingerprint sensitivity, cache exclusion, deterministic archives, archive/manifest consistency, recoverable original identity after edits, refusal to overwrite snapshots, internal-symlink rejection, version validation, and CLI behavior. Repository structural validation, official skill metadata validation, and CSV header/row consistency checks passed. These establish local package and helper properties, not model superiority or traffic improvement.

The release is prepared for future site experiments; no website was deployed, analytics account connected, live traffic baseline collected, or recurring monitor scheduled. No production traffic result is claimed.

## SEO release safeguards and matched evaluation, 2026-10-12

Release 1.1.0 adds an explicit package file list; rejection of unexpected files; stable, modified, unregistered and development states; registry/archive fingerprint verification; refusal to reuse a released version; and repository validation of those constraints. The 1.0.0 release pair remains unchanged. Its legacy archive is verified without imposing the new file-list format retroactively.

Added a standard-library normalized traffic validator, source-specific handling of exported unavailable values encoded as zero, and a complete synthetic ledger/cohort/raw-counts/observation/decision example. The validator withholds calculations on invalid records and withholds individual comparisons on partial or missing observations. It does not verify raw-export truth, infer causal effects, or select a winning skill. Real analytics were not accessed.

One additional authored exported-zero scenario brings the collection to 53 behavioral cases (11 SEO) and 38 routing cases. Two independent agents executed the same 13 SEO tasks against exact 1.0.0 and 1.1.0 packages: the 11 authored tasks plus two held-out artifact tasks. Each completed a canonical-only edit, an original local HTML draft, and experiment-ledger/cohort artifacts. [Inputs, exact fingerprints, outputs, commands and reviewer grades](../evals/results/seo-1.1.0/README.md) are retained. Both received 12 full passes and one partial: the same historical-attribution answer omitted an explicit version-bump reminder. There is no aggregate score advantage or general superiority claim. The candidate additionally exercised its traffic checker on incomplete data and correctly withheld comparisons.

These were single sessions per package, with fixed task order and no repeated trials. Exact runtime model identifier/settings were not exposed; both used the inherited configuration without overrides. Grading was by the parent agent against a separately retained rubric. The evaluation establishes bounded artifact/decision evidence, not browser-rendered usability, automatic routing accuracy, hosted CI, or live traffic improvement.

Final local verification: all **69 repository tests passed**. Repository structural validation, official skill metadata validation, release-registry verification through the installed skill path, and diff whitespace checks passed. The installed 1.1.0 package fingerprint matches the exact candidate used in the paired evaluation: `5b9cafe1c6219fb84b4d2f8ea6fdb6d5c70bce183be7059f5cd331b848976699`.
