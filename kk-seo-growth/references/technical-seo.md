# Technical SEO and implementation

## Evidence levels

Distinguish repository source, built HTML, server response, browser-rendered DOM, crawler access, and reported index status. Each answers different questions. Do not claim live production behavior from source files alone. When access is blocked, produce a limited review and a precise list of missing checks.

Use bounded crawling only when authorized and supported. Respect site controls and rate limits. Start with the homepage, key conversion pages, sitemap, robots file, and a representative sample of each template.

## Prioritized inspection

| Area | Check | Interpretation |
|---|---|---|
| HTTP | Final URL, status, redirect chain, relevant headers | A designed 404 is valid; an important landing page returning 404 is a blocker |
| Indexing controls | robots.txt, meta robots, X-Robots-Tag | robots controls crawling; blocking crawling can prevent discovery of a noindex directive |
| Canonicals | Intended indexable URL, absolute resolution, conflicting signals | A canonical is a signal, not a guaranteed exclusion mechanism |
| Sitemaps | Valid reachable canonical URLs, substantive modification dates | Submission assists discovery but does not guarantee indexing |
| Rendering | Main copy and links available in HTML or rendered DOM | JavaScript is not automatically unindexable; verify what can be processed |
| Architecture | Clear navigation, descriptive URLs, contextual links, important orphan pages | Make important pages discoverable through useful links |
| Metadata | Descriptive title, useful description, language, social preview | Titles/snippets can be rewritten; no fixed character count guarantees display |
| Structure | Main heading, readable sections and tables, accessible text | Serve comprehension rather than a numeric SEO rule |
| Media | Alt text, dimensions, loading, crawlable assets, relevant video | Use empty alt for decoration; avoid keyword-stuffed alt text |
| Mobile/performance | Actual interaction, layout, field data if available, lab diagnostics | Separate measured user problems from speculative score optimization |
| Conversion | Primary CTA, working demo/download/store link, price clarity | Verify destination and behavior, not just button appearance |

Review important existing pages before mass-changing metadata. Low CTR can result from position, intent, SERP layout, device, brand mix, or seasonality. Compare similar query/page/device groups before attributing it to a title.

## Framework and URL details

Follow the existing stack. For React/Next/Vue/TanStack or other applications, inspect route handling, metadata generation, server rendering/prerendering where appropriate, hydration failures, and crawlable anchor links. Do not migrate frameworks solely for SEO without a concrete deficiency.

Check canonical consistency across HTTP/HTTPS, www/non-www, trailing slashes, parameters, and preview domains. Ensure staging does not accidentally become the canonical destination. Keep useful filtered pages indexable only when they have distinct value; do not blanket-index every parameter combination.

For multilingual sites, verify language quality and localized task fit. Check reciprocal hreflang, canonical alignment, and an appropriate language selector if used. Do not publish country/language permutations without useful localized content.

## HTML sitemaps and category navigation

An HTML sitemap is a user-facing navigation page; crawlers follow its links as ordinary links. It does not replace a machine-readable sitemap and is not a supported sitemap submission format in Search Console. Google supports XML, RSS/Atom, and plain-text URL lists; see [supported formats](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

Recommend an HTML sitemap or topic directory when it resolves a navigation/discovery problem. A small well-linked site may need no additional page. Organize large collections by useful topics or categories, which then link to individual resources; do not automatically dump every URL onto one page. Reuse an effective existing hub instead of creating a redundant sitemap.

For generated collections, verify a crawlable path from an accessible hub to each eligible published page. Use descriptive `<a href>` links, verify targets, and inspect pagination where it is needed to reach the full collection. Search-box-only access or click handlers without usable links do not establish such a path. See [Google's link guidance](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).

Check mobile navigation and meaningful grouping; exclude drafts, broken targets, and duplicate filter permutations. Keep ordinary navigation useful for visitors, including appropriate support/about pages even when they are not acquisition targets. HTML and XML lists need not be identical. Do not promise ranking lifts, guaranteed indexing, or resolution of a Search Console sitemap-report error merely because HTML links are reachable. Distinguish a valid file, an observed crawler fetch, successful sitemap-report processing, and page index status.

## Structured data

Consult current official documentation for supported types and eligibility. Mark up only facts visible to users and genuinely applicable entities. Distinguish schema.org validity from Google rich-result eligibility and actual display.

Do not invent ratings, reviews, organization details, offers, or availability. Do not assume FAQ, review, or software markup receives a rich result. Verify current support. Validate syntax and relevant requirements, then inspect visible content consistency. Do not treat schema as special AI recommendation markup.

## Preserve and verify

Capture original output or use version history. Review source changes and semantic inventories, including tables/rows, CTAs, links, images, headings, and JSON-LD. A rewrite must not quietly remove useful functionality or evidence.

The bundled page_inventory.py is a local static HTML helper. It cannot crawl, render JavaScript, verify indexation, detect all schema semantics, infer trustworthiness, or guarantee preservation. Use it with source diffs and rendered inspection.

For authorized deployment, verify the changed URLs and representative content after release. If stale content appears, investigate the built artifact, changed routes, deployed version, origin, cache headers, service worker, and browser separately. Do not diagnose caching solely from old-looking text.

Record validation and uncertainty. Observe indexing later through legitimate inspection/reporting tools; do not promise immediate indexing or repeatedly resubmit URLs without evidence of a fix.
