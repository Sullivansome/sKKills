# End-to-end execution and evidence

Use this reference for broad software delivery or lifecycle coverage audits. Enter at the current unresolved phase and loop as evidence changes. The table maps responsibility; it does not require sequential departments, extra documents, or every skill invocation for every task.

## Phase contracts

| Phase | Lead and supporting skills | Evidence needed for the next decision |
|---|---|---|
| Discover and prioritize | kk-product-spec | Problem evidence, assumptions, user outcome, scope and success measure |
| Plan useful slices | kk-product-spec; lifecycle coordinates | Acceptance examples, dependencies, risk/learning order, owner and next slice; estimates labeled as estimates |
| Design the experience | kk-experience-design | Critical task/state contract, content, accessible/input behavior, prototype findings or untested hypotheses |
| Design the system | kk-architecture-design; security supports | Domain/data/API contracts, failure modes, constraints, consequential decisions and a first vertical slice |
| Enable contributors | kk-project-bootstrap | Reproducible setup, dependency/toolchain locks, test-data setup and real local/CI commands |
| Provision runtime environments | kk-platform-infrastructure | Reviewed target/configuration, exact change effects, secrets/state handling and verified environment or explicit access gaps |
| Implement and integrate | kk-ai-implementation | Focused change, behavior documentation, compatible contracts, integration evidence and reviewable diff |
| Verify and review | kk-software-verification; security and AI evaluation as applicable | Acceptance-to-check trace, real results, important denial/failure paths and unresolved defects |
| Prepare and promote a release | kk-release-delivery | Exact candidate identity, signing evidence each channel requires, readiness gates, migration compatibility, rollout/recovery and user-facing notes |
| Package and distribute | kk-distribution | Signed native packages/final payloads, authenticated update/install path, channel-specific acceptance and actual availability |
| Operate and support | kk-production-ops | User-facing signals, support/escalation owner, runbooks, recovery evidence, cost/capacity and incident response |
| Learn and reprioritize | kk-product-spec; experience and ops support | Observed task outcomes/support evidence compared to expectations; next experiment, bug or improvement |
| Maintain and migrate | kk-software-evolution | Version/consumer inventory, compatible transition, reconciled data, recovery limits and completed cleanup |
| Deprecate and retire | kk-software-evolution | Consumer transition, data retention/deletion decision, access/resource removal and end-of-support evidence |

UX and architecture inform each other. Environment work can proceed alongside implementation when contracts are stable. Distribution signing/verification precedes the promotion gate even though both are delivery responsibilities. Product feedback and incidents return to earlier phases rather than creating an unrelated queue of reports.

## Cross-cutting responsibilities

- **Security/privacy/supply chain:** assess relevant boundaries during requirements/design, implement controls, verify negative paths, authenticate releases, and respond to newly discovered exposure throughout support. Record data purpose and disposition. Use qualified owners for unresolved domain/legal requirements; do not manufacture a compliance claim.
- **Documentation and developer experience:** each changed contract carries its documentation: setup, API examples, user help, migration/release notes and operational instructions as applicable. Test important documented commands/examples. Reuse project sources of truth instead of adding a parallel document set.
- **Traceability and change ownership:** connect the important acceptance condition to implementation, verification evidence and release identity. Scale from a short issue/PR note to a larger record only when needed. Code review and integration must account for current branch/base changes; prior checks on another revision are not current evidence.
- **AI-assisted engineering:** ground APIs and dependencies, preserve unrelated work, constrain tool authority, review generated changes and independently verify behavior. More generated code or agreeing agents is not quality evidence.
- **AI product behavior:** use kk-ai-evaluation only when the product contains model/prompt/retrieval/tool behavior. Carry model/prompt/data/tool versions and quality/safety/cost regressions through releases and monitoring. AI-written deterministic software does not automatically need model evaluations.

## Minimal handoff record

For multi-phase work, update the existing issue, PR or project record with: intended outcome and acceptance examples; selected revision/artifact and affected contracts; decisions and relevant constraints; checks actually run with their results; unresolved blockers and current authorization; next action/owner and recovery or follow-up condition. Link evidence instead of copying logs or secrets. Name unavailable owners as unassigned rather than inventing them.

Label target-project maturity separately from skill coverage: covered, partial, missing, not applicable with reason, or unverified. A skill file provides a procedure; it does not prove the target app has implemented it. Close the requested scope only after its acceptance evidence exists; explicitly report any remaining external blocker. Publication requires the signing and consumer verification each intended channel requires: detached publisher signatures for direct downloads and operated feeds, channel signing/provenance for stores and registries. Finishing code alone does not close an authorized end-to-end delivery task.

## Adapt to product type and scope

- A service usually needs environment provisioning, staged deployment and operations. Do not generate desktop installers for it.
- A desktop/mobile application needs platform acceptance, signed distribution and upgrade/support compatibility; use the appropriate official store/platform mechanics where relevant.
- A library or CLI needs a clean consumer install, supported runtime/API/CLI contracts, documentation and signed release artifacts using its ecosystem's supported verification path.
- A local tool may mark hosted infrastructure and on-call operation not applicable with reasons. A typo normally needs only a focused edit and proportionate verification.
- Specialized safety-critical, hardware, regulated-domain or scientific-training work may require additional expertise and evidence. Identify that boundary without treating a generic workflow as certification.
