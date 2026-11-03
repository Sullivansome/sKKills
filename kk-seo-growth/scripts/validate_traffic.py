#!/usr/bin/env python3
"""Check normalized SEO experiment CSVs before descriptive traffic comparisons."""
import argparse
import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def read_rows(path, required):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)) or not set(required) <= set(fields):
            raise ValueError(f'{Path(path).name}: duplicate or missing required columns: {sorted(set(required)-set(fields))}')
        rows = list(reader)
    if not rows:
        raise ValueError(f'{Path(path).name}: no data rows')
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise ValueError(f'{Path(path).name}: malformed CSV row')
    return [{k: v.strip() for k, v in r.items()} for r in rows]


def iso_day(value):
    return date.fromisoformat(value)


def timestamp(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('timestamps require a UTC offset')
    return dt


CONTEXT = ('source', 'property', 'channel', 'search_type', 'country', 'device', 'query_segment', 'metric_definition', 'unit', 'timezone', 'filters')


def validate(observations, cohorts, experiments):
    errors, warnings, comparisons = [], [], []
    obs = read_rows(observations, ('experiment_id', 'cohort_id', 'arm', 'metric', 'period', 'period_start', 'period_end', 'value', 'data_status', 'extracted_at', 'raw_export_ref', *CONTEXT))
    members = read_rows(cohorts, ('experiment_id', 'cohort_id', 'arm', 'page_id', 'canonical_url', 'first_published_at', 'changed_at', 'skill_version', 'skill_sha256', 'site_revision'))
    ledger = read_rows(experiments, ('experiment_id', 'cohort_id', 'release_at', 'skill_version', 'skill_sha256', 'site_revision'))
    records, groups, occupied = {}, {}, set()
    for r in ledger:
        key = (r['experiment_id'], r['cohort_id'])
        if not all(key) or key in records:
            errors.append(f'Experiment ledger duplicate/empty identity: {key}')
        records[key] = r
        try:
            timestamp(r['release_at'])
        except ValueError as exc:
            errors.append(f'{key}: invalid release_at: {exc}')
    for r in members:
        key = (r['experiment_id'], r['cohort_id'], r['arm'])
        group = groups.setdefault(key, [])
        if r['arm'] not in {'treatment', 'control'} or not all(key) or not r['page_id']:
            errors.append(f'Invalid cohort identity: {key}')
        url = urlsplit(r['canonical_url'])
        if url.scheme not in {'http', 'https'} or not url.netloc or url.fragment:
            errors.append(f'{key}: invalid canonical URL')
        for kind, value in [('id', r['page_id']), ('url', r['canonical_url'])]:
            identity = (r['experiment_id'], kind, value)
            if identity in occupied:
                errors.append(f'{key}: duplicate page membership across cohorts/arms ({kind})')
            occupied.add(identity)
        group.append(r)
        record = records.get(key[:2])
        if record is None:
            errors.append(f'{key}: missing experiment ledger entry')
        if r['arm'] == 'treatment':
            for field in ('skill_version', 'skill_sha256', 'site_revision'):
                if not r[field] or (record and r[field] != record[field]):
                    errors.append(f'{key}: missing/mismatched {field}')
            if not re.fullmatch('[0-9a-f]{64}', r['skill_sha256']):
                errors.append(f'{key}: invalid package fingerprint')
        try:
            iso_day(r['first_published_at'])
            if r['arm'] == 'treatment':
                iso_day(r['changed_at'])
        except ValueError:
            errors.append(f'{key}: missing/invalid page dates')
    pairs = {}
    for index, r in enumerate(obs, 2):
        label = f'observation row {index}'
        key = (r['experiment_id'], r['cohort_id'], r['arm'])
        pair_key = (*key, r['metric'])
        pair = pairs.setdefault(pair_key, {})
        if key not in groups:
            errors.append(f'{label}: missing cohort membership')
        if r['period'] not in {'baseline', 'followup'}:
            errors.append(f'{label}: invalid period')
        if r['period'] in pair:
            errors.append(f'{label}: duplicate/overlapping observation; provide one aggregate per metric/period/cohort')
        pair[r['period']] = r
        if not r['metric'] or any(not r[c] for c in CONTEXT) or not r['raw_export_ref']:
            errors.append(f'{label}: missing metric context or export provenance (use explicit all/none where applicable)')
        if r['data_status'] not in {'complete', 'partial', 'missing', 'not_measured'}:
            errors.append(f'{label}: invalid data_status')
        try:
            start, end = iso_day(r['period_start']), iso_day(r['period_end'])
            extracted = timestamp(r['extracted_at']).astimezone(ZoneInfo(r['timezone']))
            if end < start or end >= extracted.date():
                errors.append(f'{label}: invalid or unfinished reporting period')
        except (ValueError, ZoneInfoNotFoundError):
            errors.append(f'{label}: invalid date, offset, or IANA timezone')
        try:
            value = Decimal(r['value']) if r['value'] else None
            if value is not None and (not value.is_finite() or value < 0):
                errors.append(f'{label}: value must be finite and nonnegative')
            if value is not None and r['unit'] == 'count' and value != value.to_integral_value():
                errors.append(f'{label}: counts must be integers')
            if r['data_status'] == 'complete' and value is None:
                errors.append(f'{label}: complete observation needs a value')
            if r['data_status'] in {'missing', 'not_measured'} and value is not None:
                errors.append(f'{label}: unavailable observations must have blank values')
            if value == 0 and r.get('zero_evidence') != 'observed':
                errors.append(f'{label}: zero is unverified; preserve ambiguous exported zeros as missing/blank')
            if value == 0 and not r.get('zero_evidence_ref'):
                errors.append(f'{label}: observed zero needs an evidence reference')
        except InvalidOperation:
            errors.append(f'{label}: invalid numeric value')
        if r['data_status'] != 'complete':
            warnings.append(f'{label}: {r["data_status"]}; comparison withheld')
    for key, pair in pairs.items():
        if set(pair) != {'baseline', 'followup'}:
            errors.append(f'{key}: requires baseline and followup rows (use not_measured for unavailable baseline)')
            continue
        a, b = pair['baseline'], pair['followup']
        try:
            a0, a1, b0, b1 = map(iso_day, (a['period_start'], a['period_end'], b['period_start'], b['period_end']))
            if a1 >= b0:
                errors.append(f'{key}: periods overlap or are reversed')
            if (a1-a0).days != (b1-b0).days or a0.weekday() != b0.weekday():
                errors.append(f'{key}: periods have unequal duration or weekday alignment')
            if any(a[c] != b[c] for c in CONTEXT):
                errors.append(f'{key}: baseline/followup source, filters, units, or definitions differ')
            for member in groups.get(key[:3], []):
                if iso_day(member['first_published_at']) > a0 and a['data_status'] == 'complete':
                    errors.append(f'{key}: page lacks a full pre-existing baseline; use a new-page cohort')
                if member['arm'] == 'treatment':
                    changed = iso_day(member['changed_at'])
                    if not a1 < changed <= b0:
                        errors.append(f'{key}: intervention overlaps measurement or postdates followup start')
            record = records.get(key[:2])
            if record and key[2] == 'treatment':
                release_day = timestamp(record['release_at']).astimezone(ZoneInfo(a['timezone'])).date()
                if not a1 < release_day <= b0:
                    errors.append(f'{key}: release date is outside the intervention gap')
            if a['data_status'] == b['data_status'] == 'complete' and a['value'] and b['value']:
                before, after = Decimal(a['value']), Decimal(b['value'])
                if before.is_finite() and after.is_finite():
                    comparisons.append({'experiment_id': key[0], 'cohort_id': key[1], 'arm': key[2], 'metric': key[3], 'page_count': len(groups.get(key[:3], [])), 'days': (a1-a0).days+1, 'baseline': float(before), 'followup': float(after), 'absolute_change': float(after-before), 'relative_change_percent': float((after-before)/before*100) if before > 0 else None})
        except (ValueError, InvalidOperation, ZoneInfoNotFoundError):
            errors.append(f'{key}: invalid comparison inputs')
    # A control used alongside treatment must describe the same measurement context/window.
    arm_contexts = {}
    for r in obs:
        scope = (r['experiment_id'], r['metric'], r['period'])
        context = tuple(r[c] for c in (*CONTEXT, 'period_start', 'period_end'))
        if scope in arm_contexts and arm_contexts[scope] != context:
            errors.append(f'{scope}: treatment/control measurement contexts differ')
        arm_contexts[scope] = context
    # Never emit actionable calculations from a structurally invalid data set.
    return {'valid': not errors, 'errors': errors, 'warnings': warnings,
            'comparisons': comparisons if not errors else [],
            'limitations': 'Descriptive checks only. Does not verify exports, fingerprints against archives, randomization, causal lift, or skill superiority.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('observations', 'cohorts', 'experiments'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.observations, args.cohorts, args.experiments)
    except (OSError, ValueError, csv.Error) as exc:
        result = {'valid': False, 'errors': [str(exc)], 'warnings': [], 'comparisons': []}
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
