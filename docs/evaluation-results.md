# Evaluation record

Initial evaluation: 2026-09-10. Updated: 2026-09-13. These results distinguish package correctness, executable installer behavior, description selection, and limited behavioral skill samples. They are not a benchmark of general agent effectiveness. Skill links use the current `kk-` names; the initial runs preceded the namespace change.

## Authored cases

The initial collection had 27 prompts. It now has **40 behavioral cases**: eleven bootstrap cases, four distribution cases, three lifecycle cases, and two per remaining skill. Every case has nonempty grading expectations. Four added bootstrap cases include raw fixtures for React Router/legacy React Query, Query-only usage in Next.js, scoped TanStack Router, and a generic Go CLI. The full suite has **not** been executed. The separate routing set now has 31 lead-skill selection cases; actual runtime automatic-selection precision/recall has not been measured.

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
