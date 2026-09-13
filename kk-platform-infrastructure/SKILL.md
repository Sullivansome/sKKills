---
name: kk-platform-infrastructure
description: Create or change reproducible runtime environments and infrastructure as code, including networks, identities, secrets, storage, environment isolation and drift handling. Use for provisioning or infrastructure change plans; use kk-project-bootstrap for repository tooling/CI, kk-release-delivery for app rollout, and kk-production-ops for active incidents.
---

# Platform Infrastructure

Make the application's required environments reproducible, inspectable and recoverable using the existing platform. Infrastructure configuration, its deployment and runtime health are different evidence states.

## Establish ownership and target

Inspect existing infrastructure definitions, state/backend configuration, provider versions, topology, identities and environment boundaries. Confirm the intended account/project, region, environment and affected resources using available evidence. Do not infer production identity from a directory name. Read actual installed-version documentation before using provider-specific commands.

Identify ownership, availability/capacity needs, permitted costs, data location and retention constraints, and recovery requirements. Prefer an existing managed service or simple environment when it meets the requirements; do not introduce orchestration or another cloud without a demonstrated need. A local-only app may need no hosted infrastructure.

## Define reproducible environments

Use the established IaC/configuration system. Separate configuration from secret delivery, isolate development/test/staging/production appropriately, and document justified differences. Specify dependencies, network exposure, service identities and least privilege, encryption/trust configuration, storage lifecycle, backups, resource limits and cost visibility as applicable.

Protect state, plan files and credentials with access controls and appropriate storage. A redacted console does not prove the saved artifact contains no secrets. For Terraform, see the official [sensitive-data guidance](https://developer.hashicorp.com/terraform/language/manage-sensitive-data). Avoid credentials in source, broadly accessible CI artifacts or generated reports. Inspect untrusted configuration and provider/plugin sources before executing it with privileged credentials; planning is not a universal sandbox.

Preserve existing resources and IDs where needed. Import/adopt unmanaged resources only after matching real ownership and identity; do not recreate them merely because state is missing. Specify state locking or equivalent concurrency control, state recovery and drift detection. Do not silently accept drift or force-unlock an active operation.

## Review the exact change

Generate the supported preview/plan when authorized access is available, or prepare local configuration and report why a live preview is unavailable. Review actual creates, updates, replacements and deletions, privilege/network expansion, persistent-data effects, dependencies and estimated cost changes. A successful syntax check is not a reviewed execution plan.

Record the target, configuration revision, provider/lockfile versions and plan identity. Check recovery feasibility: reverting source cannot restore deleted data or undo an external side effect. Require verified recovery evidence for changes that depend on a restore. Resolve unexpected destructive effects before applying the plan.

Prepare the concrete configuration, reviewed plan and verification/recovery steps before requesting any missing execution approval. Reuse prior authorization for the stated target and actions. Do not apply infrastructure in a preparation-only task. If the target, inputs or state changed enough to invalidate the plan, refresh it and reassess the changed effects before execution.

## Execute, verify and transfer ownership

When execution is authorized, use the reviewed plan or the tool's equivalent mechanism to bind the reviewed change to execution. Serialize conflicting operations and stop on failed or partial changes; inspect actual state before retrying. Do not blindly retry replacements or assume a failed apply made no changes.

Verify resource state, network and identity boundaries, secret delivery, service connectivity, backup configuration and required health signals. Exercise an allowed denial path as well as legitimate access. Test rebuild/restore in an isolated environment where recovery depends on it; do not call a configured backup a proven restore.

Carry verified environment endpoints/identifiers, configuration revision, limitations, ownership, drift checks, cost signals and recovery evidence to application delivery and operations. Do not copy secret values into handoff documents. Report separately: authored, validated, planned, applied, and runtime-verified. Application artifacts retain this collection's signed-and-verified release requirement; provisioning success does not waive it.
