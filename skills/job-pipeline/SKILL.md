---
name: job-pipeline
description: Run a high-volume, no-duplicate job search as a three-worker pipeline (daily Searcher, Analyst, Materials) that shares one tracker sheet, one facts file and one JD folder, with the candidate approving every application. Use when setting up or operating a job search, screening new roles, or deciding what a worker may change.
---

# Job application pipeline

Three linked workers pass roles along one status column. The candidate approves and submits; workers never apply, message, sign in or create accounts.

```
Searcher (daily) ──New──▶ Analyst ──Screened──▶ Candidate ──Approved──▶ Materials ──Materials ready──▶ Candidate submits ──Applied──▶ …
```

## Shared state
- **Tracker** (Google Sheet or spreadsheet): columns and owners in `templates/tracker_columns.md`. Each worker writes only its own columns, so parallel workers never overwrite each other.
- **Facts file**: the only source of truth for the candidate's experience. See `job-fact-check`.
- **JD folder**: `jds/YYYY-MM-DD_Company_Role.md`, full posting text plus URL, date checked, location rule and pay.
- **Outputs**: one folder per role with `<First>_<Last>_Resume.pdf`, optional `<First>_<Last>_Cover_Letter.pdf`, `outreach.md`, `form_answers.md`.

## Status flow
`New` → `Screened` → `Approved` / `Skipped` (candidate) → `Materials ready` → `Applied` (candidate) → `Screening` / `Assessment` / `Interviewing` / `Offer` / `Rejected` / `Withdrawn`.
Only the candidate sets `Approved`, `Skipped` (except clear eligibility failures) and `Applied`.

## Workers
1. **Searcher** – a scheduled task built from `templates/searcher_prompt.md`. Finds recently posted roles that pass the hard filters (location eligibility at role level, pay floor, excluded role types), dedupes against the tracker by company + title and by URL, saves the JD, appends rows as `New`. Targets a minimum daily count and broadens keywords if short.
2. **Analyst** – for each `New` row: role type, fit (A = tailor fully, B = base resume with keyword tuning, C = long shot), key gaps against confirmed facts only, suggested base resume, a short JD fingerprint (to detect reposted or changed JDs), then `Screened`. Questions that change eligibility or truthfulness go to the candidate, prefixed `QUESTION:`.
3. **Materials** – for each `Approved` row: build the resume (and CL when required or fit A) with `resume-builder`, outreach for fit A with `job-outreach`, form answers with `job-form-answers`; every document passes `job-fact-check`; then `Materials ready`.

## Coordinator
One session starts the Analyst and Materials sessions, relays batches, and gives the candidate one summary table per batch to approve. Rules live in a `PIPELINE.md` in the candidate's workspace (start from `templates/PIPELINE.template.md`) so every worker reads the same version.

## Measure
Track response rate (any reply that is not silence) by role type, source and base resume. Shift the Searcher's mix toward what gets replies.
