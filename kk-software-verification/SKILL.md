---
name: kk-software-verification
description: Build a risk-based test strategy, review code for correctness, or verify a substantial change before release. Use for missing test coverage, regression prevention, flaky tests, acceptance validation, or an evidence-based quality review of AI-generated code.
---

# Software Verification

Test the intended contract independently of how the implementation happens to work. A green pipeline can still validate the wrong behavior.

## Establish scope and evidence

Read the requested behavior, diff, affected callers, tests, and execution environment. Identify the failure modes with meaningful user impact. Trace critical requirements to a check and an expected result. Reuse the project's test runner and fixtures; do not install a parallel testing framework without a concrete gap.

Separate a review request from a request to fix findings. For review, lead with actionable defects and evidence; do not silently rewrite the change. For implementation, add or repair the checks needed to establish the contract.

## Choose the right checks

| Risk | Useful evidence |
|---|---|
| Pure logic and invariants | Unit, property-based, or boundary-value tests with independent expected results |
| API/database/external integration | Contract and integration tests against a realistic boundary, including incompatibility and failure |
| Critical user journey | A small number of end-to-end tests through the actual UI or interface |
| Authorization and tenant isolation | Denied access, wrong tenant, missing identity, and privilege-change tests |
| Concurrency and state transitions | Duplicate delivery, retries, interleaving, partial writes, cancellation, recovery |
| Usability and accessibility | Keyboard/focus and screen-reader checks, contrast/reflow, error recovery, plus suitable automation |
| Performance or resource limits | Representative workload and baseline; latency percentiles, throughput, memory and cost where relevant |
| Migration or recovery | Old/new compatibility, representative data, interrupted/resumed execution, restore or reconciliation |

Choose checks by risk, not quotas or a universal coverage target. Avoid tests that only assert mock calls, restate implementation constants, or snapshot huge unstable outputs. Use controllable clocks and randomness; isolate data and resources. Mock external boundaries deliberately and document what the mock cannot prove.

For a regression, confirm that the test fails on the old behavior when practical. For critical invariants, targeted mutation or a deliberately faulty implementation can reveal vacuous tests; use it only when it adds confidence, not as ceremony for a copy edit.

## Execute and review

Run targeted checks and required project checks. Record the actual commands, environment, results, and limitations. Missing tests or unavailable services are gaps, not passes. Distinguish pre-existing failures with baseline evidence rather than assuming they predate the change.

Review the diff against invariants and failure modes independently of the author’s explanation. Trace concrete paths and identify the trigger, affected behavior, and minimal correction. Prioritize by impact and likelihood; avoid speculative defects without a plausible path. Report no actionable findings when that is what the evidence supports.

For flaky tests, reproduce and investigate shared state, timing, ordering, external dependencies, and resource cleanup. Replace arbitrary sleeps with observable conditions. Quarantine only with a documented owner and exit condition; do not use retries to conceal a deterministic bug.

For UI work, automated accessibility checks supplement manual interaction; they do not establish full conformance. Use the project's target and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for web acceptance criteria where applicable.

## Deliver

Provide implemented checks or a concise verification report: contract covered, defects with file/location and reproduction evidence, actual results, and unverified risks. Preserve known limitations instead of compressing them into “all tests pass.” Escalate release decisions based on material residual risk; do not claim that test coverage proves absence of bugs.
