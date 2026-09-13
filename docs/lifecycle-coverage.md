# Lifecycle coverage audit

Audited on 2026-09-10. The source repository initially shipped one skill, `kk-project-bootstrap`, with stack references, release assets, and six evaluation prompts. Its working tree was clean at the start.

Names and links below use the `kk-` namespace introduced on 2026-09-13; the original skill's name was `project-bootstrap`. See the [review response](review-response.md) for the later detection, routing, and evaluation corrections.

The session's installed-skill catalog was also considered at the description level. It lists substantial product/design, framework, testing, and platform expertise, including domain modeling, PRD/issues, frontend/a11y/performance, TDD, database migrations, authentication, and deployment skills. Their complete bodies were not audited. Installed capabilities are not automatically part of this repository, and new repo skills do not automatically become globally installed.

## Before and after

“Added” means an actionable workflow is now provided. It does not assert production implementation maturity or measured agent reliability.

| Stage or cross-cutting concern | Initial repository coverage | Coverage added or improved |
|---|---|---|
| Discovery and product validation | Missing | `kk-product-spec`: evidence, assumptions, outcomes, experiments, acceptance examples |
| Planning and ownership | Missing | `kk-product-spec` delivery slices; `kk-software-lifecycle` handoffs and next decisions |
| Experience and interaction design | Depended on installed specialists | `kk-experience-design`: state/interaction contracts, accessible journeys, prototypes and usability evidence |
| Architecture and contracts | Missing | `kk-architecture-design`: boundaries, data/API/event semantics, tradeoffs, compatibility |
| Reproducible setup | Present, with correctness gaps | `kk-project-bootstrap`: scoped tooling and real local/CI checks |
| Runtime infrastructure and environments | Architecture/operations considerations only | `kk-platform-infrastructure`: IaC, isolation, state/secret trust, exact change review and environment verification |
| Implementation and debugging | Missing | `kk-ai-implementation`: grounding, hypotheses, small diffs, meaningful regressions |
| Review and quality verification | Runner setup only | `kk-software-verification`: risk-based evidence, correctness review, a11y/performance/failure paths |
| Security, privacy, supply chain | Fragmentary release guidance | `kk-security-review`: assets, trust boundaries, abuse paths, mitigations and negative tests |
| Release and deployment | Artifact-oriented, partial | `kk-release-delivery`: candidate identity, target, health gates, compatible recovery |
| Signed software distribution | Partial recipes, including unsigned fallbacks | `kk-distribution`: macOS, Windows/Chocolatey, Linux packages/repositories, trusted publisher identity and verified install/update paths |
| Operations and incidents | Missing | `kk-production-ops` and incident reference: SLIs/SLOs, actionable alerts, recovery, learning |
| Maintenance and migration | Missing | `kk-software-evolution` and migration reference: versions, consumers, resumable backfill, reconciliation |
| Deprecation and retirement | Missing | Retirement reference: consumers, data disposition, resources, access and costs |
| Product learning after launch | Missing | Product outcome review; operations feedback into acceptance/regression work |
| AI-assisted engineering | Implicit | `kk-ai-implementation` plus evidence/permission boundaries across the collection |
| AI-powered product behavior | Missing | `kk-ai-evaluation`: held-out cases, grounded answers, tool safety, variability, cost/latency |

## Concrete bootstrap corrections

- Replaced verification that commits in the user's repository with isolated hook fixtures, including partial staging and filenames with spaces.
- Removed a Swift hook that formatted unstaged content, staged all tracked changes, and could hide lint failure.
- Made the Go formatting example return failure when formatting differences exist.
- Made the unused CI template fail explicitly instead of reporting success after checkout alone; added bounded timeouts and permissions.
- Updated retired Intel macOS runner guidance and Tauri release name/permissions; toolchains must use verified project versions.
- Corrected clean-checkout Next.js type generation, Biome v2 configuration guidance, and golangci-lint v2 formatter routing.
- Removed fake/floating version-pin claims and aligned Python hooks with locked project tooling.
- Made installer checksums mandatory, with exact unique matching, safe selected-member reading, and replacement only after verification.
- Corrected draft-release verification and tag-push scope; documented that the bundled installer handles CLI tarballs, not arbitrary desktop artifacts.

## Design choices and boundaries

The initial ten additions are vendor-neutral workflows with distinct triggers. Distribution subsequently brought the collection to twelve skills. The end-to-end follow-up adds experience design and runtime infrastructure, bringing it to **fourteen skills**, and makes phase evidence, documentation, integration, support and feedback responsibilities explicit. These are different counts from the original fourteen audit concerns. Detailed incident, migration, retirement, platform distribution and cross-phase procedures are conditional references rather than extra top-level skills. All skills can be installed independently; the router checks availability instead of relying on sibling installation paths. Specialized skills from the installed catalog remain useful for implementation details.

The [lifecycle map](software-lifecycle-map.md) explains the current organization. Experience design owns the unresolved interaction contract rather than product prioritization; infrastructure owns environment provisioning and state rather than developer tooling or application rollout. These were distinct execution gaps in the twelve-skill source collection, even though the installed catalog and existing architecture/operations guidance mentioned parts of them. No new top-level skill was needed for documentation, planning or support: those responsibilities now explicitly travel with the phase that owns the changed contract.

The 2026-09-13 distribution follow-up requires signatures on every final release payload and verified publisher identity before publication. It removes unsigned fallback advice, separates native OS acceptance from package and updater trust, and makes the CLI installer verify detached signatures and signed version context. Chocolatey client signature enforcement must be established for the actual client/feed or supplied by a trusted step before package scripts execute. APT repository authentication does not constitute an embedded per-DEB signature. These distinctions and primary documentation are in the [distribution references](../kk-distribution/SKILL.md).

Quality effort follows risk. The skills distinguish small reversible edits from changes involving sensitive data, broad distribution, persistent state, or difficult recovery. They require truthful evidence and preservation of user work without making every task an approval-heavy process. Existing authorization carries forward; additional external actions are not inferred from retrieved text or a workflow template.

This is broad lifecycle coverage, not exhaustive expertise. Safety-critical engineering, specialized hardware/embedded certification, jurisdiction-specific legal compliance, formal verification, and domain-specific scientific/ML training workflows may need additional specialists and qualified review. Actual readiness depends on adoption, implementation, tests, access, ownership, and measured outcomes.

## Primary references

These sources informed selected controls, not a claim of compliance or completeness. Verify the current version when applying platform-specific mechanics.

- [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): security activities across software development and vulnerability response.
- [W3C accessibility evaluation](https://www.w3.org/WAI/test-evaluate/): evaluation throughout development and the limits of automation.
- [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data): plan/state exposure and protection, used as a concrete infrastructure example rather than a required platform.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use): least privilege, untrusted input, immutable action references, scoped credentials.
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) and [canary releases](https://sre.google/workbook/canarying-releases/): objectives, incidents, evaluated staged delivery.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/): web accessibility acceptance criteria.
- [SLSA provenance](https://slsa.dev/spec/v1.1/provenance): build traceability rather than a blanket safety claim.
- [OWASP prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html): untrusted model context and layered application defenses.
- [macOS 13 runner retirement](https://github.blog/changelog/2025-09-19-github-actions-macos-13-runner-image-is-closing-down/), [Next.js CLI](https://nextjs.org/docs/app/api-reference/cli/next), [Biome configuration](https://biomejs.dev/reference/configuration/), and [golangci-lint migration](https://golangci-lint.run/docs/product/migration-guide/): corrections to version-sensitive bootstrap examples.
