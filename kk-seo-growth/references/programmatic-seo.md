# Programmatic SEO

Use this workflow when a repeatable search task and a maintained dataset can produce useful pages. Automation is a production method, not evidence of demand or permission to publish every combination.

## Choose a page family

Start with audience/product fit, representative current search results, and the distinct material available for each variation. Map query clusters to existing URLs before generating candidates. Examples:

| Pattern | Material that earns a separate page |
|---|---|
| Use-case templates or examples | Original usable assets and situation-specific adaptation notes |
| Product comparisons | Verified differences that change a decision, with dated evidence |
| Integrations | Actually supported workflows, setup, triggers/actions, and limitations |
| Location or attribute directories | Accurate relevant listings, meaningful selection criteria, local availability |
| Audience solutions | Demonstrated task-specific workflows and requirements |
| Conversions or calculators | Correct working calculations, units, input validation, and useful output |

A short working tool may supply more value than lengthy prose. Do not use word counts or textual similarity scores as universal publication thresholds. Do not extrapolate visits from a famous site's page count or repeat unaudited traffic estimates as a forecast.

## Define the data contract

Adapt [page records](../assets/programmatic-pages.csv) to the site's existing data store; a spreadsheet is sufficient for a pilot. Keep a stable page ID independent of title/slug, canonical URL, intent cluster, template version, distinct material, evidence sources, usage rights, verification date, and review due date. The material reference can point to structured records or usable assets rather than stuffing them into a CSV cell. Keep a disposition and reason for every candidate:

- **Publish:** the task is distinct, the evidence/material is sufficient, and applicable checks pass.
- **Merge:** an existing page serves the same task; preserve useful material and plan redirects if an old public URL is retired.
- **Hold:** material is missing, stale, unsupported, or insufficiently distinct; keep it out of generated public pages, navigation, and XML sitemaps.

Define required fields and freshness expectations for the particular page family. Verify permission to reuse third-party material. Handle unavailable facts as unknowns; omit or qualify claims rather than generating plausible values. A source outage must not silently replace useful published content with an empty page.

## Generate and inspect a pilot

Build one representative template and preview a small batch selected to cover typical, sparse, and boundary records. Choose the batch size for the dataset and authorized scope, not a fixed SEO quota.

- Reject duplicate IDs and conflicting URLs. Treat A/B and B/A as the same comparison unless the user task truly differs.
- Import/update by stable ID; rerunning the same input must not create duplicate pages. Protect intentional editorial overrides and review URL changes.
- Generate metadata, internal links, and sitemap entries from eligible published records. Test link targets and unintended indexing/canonical exclusions.
- Verify the actual utility: copyable templates, valid listings, reproducible integrations, or accurate calculations, as applicable.
- Inspect rendered desktop/mobile output for representative records, including missing optional fields and long values. Compare before/after output for existing pages.
- Prepare a recoverable source/data snapshot and a bounded release. Verify public content after authorized deployment; a draft or build is not publication.

## Navigation and URL lifecycle

Provide a useful path from an accessible topic/category hub to each published page. Use contextual related links where they help the next task. Follow [HTML sitemap guidance](technical-seo.md#html-sitemaps-and-category-navigation); an unstructured all-URL dump is not a substitute for browseable categories.

Define which filter combinations have independent value. Do not expose a combinatorial crawl space for empty results, arbitrary sort orders, or duplicate filters. Keep crawling controls, noindex, and canonical signals distinct; consult current [Google faceted-navigation guidance](https://developers.google.com/crawling/docs/faceted-navigation) before choosing controls. Invalid or nonsensical facet combinations should return an appropriate not-found response; temporarily empty useful categories require a separate product/content decision.

Track source changes and review deadlines. Decide whether to refresh, hold new publication, retain a useful historical page with a clear status, consolidate into a relevant replacement, or retire a URL. Use permanent redirects only for genuine replacements; avoid sending unrelated retired pages to the homepage. Keep navigation and sitemaps aligned with the final state. Do not mass-remove established pages solely because a short traffic window is empty.

## Expand from evidence

Record the pilot's skill fingerprint, template/data revision, exact URLs, and deployment date through [versioned evaluation](versioned-evaluation.md). Measure discovery, organic arrivals, task completion, and maintenance effort separately. Expand when usefulness, data upkeep, and observed outcomes justify the next batch. Investigate indexing or measurement gaps before interpreting missing traffic as a page-quality verdict.
