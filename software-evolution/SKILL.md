---
name: software-evolution
description: Maintain and evolve existing software through dependency upgrades, API/schema/data migrations, debt reduction, deprecation, and service retirement. Use when compatibility, persisted data, existing consumers, or end-of-life obligations make a change more than a local refactor.
---

# Software Evolution

Change or remove a system without abandoning its consumers, data, or operational obligations. Local refactoring alone can use the ordinary implementation workflow.

## Inventory what depends on the change

Inspect current versions, dependency and usage graphs, API consumers, stored data, background jobs, deployment topology, and support commitments. Include older mobile/desktop clients, third-party integrations, scheduled workloads, and infrequently used consumers. Absence from a short log sample is not evidence of no usage.

Clarify the desired outcome: security/compatibility upgrade, lower maintenance cost, new data shape, replacement system, or retirement. Rank debt by actual failure risk, change friction, or operating cost; avoid rewrites motivated only by code aesthetics. Preserve existing tests and observed behavior while isolating intentional changes.

## Choose a change path

- **Dependency/runtime upgrade:** read official migration notes and advisories for the actual version jump; inspect transitive and lockfile changes. Upgrade in the smallest coherent groups, apply necessary code/configuration changes, and verify build, representative behavior, deployment/runtime compatibility, and rollback. Do not run a broad force-fix command without reviewing its breaking effects.
- **API, schema, or data migration:** read [references/migrations.md](references/migrations.md) for compatibility, resumable execution, and data verification.
- **Debt or platform replacement:** establish a behavior/performance baseline, use characterization tests where needed, and replace bounded slices with explicit ownership and cutover criteria. Keep an exit path and remove temporary adapters after verified adoption.
- **Deprecation or retirement:** read [references/retirement.md](references/retirement.md) before disabling access or deleting resources.

Use current official documentation for version-sensitive mechanics. Confirm the package or tool exists; do not substitute a similarly named dependency. Keep required license notices and record distribution changes where relevant.

## Verify the transition

Test supported old and new consumers against the transition state, not just the final design. Exercise failure and resume paths for stateful work. Compare observed user outcomes, data invariants, performance, and cost to the baseline as applicable. Verify backup restoration when the recovery plan depends on it.

Define milestones using evidence: deployed, backfilled, reconciled, consumers migrated, old behavior unused, and cleanup completed. A migration script existing or returning zero is not proof that the data is correct.

## Deliver

Implement the authorized changes and update the existing migration/upgrade/runbook record with versions, compatibility window, checks, execution status, recovery constraints, and remaining owners/actions. Preserve the difference between a prepared plan and an executed production migration. Keep follow-up work explicit, and remove obsolete code/configuration only after its exit conditions are met.
