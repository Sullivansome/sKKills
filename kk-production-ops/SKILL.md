---
name: kk-production-ops
description: Improve production observability, reliability, capacity, cost, runbooks, and disaster recovery, or diagnose and respond to a live incident. Use for SLOs, actionable alerts, outages, operational readiness, restore drills, and recurring operational toil.
---

# Production Operations

Make user-impacting failures detectable, diagnosable, and recoverable. Choose the mode from the task: operational improvement or incident response. For an incident, read [references/incident-response.md](references/incident-response.md) immediately and prioritize stabilization over redesign.

## Understand the service

Inspect topology, ownership, critical journeys, dependencies, deployment history, existing telemetry, runbooks, and access constraints. Separate observed production facts from local reproduction or guesses. Use read-only access first; avoid exporting sensitive production data when aggregate or redacted evidence is enough.

Define the reliability objective in user terms: successful eligible requests, completed jobs within a deadline, data freshness, or crash-free sessions. Specify the population, exclusions, time window, and target using actual requirements. An SLI is the measurement; an SLO is its target. Do not invent targets or confuse infrastructure uptime with user success.

## Add useful signals

Instrument the important boundary with structured errors, correlation IDs/traces, latency distributions, throughput, saturation, and domain success/failure signals. Ensure dashboards distinguish versions, regions, and relevant tenants without exposing personal data or creating unbounded metric cardinality. Control sampling, retention, and telemetry cost.

Alert on actionable user impact or imminent exhaustion; connect alerts to an owner, severity, and a runbook. For SLO-based services, consider multi-window error-budget burn alerts. Establish thresholds from service requirements and observed baseline. Route low-urgency trends to normal work rather than paging. Verify that a controlled fault produces the expected signal and reaches the configured route in an authorized test.

## Engineer recovery and capacity

- Set explicit timeouts, bounded retries, backpressure, concurrency/resource limits, and graceful degradation around failing dependencies. Check for retry amplification and cascading failure.
- Measure representative load before tuning. Track latency percentiles, bottlenecks, capacity headroom, and unit cost. Change one relevant variable and compare to baseline; avoid broad optimization without evidence.
- Define recovery time and recovery point goals with the owner. Verify backups, restore into isolation, validate data and access, and record measured recovery time/data loss against those goals.
- Include configuration, secrets/key recovery, dependencies, queues, and regional failure in recovery planning where applicable. A healthy database backup alone may not restore the service.
- Create a concise runbook with symptoms, read-only diagnostics, bounded mitigation, verification, escalation, and known hazards. Exercise high-impact procedures safely; do not conduct production chaos tests without specific authorization.

## Close the loop

Use incident causes, recurring support issues, and observed cost to prioritize work. Automate repetitive operations only after the procedure is understood and has safe retry/stop behavior. Track the user outcome of a reliability change; dashboards and alerts are means, not success metrics.

For ongoing support, define the intake/escalation owner and supported version/environment information needed for diagnosis. Turn reproducible reports into regression cases; route usability problems to experience design and unmet outcomes to product work. Maintain user-facing troubleshooting and support/end-of-life guidance alongside runbooks. Prepare communication within scope; do not send customer messages without authorization.

Deliver changed instrumentation/configuration or runbooks plus what was actually tested. Report unavailable production access explicitly and provide the next concrete verification step. Do not claim an ongoing monitor is active unless it was configured through an available mechanism with user authorization.

For deeper guidance, consult the relevant chapters of the [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) on SLOs, alerting, incidents, and load rather than loading the entire book.
