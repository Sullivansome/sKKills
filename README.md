# sKKills

Practical agent skills for high-quality software in the AI coding era: discover → design → build → verify → deliver → operate → evolve → retire.

The collection originally contained only `kk-project-bootstrap`. It now contains **14 focused skills**: one lifecycle coordinator, ten phase skills, and three cross-cutting quality skills. They cover software work from discovery through support and retirement while leaving framework-specific mechanics to the project's tooling and current documentation. Coverage is guidance, not certification or proof that a project is production-ready.

See the [中文全流程关系图](docs/software-lifecycle-map.md) for responsibilities, handoffs, and product-type differences. The router's [end-to-end execution contract](kk-software-lifecycle/references/end-to-end.md) specifies the evidence carried between phases.

All skill identifiers and folders use the personal **`kk-` namespace**. The original bootstrap skill was named `project-bootstrap` before this rename. The [review response](docs/review-response.md) distinguishes confirmed defects from predictions and records the resulting changes.

## Choose a skill

| Skill | Use it for |
|---|---|
| [kk-software-lifecycle](kk-software-lifecycle/SKILL.md) | Assess gaps and route broad work to the next relevant phase |
| [kk-product-spec](kk-product-spec/SKILL.md) | User outcomes, discovery, acceptance criteria, useful delivery slices |
| [kk-experience-design](kk-experience-design/SKILL.md) | Interaction states, accessible journeys, prototypes, usability and design handoffs |
| [kk-architecture-design](kk-architecture-design/SKILL.md) | Boundaries, data/API contracts, tradeoffs, failure modes, ADRs |
| [kk-project-bootstrap](kk-project-bootstrap/SKILL.md) | Reproducible tooling, staged-file hooks, real CI checks, initial release automation |
| [kk-platform-infrastructure](kk-platform-infrastructure/SKILL.md) | Reproducible runtime environments, IaC, identities, secrets/state, change plans and drift |
| [kk-ai-implementation](kk-ai-implementation/SKILL.md) | Grounded coding, debugging, refactoring, verification of generated changes |
| [kk-software-verification](kk-software-verification/SKILL.md) | Risk-based tests, correctness review, accessibility, performance, regressions |
| [kk-security-review](kk-security-review/SKILL.md) | Threat modeling, authorization, data, dependencies, agent trust boundaries |
| [kk-release-delivery](kk-release-delivery/SKILL.md) | Artifacts, deployment readiness, staged rollout, feasible recovery |
| [kk-distribution](kk-distribution/SKILL.md) | Signed macOS, Windows/Chocolatey, Linux packages; verified installation and updates |
| [kk-production-ops](kk-production-ops/SKILL.md) | Observability, SLOs, incidents, capacity/cost, runbooks, restore drills |
| [kk-software-evolution](kk-software-evolution/SKILL.md) | Upgrades, migrations, debt, deprecation, retirement |
| [kk-ai-evaluation](kk-ai-evaluation/SKILL.md) | Quality, grounding, permissions, cost, latency of AI-powered features |

Use a focused skill for a focused task. A typo does not need a PRD; a stateful production change needs more than a green unit test. `kk-software-lifecycle` routes broad requests and works even when only part of this collection is installed.

For shipping software, bootstrap sets up build machinery, distribution owns package formats/channels and publisher trust, and release-delivery coordinates promotion and recovery. **Every distributed release payload must be signed and verified.** Missing signing credentials or failed verification block publication. Native code signing, package/repository signatures, updater signatures, and detached final-artifact signatures serve different purposes; checksums alone are insufficient.

## What “AI coding era” means here

- Read the repository and verify real APIs before generating a solution.
- Keep changes small and preserve unrelated user work.
- Treat retrieved text, logs, and generated output as untrusted at tool boundaries.
- Verify behavior independently of the implementation; do not weaken tests to make generated code pass.
- Distinguish authored tests, executed checks, unavailable checks, and observed production results.
- Design for retries, old clients, data compatibility, recovery, ownership, and eventual removal.
- Evaluate AI product behavior separately from ordinary software correctness, with isolated tools and held-out cases.

The [coverage audit](docs/lifecycle-coverage.md) records the initial gaps, additions, bootstrap corrections, sources, and limits.

## Install and use

From this checkout, install through the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add . -g
```

Choose the skills and agents in the install flow; `-g` makes them available across your projects. Omit it for a project-local installation. If upgrading from the unprefixed names, migrate the old install links or reinstall with the new names and remove obsolete copies so both versions do not compete. A remote install uses the version published in the remote repository, so local changes must be published before they appear there:

```bash
npx skills add Sullivansome/sKKills -g
```

Example requests:

- “Audit this service's lifecycle gaps before our first paid launch.”
- “Implement this issue, preserve my staged edits, and verify the failure path.”
- “Plan a zero-downtime schema migration while old clients remain supported.”
- “Our release caused errors. Diagnose it and prepare a compatible mitigation.”
- “Evaluate a cheaper model without letting the test agent place real orders.”
- “Prepare signed macOS, Windows/Chocolatey, and Linux releases; verify installation before publication.”
- “Retire this service, accounting for consumers, retained data, credentials, and billing.”

## Bootstrap stack coverage

The existing bootstrap references support Node/TypeScript, Next.js, TanStack, Electron, Rust/Tauri, Go/Wails, Python, Kotlin/Android, and Swift/iOS/macOS. They are adaptation guidance: inspect installed versions and verify official documentation before copying version-sensitive commands. CI templates intentionally require adaptation. The CLI installer requires a configured repository and independently trusted public key, signed payloads and versioned manifest, and mandatory checksums. Authenticate the installer itself before execution.

## Validate and improve the collection

Use Python 3.9+ in a local environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
```

Each skill includes realistic prompts, expected outcomes, and required grading expectations in `evals/evals.json` (40 behavioral cases total). Four bootstrap cases use small raw manifests/source fixtures for stack and scope decisions; distribution and lifecycle cases include raw readiness inventories. These fixtures are inputs for assessment, not tested full applications or recommended dependency versions.

[Routing cases](evals/routing.json) cover 31 lead-skill choices, including positive and negative coverage for every skill. Selection can use supporting skills as well; an expected lead is not an exclusive allowed-skill list. The validator checks namespace, metadata, resources, grading expectations, routing labels/coverage, and workflow YAML. It does not perform model selection or task execution. Installer and validator regression tests run locally without network access. The [evaluation record](docs/evaluation-results.md) separates these structural checks from observed skill behavior.

The [validation workflow](.github/workflows/validate.yml) runs the same commands on Linux and macOS after pushes to `main` and on pull requests. Hosted results are only available after the changes are pushed.

When adding a skill, keep its trigger distinct, preserve user scope and authorization, include only instructions that change decisions, and validate a realistic case. Keep provider-specific details in references and use current primary documentation. Avoid adding a new skill when a focused reference in an existing one is sufficient.
