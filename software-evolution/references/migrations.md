# Stateful and contract migrations

## Before execution

Identify authoritative data, writers/readers, old clients, schema and API contracts, volume, access paths, data sensitivity, and recovery objectives. Verify a representative sample without exposing production records. Record invariants such as uniqueness, tenant scope, referential integrity, money totals, or event ordering.

Specify coexistence: which old/new application versions work with each schema state. Use **expand → migrate → contract** when rolling deployments or old clients require it:

1. Add compatible fields/endpoints or structures. Keep old readers and writers working. Define how new and old representations remain consistent; dual writes need transactionality or reconciliation, not an assumption of success.
2. Deploy compatible readers/writers in a deliberate order. Backfill with bounded batches, stable cursors/checkpoints, idempotent updates, and a tested restart path. Set timeouts, rate limits, lock/replication-lag limits, and stop conditions from the environment.
3. Reconcile counts and domain invariants, handle rejects, and verify new behavior. Counts alone miss incorrect values, missing tenant scope, and duplicated business effects.
4. Switch reads or traffic gradually where useful. Observe the compatibility window and confirm all supported consumers have moved.
5. Remove old fields/endpoints and transitional code only after evidence supports it. A later contract step can be independently reviewed and deployed.

## Data and recovery safeguards

Estimate lock duration, table rewrites, index build behavior, transaction size, storage growth, and replica lag using the actual database version and official guidance. A syntactically valid migration can still cause an outage.

Rehearse against representative data in isolation. Exercise interruption, retry, malformed records, concurrent writes, and rollback or forward repair. Verify backup restoration if it is part of the plan. Determine the last reversible point; newly written data may make an old binary or down-migration unsafe.

Prepare exact production commands, target/account, dry-run evidence, expected affected rows/resources, and recovery/stop criteria. Execute only within existing authorization. Do not infer permission for deletion from a request to prepare a migration. Preserve a checkpoint and review evidence when a threshold is crossed instead of repeatedly retrying.

## Completion evidence

Record executed batches/versions, rejected records, invariant reconciliation, old/new consumer checks, observation results, and outstanding cleanup. Protect sensitive evidence. Do not call the migration complete until the requested state is reached and its relevant invariants are verified.
