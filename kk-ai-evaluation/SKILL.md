---
name: kk-ai-evaluation
description: Design and run evaluations for LLM features, RAG systems, prompts, models, and tool-using agents, including quality, grounding, permissions, regressions, latency, and cost. Use when changing AI behavior or deciding whether an AI feature is ready to ship; ordinary AI-written code uses normal software verification.
---

# AI Evaluation

Evaluate the behavior of an AI-powered feature against the task it must perform. Distinguish model quality from the surrounding system's security and reliability.

## Define a falsifiable contract

Identify users, task, allowed data/tools, prohibited side effects, success/failure behavior, fallback or human handoff, and quality/latency/cost requirements. Preserve product constraints. Decide whether an LLM is necessary; compare against an existing deterministic or simpler baseline where available.

Record the exact model/version, prompt, tool schemas, retrieval/index configuration, code revision, sampling settings, and evaluation environment. Provider behavior may change; do not invent fixed version guarantees. Use current official API documentation for supported features.

## Build representative cases

Use consented/de-identified examples or synthetic fixtures that preserve the important structure. Version the dataset with provenance and access controls. Separate development cases from held-out evaluation cases, and keep tuning changes away from the held-out set. Do not expose private datasets to an external model without authorization.

Cover common tasks, realistic ambiguity, insufficient evidence, long or conflicting context, refusal/fallback, multilingual or accessibility needs where relevant, and high-impact failures. Include adversarial retrieved content, cross-user/tenant data, malformed tool arguments, retries, and duplicate side effects for agents. Pair prompt-injection cases with legitimate controls so “refuse everything” cannot earn a good score.

For RAG, test retrieval relevance and permission filtering separately from answer grounding, citation accuracy, and abstention. Retrieval from the wrong tenant is a failure even if the answer is factually correct.

## Choose independent measures

- Use deterministic checks for schemas, exact calculations, permitted tool calls, destination restrictions, data isolation, and required state changes.
- Use task-specific rubrics for answer quality, with concrete pass/fail examples. Compare to verified references when available; do not ask the same model merely whether its own answer is correct.
- Calibrate model judges against human-labeled samples. Blind/randomize candidate order for comparisons, record disagreement, and keep critical security invariants outside a subjective judge.
- Measure end-to-end success, abstention/error rate, latency percentiles, token/tool cost, and relevant slices. Report sample size, repeated-run variability, and uncertainty; a single lucky output is not reliability evidence.

Agree thresholds from the product's consequences and baseline before selecting a winning candidate. Do not hide severe rare failures inside an aggregate average or alter the rubric after seeing results to make a candidate pass.

## Run safely and interpret honestly

Execute against isolated tools and synthetic accounts by default. Simulate side effects unless live actions and their costs are authorized. Bound tool count, recursion, time, retries, and spend. Enforce authorization and parameter validation in application code; prompt text cannot grant tool privileges.

Run baseline and candidate on equivalent cases and conditions, with repetitions when stochastic variance matters. Keep raw outputs and evaluator evidence redacted and versioned. Separate “case authored,” “execution failed,” “not run,” and “passed.” Diagnose failures by retrieval, prompt/model, tool contract, or application logic before tuning.

## Deliver and monitor

Produce the eval dataset/rubric, runnable harness using the existing stack, versioned results, and a decision with limitations. Add the important regressions to the release gate. For rollout, include fallback/kill switch, sampled review with appropriate privacy controls, drift/quality/cost signals, and re-evaluation on model, prompt, tool, or retrieval changes.

An evaluation cannot prove prompt injection impossible. Layer application controls and use [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) for relevant attack/defense cases. Report observed performance and residual risks without claiming universal safety.
