# sKKills

Personal agent skills for shipping software, growing websites, and producing 3D game assets. Each skill carries something an agent would not do by default: personal policy (such as mandatory signing), specialist references, or bundled scripts and templates.

All skill identifiers and folders use the personal **`kk-` namespace**. The original bootstrap skill was named `project-bootstrap` before this rename; the [review response](docs/review-response.md) records that change.

## Choose a skill

| Skill | Use it for |
|---|---|
| [kk-project-bootstrap](kk-project-bootstrap/SKILL.md) | Reproducible tooling, staged-file hooks, real CI checks, initial release automation |
| [kk-distribution](kk-distribution/SKILL.md) | Signed macOS, Windows/Chocolatey, Linux packages; verified installation and updates |
| [kk-seo-growth](kk-seo-growth/SKILL.md) | Website SEO, search-intent content, AI-search visibility, and evidence-based discovery experiments |
| [kk-delegate-3d-modelling](kk-delegate-3d-modelling/SKILL.md) | Delegate 3D assets by complexity through isolated live Blender MCP processes on macOS and Windows, with references and export review |

Install only the skills you need. General engineering practice (implementation, review, security, release, operations) is left to the agent and its built-in commands such as Claude Code's `/code-review` and `/security-review`. A set of lifecycle skills covering those phases was removed on 2026-11-19 because it mostly restated default agent behaviour; see the [evaluation record](docs/evaluation-results.md).

## Shipping software

Bootstrap sets up build machinery; distribution owns package formats, channels, and publisher trust. **Every directly distributed release payload must be signed and verified** — downloads, install scripts, and package repositories, feeds or taps you operate (APT/RPM, Chocolatey, Homebrew). Missing signing credentials or failed verification block publication. Native code signing, package/repository signatures, updater signatures, and detached final-artifact signatures serve different purposes; checksums alone are insufficient. Where an app store, language registry or moderated repository you don't operate is the trust authority (App Store/TestFlight, Google Play, PyPI, npm, crates.io, the Chocolatey community repository, homebrew-core), meet that channel's required signing, keep native OS signatures on the software it installs, and use its supported provenance or attestations instead of adding detached signatures that no client verifies.

The bootstrap references support Node/TypeScript, Next.js, TanStack, Electron, Rust/Tauri, Go/Wails, Python, Kotlin/Android, and Swift/iOS/macOS. They are adaptation guidance: inspect installed versions and verify official documentation before copying version-sensitive commands. CI templates intentionally require adaptation. The CLI installer requires a configured repository and independently trusted public key, signed payloads and versioned manifest, and mandatory checksums. Latest-release discovery additionally requires `python3`; setting `VERSION` avoids that dependency. Authenticate the installer itself before execution.

## SEO growth

`kk-seo-growth` applies to website search discovery; its marketing-distribution reference is separate from `kk-distribution`'s package signing and installation work. Dated personal site observations are optional [project notes](docs/seo-site-context.md), kept outside the reusable skill. Its offline HTML helper requires Python 3.9+ and has bundled regression tests included in the repository test command below.

SEO skill releases have a [version](kk-seo-growth/VERSION), [change history](kk-seo-growth/CHANGELOG.md), and an exact package fingerprint. The latest published release is [1.1.0.zip](releases/kk-seo-growth/1.1.0.zip) with its [manifest](releases/kk-seo-growth/1.1.0.json); the original [1.0.0 snapshot](releases/kk-seo-growth/1.0.0.zip) remains unchanged. The working tree is an unreleased `-dev.N` version until the next release is published. Release validation checks archive contents and registered fingerprints; maintainer steps for snapshots, publishing, and the registry are in [SEO releases](docs/seo-release.md). The [worked traffic example](kk-seo-growth/examples/traffic-pilot/README.md) demonstrates the observation checker, and [matched behavioral results](evals/results/seo-1.1.0/README.md) retain actual prior/candidate artifacts. Follow [versioned evaluation](kk-seo-growth/references/versioned-evaluation.md) to associate deployed site changes and fixed page groups with that identity. Older activity without a recoverable skill snapshot stays `legacy-unknown`; installing an updated skill does not relabel old traffic.

## Install

From this checkout, install through the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add . -g
```

Choose the skills and agents in the install flow; `-g` makes them available across your projects. Omit it for a project-local installation. If you installed skills that have since been removed or renamed, delete the obsolete copies so they do not keep triggering. A remote install uses the version published in the remote repository, so local changes must be published before they appear there:

```bash
npx skills add Sullivansome/sKKills -g
```

## Validate

Use Python 3.9+ in a local environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s kk-delegate-3d-modelling/tests -v
.venv/bin/python -m unittest discover -s tests -v
```

Each skill includes realistic prompts, expected outcomes, and grading expectations in `evals/evals.json`; the validator prints the current case count. [Routing cases](evals/routing.json) check which skill should lead a request, including requests that no skill in this collection should take. The validator checks namespace, metadata, resources, grading expectations, routing labels/coverage, workflow YAML, and the SEO release registry. It does not run agent evals. The [evaluation record](docs/evaluation-results.md) separates these structural checks from observed skill behavior.

The [validation workflow](.github/workflows/validate.yml) runs the same commands on Linux and macOS after pushes to `main` and on pull requests.

When adding a skill, keep its trigger distinct, include only instructions that change the agent's decisions, and validate a realistic case with and without the skill. Avoid adding a new skill when a focused reference in an existing one is sufficient.
