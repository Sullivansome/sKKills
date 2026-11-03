# sKKills

Practical agent skills for high-quality software in the AI coding era: discover → design → build → verify → deliver → operate → evolve → retire.

The collection originally contained only `kk-project-bootstrap`. It now contains **17 focused skills**: one lifecycle coordinator, ten phase skills, three cross-cutting quality skills, one search-growth specialist, and two idea critics. They cover software work from discovery through support and retirement while leaving framework-specific mechanics to the project's tooling and current documentation. Coverage is guidance, not certification or proof that a project is production-ready.

See the [lifecycle map](docs/software-lifecycle-map.md) for responsibilities, handoffs, and product-type differences. The router's [end-to-end execution contract](kk-software-lifecycle/references/end-to-end.md) specifies the evidence carried between phases.

All skill identifiers and folders use the personal **`kk-` namespace**. The original bootstrap skill was named `project-bootstrap` before this rename. The [review response](docs/review-response.md) distinguishes confirmed defects from predictions and records the resulting changes.

## Choose a skill

| Skill | Use it for |
|---|---|
| [kk-software-lifecycle](kk-software-lifecycle/SKILL.md) | Assess gaps and route broad work to the next relevant phase |
| [kk-product-spec](kk-product-spec/SKILL.md) | User outcomes, discovery, acceptance criteria, useful delivery slices |
| [kk-game-idea-critic](kk-game-idea-critic/SKILL.md) | Critique and compare indie game concepts, player decisions, commercial positioning, scope, and playable validation tests |
| [kk-ios-app-idea-critic](kk-ios-app-idea-critic/SKILL.md) | Critique and compare iOS app ideas, substitutes, monetization, platform feasibility, and App Review originality risks |
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
| [kk-seo-growth](kk-seo-growth/SKILL.md) | Website SEO, search-intent content, AI-search visibility, and evidence-based discovery experiments |

Use a focused skill for a focused task. A typo does not need a PRD; a stateful production change needs more than a green unit test. `kk-software-lifecycle` routes broad requests and works even when only part of this collection is installed.

**Installing all 17 is unnecessary.** For repository setup and desktop/CLI delivery, start with `kk-project-bootstrap` and `kk-distribution`. Add product, experience or architecture guidance when those decisions are unresolved; infrastructure, security, release, operations or evolution guidance when the task needs that expertise; and `kk-ai-evaluation` only for AI product behavior. Use the game or iOS app idea critic when deciding whether a concept is worth building or improving its product promise. Framework-specific skills may already cover some of this work, and agents with built-in diff review (for example Claude Code's `/code-review` and `/security-review`) overlap `kk-software-verification` and `kk-security-review` for single-change reviews.

`kk-seo-growth` applies to website search discovery; its marketing-distribution reference is separate from `kk-distribution`'s package signing and installation work. Dated personal site observations are optional [project notes](docs/seo-site-context.md), kept outside the reusable skill. Its offline HTML helper requires Python 3.9+ and has bundled regression tests included in the repository test command below.

SEO skill releases have a [version](kk-seo-growth/VERSION), [change history](kk-seo-growth/CHANGELOG.md), and an exact package fingerprint. The current release is [1.1.0.zip](releases/kk-seo-growth/1.1.0.zip) with its [manifest](releases/kk-seo-growth/1.1.0.json); the original [1.0.0 snapshot](releases/kk-seo-growth/1.0.0.zip) remains unchanged. Release validation checks archive contents and registered fingerprints; development edits require an explicit `-dev.N` version. The [worked traffic example](kk-seo-growth/examples/traffic-pilot/README.md) demonstrates the observation checker, and [matched behavioral results](evals/results/seo-1.1.0/README.md) retain actual prior/candidate artifacts. Follow [versioned evaluation](kk-seo-growth/references/versioned-evaluation.md) to associate deployed site changes and fixed page groups with that identity, then compare traffic and useful outcomes using complete, comparable observations. Older activity without a recoverable skill snapshot stays `legacy-unknown`; installing an updated skill does not relabel old traffic.

`kk-ai-implementation` and `kk-software-lifecycle` are optional process aids. Much of the former repeats ordinary coding-agent practice; the latter mainly coordinates this catalog. They are the first candidates to fold into repository guidance if the collection is consolidated. Keep a separate skill when its procedures or resources add demonstrated value; complete lifecycle coverage does not require one installed skill per phase. `kk-software-verification` remains useful for dedicated testing/review work, but is not a prerequisite for checking an ordinary change.

For shipping software, bootstrap sets up build machinery, distribution owns package formats/channels and publisher trust, and release-delivery coordinates promotion and recovery. **Every directly distributed release payload must be signed and verified** — downloads, install scripts, and package repositories, feeds or taps you operate (APT/RPM, Chocolatey, Homebrew). Missing signing credentials or failed verification block publication. Native code signing, package/repository signatures, updater signatures, and detached final-artifact signatures serve different purposes; checksums alone are insufficient. Where an app store or language registry is the trust authority (App Store/TestFlight, Google Play, PyPI, npm, crates.io), meet that channel's required signing and use its supported provenance or attestations instead of adding detached signatures that no client verifies.

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

The existing bootstrap references support Node/TypeScript, Next.js, TanStack, Electron, Rust/Tauri, Go/Wails, Python, Kotlin/Android, and Swift/iOS/macOS. They are adaptation guidance: inspect installed versions and verify official documentation before copying version-sensitive commands. CI templates intentionally require adaptation. The CLI installer requires a configured repository and independently trusted public key, signed payloads and versioned manifest, and mandatory checksums. Latest-release discovery additionally requires `python3`; setting `VERSION` avoids that dependency. Authenticate the installer itself before execution.

## Validate and improve the collection

Use Python 3.9+ in a local environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
```

Each skill includes realistic prompts, expected outcomes, and required grading expectations in `evals/evals.json` (57 behavioral cases total). Five bootstrap cases use raw manifests, source, or release-contract fixtures for stack and scope decisions; distribution and lifecycle cases include raw readiness inventories. These fixtures are inputs for assessment, not tested full applications or recommended dependency versions.

[Routing cases](evals/routing.json) cover 42 lead-skill choices, including positive and negative coverage for every skill. Selection can use supporting skills as well; an expected lead is not an exclusive allowed-skill list. The validator checks namespace, metadata, resources, grading expectations, routing labels/coverage, and workflow YAML. It does not perform model selection or task execution. Installer, validator, SEO inventory, release-registry, and traffic-observation regression tests run locally without network access. The [evaluation record](docs/evaluation-results.md) separates these structural checks from observed skill behavior.

The [validation workflow](.github/workflows/validate.yml) runs the same commands on Linux and macOS after pushes to `main` and on pull requests. Hosted results are only available after the changes are pushed.

When adding a skill, keep its trigger distinct, preserve user scope and authorization, include only instructions that change decisions, and validate a realistic case. Keep provider-specific details in references and use current primary documentation. Avoid adding a new skill when a focused reference in an existing one is sufficient.
