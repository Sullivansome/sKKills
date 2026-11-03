Fixed the isolated copy at `after/landing.html`: the canonical is now `https://example.test/sketch-dash/`.

Local source diff and before/after inventories confirm the only edit is the canonical URL. Reversing that replacement reproduces the original exactly. Saved `source.diff`, `page-changes.json`, and `execution.log`. Original input unchanged; no redesign, analytics, or deployment. This source check does not establish served HTML or indexing.
