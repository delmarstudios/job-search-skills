---
name: job-fact-check
description: Truthfulness gate for job-application materials. Use before a resume, cover letter, recruiter message or application-form answer is marked final or handed to the candidate, and whenever a draft adds a new number, title, date or claim.
---

# Job materials fact check

Every resume, cover letter, outreach note or form answer must trace to the candidate's confirmed facts file (`facts_file` in `config/candidate.json`). The candidate's latest direct corrections in that file win over older entries. Nothing passes on "probably true".

## 1. Mechanical check (always run)

```bash
python3 skills/job-fact-check/scripts/fact_check.py DRAFT.html [MORE.html|.md|.txt ...] --config config/candidate.json
```

It checks:
- **Resumes** (file name contains "resume"): each employer's title and dates match `employers` in the config exactly.
- **Numbers**: every number appears in the facts file, or in `allowed_numbers` with a stated reason (for example "6+ years" computed from dates).
- **Claims** that are commonly inflated: people management, P&L, quota, negotiation, UAT, model training, financial modeling, hype words, plus `extra_banned_claims` from the config.

Exit code 1 means stop: fix the wording, rebuild, run again. Never silence a finding by adding an exception unless the candidate confirmed the fact; record the fact in the facts file first.

## 2. Manual review (the script cannot judge meaning)

Read each bullet or sentence next to the facts file and confirm:
- **Ownership** – the verb matches what the candidate actually did (proposed, coordinated, built, owned). Work done by colleagues, vendors or account managers is credited to them.
- **Attribution** – shared results say "contributed to"; approximate results stay approximate ("double-digit" never becomes "23%").
- **Scope** – a side project is not presented as a job; analysis is not presented as ownership of the downstream operation.
- **Consistency** – titles, cities, dates and reasons for leaving match every other application; background checks compare them.
- **Location and availability** match the config.

## 3. Report

One line per document: `PASS` or `FIX: <what>`. Only `PASS` documents may move to "Materials ready".
