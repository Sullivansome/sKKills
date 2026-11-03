This does not establish a visibility decline. The reported 0 is ambiguous: it may represent an observed zero or an unavailable UI value. Without corroboration, normalize it as missing, not as zero exposure.

```json
{
  "source": "saved Search Console generative AI report export",
  "metric": "impressions",
  "raw_value": 0,
  "normalized_value": null,
  "data_status": "missing",
  "missing_reason": "Export may encode unavailable UI values as zero; original UI and corroboration unavailable",
  "period_start": null,
  "period_end": null,
  "property": null,
  "dimensions_and_filters": null,
  "extracted_at": null,
  "baseline_value": null,
  "visibility_change": null
}
```

Preserve the raw zero and this transformation note separately. Do not calculate a decline or percentage from unavailable values. The smallest next evidence is the original report state or an independently verified export distinguishing measured zero from unavailable, plus a comparable prior period with matching scope and metric definitions. Traffic and revenue are also not established; impressions are not visits.
