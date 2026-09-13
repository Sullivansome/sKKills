# Incident response

## Stabilize and keep a reliable record

1. Establish user impact, affected environment, onset, scope, and incident owner. If ownership is unknown, identify the needed responder without inventing one. Record timestamps with a timezone. Distinguish facts, hypotheses, actions, and results.
2. Inspect health signals, recent changes, deployment/configuration identifiers, dependencies, and saturation with the least intrusive tools available. Preserve useful logs and evidence; avoid secrets or personal data in the incident record. Do not delay urgent containment to complete a perfect timeline.
3. Choose the lowest-risk mitigation supported by evidence: rollback a compatible release, disable a feature, shed load, or isolate a failing component. Check data compatibility before rollback. Use existing emergency authorization; a runbook does not grant new production privileges. Prepare the exact action and expected result before asking for any missing approval.
4. Make a bounded change, record it, and evaluate user-facing signals. Avoid concurrent speculative fixes, unbounded restarts/retries, or disabling authentication to restore availability. Stop if the mitigation worsens impact.
5. Validate recovery through a critical journey and a meaningful observation interval. Check deferred queues, partial writes, duplicates, and stale caches for lingering damage. A process restart or green health endpoint alone is not recovery.

Draft concise status updates containing impact, known facts, current mitigation, and next update point. Send them only when authorized. Do not guess restoration times. For suspected compromise, preserve evidence and coordinate containment, credential rotation, and the appropriate security owner; do not destroy forensic data as routine cleanup.

## Learn after stabilization

Create a blameless record of impact, detection, timeline, contributing conditions, mitigation, recovery verification, and remaining uncertainty. Separate confirmed causal chains from plausible explanations. Assign follow-ups only to known owners: prevention, detection, response, and a regression or recovery test. Each action needs an observable completion condition; “be more careful” is not one.

Update the relevant runbook and acceptance/regression cases. Do not rewrite architecture during an active incident unless it is necessary for recovery. Report “mitigated” or “monitoring” until the available evidence supports “resolved.”
