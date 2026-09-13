# sKKills

Practical agent skills for high-quality software in the AI coding era: discover → design → build → verify → deliver → operate → evolve → retire.

The collection originally contained only `project-bootstrap`. It now contains **11 focused skills**. They cover the major lifecycle workflows while leaving framework-specific implementation to the project's tooling and available specialist skills. Coverage is guidance, not certification or proof that a project is production-ready.

## Choose a skill

| Skill | Use it for |
|---|---|
| [software-lifecycle](software-lifecycle/SKILL.md) | Assess gaps and route broad work to the next relevant phase |
| [product-spec](product-spec/SKILL.md) | User outcomes, discovery, acceptance criteria, useful delivery slices |
| [architecture-design](architecture-design/SKILL.md) | Boundaries, data/API contracts, tradeoffs, failure modes, ADRs |
| [project-bootstrap](project-bootstrap/SKILL.md) | Reproducible tooling, staged-file hooks, real CI checks, initial release automation |
| [ai-implementation](ai-implementation/SKILL.md) | Grounded coding, debugging, refactoring, verification of generated changes |
| [software-verification](software-verification/SKILL.md) | Risk-based tests, correctness review, accessibility, performance, regressions |
| [security-review](security-review/SKILL.md) | Threat modeling, authorization, data, dependencies, agent trust boundaries |
| [release-delivery](release-delivery/SKILL.md) | Artifacts, deployment readiness, staged rollout, feasible recovery |
| [production-ops](production-ops/SKILL.md) | Observability, SLOs, incidents, capacity/cost, runbooks, restore drills |
| [software-evolution](software-evolution/SKILL.md) | Upgrades, migrations, debt, deprecation, retirement |
| [ai-evaluation](ai-evaluation/SKILL.md) | Quality, grounding, permissions, cost, latency of AI-powered features |

Use a focused skill for a focused task. A typo does not need a PRD; a stateful production change needs more than a green unit test. `software-lifecycle` routes broad requests and works even when only part of this collection is installed.

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
npx skills add .
```

Choose the skills and agents in the install flow. A remote install uses the version published in the remote repository, so local changes must be published before they appear there:

```bash
npx skills add Sullivansome/sKKills
```

Example requests:

- “Audit this service's lifecycle gaps before our first paid launch.”
- “Implement this issue, preserve my staged edits, and verify the failure path.”
- “Plan a zero-downtime schema migration while old clients remain supported.”
- “Our release caused errors. Diagnose it and prepare a compatible mitigation.”
- “Evaluate a cheaper model without letting the test agent place real orders.”
- “Retire this service, accounting for consumers, retained data, credentials, and billing.”

## Bootstrap stack coverage

The existing bootstrap references support Node/TypeScript, Next.js, TanStack, Electron, Rust/Tauri, Go/Wails, Python, Kotlin/Android, and Swift/iOS/macOS. They are adaptation guidance: inspect installed versions and verify official documentation before copying version-sensitive commands. CI templates intentionally require adaptation; the CLI installer requires a configured repository and mandatory checksums.

## Validate and improve the collection

Use Python 3.9+ in a local environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
```

Each skill includes realistic prompts and expected outcomes in `evals/evals.json`. Structural validation checks metadata, local links, and eval data; installer tests exercise success and failure behavior without network access. These checks do **not** prove skill effectiveness. The [evaluation record](docs/evaluation-results.md) distinguishes executed behavioral samples from cases authored for future testing.

The [validation workflow](.github/workflows/validate.yml) runs the same commands on Linux and macOS after pushes to `main` and on pull requests. Hosted results are only available after the changes are pushed.

When adding a skill, keep its trigger distinct, preserve user scope and authorization, include only instructions that change decisions, and validate a realistic case. Keep provider-specific details in references and use current primary documentation. Avoid adding a new skill when a focused reference in an existing one is sufficient.
