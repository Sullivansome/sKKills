---
name: kk-release-delivery
description: Prepare or execute release promotion, service deployment, staged rollout, and recovery. Use for candidate readiness and production delivery decisions; use kk-project-bootstrap for initial build automation and kk-distribution for package formats, signing, and install/update trust.
---

# Release Delivery

Deliver the intended version with evidence that it works and a feasible response if it does not. Creating an artifact, deploying it, and verifying user behavior are separate states.

## Establish the release contract

Inspect the current release mechanism, repository instructions, target environment, requested version/commit, existing approvals, and affected clients or services. Preserve the project's established trigger; a tag is useful for versioned artifacts, but not mandatory for every service deployment.

Confirm the artifact to deliver, checks required, environment/account, rollout owner, user impact, and recovery constraints. Reuse existing authorization; ask only for missing authority immediately before the consequential action after preparation is complete. Never push unrelated tags, deploy to a guessed account, or send release announcements without authorization.

## Prepare one verifiable candidate

- Run the applicable command contract and compatibility checks for the exact candidate. Link the source commit, version, lockfiles, configuration, and build result.
- Build once and promote the same immutable artifact where the platform permits. Record digests and verify downloaded artifacts; retain required provenance or SBOM evidence.
- Scope CI permissions per job, isolate untrusted pull-request builds from release credentials, and prefer scoped short-lived credentials. Resolve action references to verified commits for production workflows; do not invent SHAs.
- Check environment configuration, secret references, runtime versions, infrastructure plan/drift, quotas, dependencies, and health probes. Keep secret values out of logs and reports.
- Check schema/API compatibility across old and new instances and clients. Use additive migration first when needed. Specify whether code rollback is possible after writes change; reversing a deployment does not reverse data mutations.

Check release notes and supported consumer compatibility. Account for store/channel delays and clients that cannot immediately downgrade. For libraries, inspect package contents, exported APIs and supported runtimes, then test a clean consumer install.

For directly distributed packages, use `kk-distribution` when available and carry its evidence into promotion: exact final payloads, verified publisher/native signatures and required notarization, plus clean install/update results. Missing credentials or failed verification block publication across the requested targets; only an explicit user scope change narrows that set. App stores and language registries use their own required signing and provenance (e.g. Play App Signing, PyPI attestations, npm provenance). For services, use the platform's artifact-signing and verification contract.

## Define rollout and recovery before execution

Choose a strategy proportional to impact: a simple deployment for a small internal tool; a canary, staged audience, or feature flag for uncertain or broad impact. Set health signals, observation window, minimum useful traffic/sample, promotion criteria, and stop/rollback thresholds from requirements and baseline evidence. An absence of traffic is not a successful canary.

If thresholds are unknown, identify the measurement and decision owner needed to set them. Keep illustrative numbers distinct from approved gates; do not insert arbitrary sample sizes or wait times into an executable runbook.

Record the previous artifact/configuration, rollback or roll-forward steps, who can execute them, and how to reconcile side effects. Rehearse recovery in an isolated environment when state or availability risk warrants it. If rollback is unsafe, state why and prepare a tested forward recovery path. A backup is useful only when it can be restored within the required recovery goals.

## Execute within scope and verify

Run the requested release actions, observe actual tool results, and stop escalation on failed checks or crossed thresholds. Preserve evidence before retrying; do not loop deployments blindly. Test an important user journey against the delivered version and check errors, latency, saturation, and relevant business outcomes during the agreed observation window.

For draft releases, verify authenticated draft assets or locally selected artifacts before publication; `/releases/latest` does not select an unpublished draft. After publication, test the explicit published version. Push only the intended tag if tags are the release mechanism.

## Deliver

Record source/version, artifact digest or identifier, target, checks, observed rollout state, and recovery path. Distinguish prepared, built, deployed, published, and verified. Report remaining observation or external approval requirements accurately; schedule monitoring only if authorized and supported. Add an owner and removal condition for temporary rollout flags.

Keep an operator's runbook concise: prerequisites/blockers, ordered actions with gates, recovery, and completion evidence. Put explanations beside the decision they affect and avoid repeating the same constraints across every phase.

Consult [Google SRE canary guidance](https://sre.google/workbook/canarying-releases/) for rollout evaluation and [SLSA provenance](https://slsa.dev/spec/v1.1/provenance) for build traceability when those concerns apply; neither alone certifies a release as safe.
