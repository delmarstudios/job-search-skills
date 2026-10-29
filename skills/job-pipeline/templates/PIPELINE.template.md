# Job application pipeline: {candidate}

Every worker reads this file, the facts file and the tracker before acting. The candidate's latest direct instructions override this file.

## Shared state
- Tracker: {sheet id or file}, tab `{tab}`. Formula columns: U, V (never write).
- Facts: `{facts_file}`.
- JDs: `{workspace}/jds/`.
- Outputs: `{workspace}/outputs/<Company_Role>/` with `{First}_{Last}_Resume.pdf`, `{First}_{Last}_Cover_Letter.pdf`, `outreach.md`, `form_answers.md`.

## Targets
- Role families: {…}
- Location rule: {…}
- Pay floor: {…}
- Exclusions: {…}
- Daily target: {N} applications.

## Worker 1: Searcher
See the scheduled task prompt. Writes A, B, C, D, E, G, H, M = New, R, W.

## Worker 2: Analyst
Picks up `New`. Writes F, I, J, K, L, S, T; sets `Screened` (or `Skipped` only for clear eligibility failures). Reports a summary table.

## Worker 3: Materials
Picks up `Approved`. Builds documents with `resume-builder`, `job-outreach`, `job-form-answers`; runs `job-fact-check` on everything; writes K, L, T; sets `Materials ready`.

## Never
Apply, submit, sign in, message, create accounts, or claim anything the facts file does not support.
