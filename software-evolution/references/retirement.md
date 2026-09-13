# Deprecation and retirement

Retirement includes consumers, persisted data, infrastructure, credentials, and ongoing costs. It is not just deleting a repository or stopping a server.

## Plan the exit

Inventory users and API clients, incoming traffic, background jobs, webhooks, queues, data stores/backups, secrets, domains/DNS, certificates, monitoring, CI, package registries, billing, and ownership. Determine the replacement/export path, support window, contractual retention, legal holds, and deletion requirements with the responsible owner. Do not infer legal requirements or erase data while their disposition is unresolved.

Define consumer notice and migration milestones, an observable usage window covering infrequent jobs, and fallback or restoration criteria. Draft notices and migration instructions; send only with authorization. For public APIs/packages, preserve useful deprecation and replacement information without silently breaking supported consumers.

## Execute in reversible stages

1. Verify replacement/export functionality and reconcile transferred data. Test a restore if it is the fallback.
2. Stop new enrollment or writes when appropriate, drain in-flight jobs and queues, then disable traffic using a reversible switch. Observe missed consumers and preserve the ability to restore service during the agreed window.
3. Revoke unused credentials and integrations, remove scheduled jobs and delivery routes, and disable obsolete infrastructure in the correct dependency order. Remove dangling DNS or integration references before releasing resources they could point to; retain defensive domain ownership where needed.
4. Archive operational knowledge and required source/artifacts with a named owner. Delete or retain data/backups according to the established policy and authorized scope, including third-party copies where applicable.
5. Remove obsolete monitors, CI, subscriptions, resources, and access grants. Verify traffic, jobs, sensitive data disposition, and residual billing from actual evidence.

Check existing authorization before irreversible deletion, credential revocation, or ownership release. Prepare the exact resource inventory and reversible work first; ask only for missing authority. A generic cleanup request is not permission to destroy unknown shared resources.

## Record completion

Report disabled and deleted resources, migrated consumers, retained data and reasons, verified billing/access state, restoration deadline if any, and remaining obligations/owners. Keep “retired but retained for policy” distinct from “fully deleted.”
