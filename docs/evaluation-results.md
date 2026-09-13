# Evaluation record

Date: 2026-09-10. These results distinguish package correctness, executable installer behavior, and a limited behavioral skill sample. They are not a benchmark of general agent effectiveness.

## Authored cases

The collection includes 27 realistic prompts in per-skill `evals/evals.json`: two per new skill plus seven bootstrap cases. They cover normal work, scope boundaries, preservation of staged edits, false-green tests, tenant isolation, prompt injection, rollout, migrations, incidents, and retirement. These are reusable test inputs and expectations; the full set has **not** been executed. Automatic skill-selection precision/recall has not been measured.

## Executed behavioral sample

Two independent subagents received the same synthetic [orders migration/release scenario](../release-delivery/evals/files/orders-transition.md), with four rolling instances, old clients supported for 90 days, money-unit conversion, shared retrying jobs, untested nightly backups, and limited staging metrics. One read `software-evolution`, its migration reference, and `release-delivery`. The baseline was instructed not to read those skills or this repository. No production execution or customer communication was authorized or performed.

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

Executed locally on macOS:

- Official skill-creator metadata validation passed for all 11 skills.
- Repository validation passed for 11 skills, 27 authored cases, local Markdown links, and workflow YAML parsing.
- All 16 installer tests passed using local mocked downloads, including missing/malformed/mismatched checksums, archive traversal/symlinks, duplicates, and preservation of an existing installation.
- Shell syntax validation and the tracked-diff whitespace check passed.

See the repeatable commands in the [README](../README.md). Metadata validation and YAML parsing establish packaging/syntax properties only. Mocked downloads do not verify GitHub availability, artifact authenticity, cross-platform release success, signing, or hosted CI execution. The new Linux/macOS CI workflow is prepared but has not run on GitHub in this task.

## Follow-up evaluation

Run each case in an isolated project with representative raw fixtures, record actual artifacts and commands, and grade behavior rather than matching headings. Include negative routing cases and held-out variants. Use repeated baseline/candidate runs before claiming improvement; calibrate subjective judgments with human review. Do not let evaluation agents access live services or incur external side effects merely because a scenario mentions them.
