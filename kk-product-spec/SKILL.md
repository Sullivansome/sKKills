---
name: kk-product-spec
description: Turn a product idea, feature request, or ambiguous issue into an evidence-based scope with user journeys, acceptance criteria, constraints, and small delivery slices. Use before substantial work when the intended behavior or value is unclear; skip for already-specified fixes.
---

# Product Spec

Make the desired behavior clear enough that an implementer and a reviewer can disagree with it constructively. Work within the user's requested product and technology constraints.

## Ground the problem

Read existing product docs, relevant code and issues, and available user evidence. Identify who has the problem, the task they are trying to complete, the current workaround, and its cost. Label observations, assumptions, and open questions separately. Do not invent customer research, market demand, or usage statistics.

When value is uncertain, choose a cheap way to learn before committing to a large build: inspect support evidence, test a prototype, or define an experiment. Draft interview or outreach materials if useful; sending them needs the user's authorization. A request to build a specified feature is not permission to replace it with product discovery.

## Define the contract

Describe:

- The user outcome and how to observe success, with baseline and target if known. Include a guardrail such as error rate, task completion time, accessibility, or cost so a local metric does not hide harm elsewhere.
- The main journey, permissions, empty/loading/error states, recovery, and important edge cases. Include offline or unreliable connectivity when relevant.
- Scope and explicit non-goals; supported devices, languages, and compatibility commitments when they matter.
- Data collected, purpose, retention/deletion needs, integrations, and known security or privacy constraints. Record unknown legal requirements for the appropriate owner; do not invent compliance claims.
- Measurable performance, reliability, and accessibility expectations appropriate to the product. Negotiate missing thresholds rather than writing unsupported guarantees.

Write acceptance examples as observable behavior: starting state, action, expected result, and failure behavior. Include denied access and duplicate or interrupted requests for features that change important state. Avoid criteria such as “looks modern,” “production ready,” or “tests pass” without a user-visible contract.

## Slice and validate

Choose the smallest useful vertical slice through the relevant UI/API/data path. Separate learning experiments from shipped behavior. Order later slices by user value, risk, and dependency; give each an independently checkable outcome. Avoid splitting only into “all backend” then “all frontend.”

For multi-slice delivery, record dependencies, ownership if known, and the next release/learning milestone in the existing backlog. Label effort/cost estimates with assumptions; do not invent deadlines or team commitments. Carry user help, support implications and outcome instrumentation into relevant acceptance criteria rather than deferring them indefinitely.

Identify the riskiest assumption and the evidence that would change the design. Use a prototype or technical spike only if it resolves that uncertainty; time-bound it and record what it proved. Include instrumentation and a post-launch review point for outcomes that require real usage. Check event definitions and data minimization before collecting telemetry.

## Deliver

Update the existing issue or product document when authorized, or create a concise local spec in the project's convention. Include problem/evidence, behavior and acceptance examples, scope, constraints, delivery slices, and unresolved decisions with their impact. For a small feature, a few paragraphs are enough. Do not create a second PRD if an existing source of truth can be updated.

Hand off to architecture or implementation with the contract and acceptance examples. Completion means the behavior is reviewable and the remaining uncertainties are explicit; it does not mean untested assumptions have become facts.

When interaction decisions remain, use `kk-experience-design` if available before or alongside architecture. After launch, compare actual user outcomes and support evidence with the intended outcome; revise the scope or experiment rather than treating shipment as proof of product value.
