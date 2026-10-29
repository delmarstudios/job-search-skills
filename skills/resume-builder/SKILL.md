---
name: resume-builder
description: Build one-page, ATS-safe resumes and matching cover letters as PDFs in a clean "Slate" style (single column, centered name, small-caps section titles, IBM Plex Sans, 11pt minimum) from structured JSON. Use when a tailored resume or cover letter is needed for a job, or when base resume variants are being created.
---

# Resume and cover letter builder

Output: a one-page PDF resume and an optional one-page cover letter with the same letterhead. Single column, no tables, icons or photos, real text in the PDF, so applicant tracking systems parse it cleanly.

## Content rules
- Every line comes from the candidate's facts file. Run `job-fact-check` before calling anything final.
- Body text never below 11pt. If a page overflows, cut or tighten wording; do not shrink type.
- Bullets: action verb + what + how + result. Prefer concrete verbs (built, designed, defined, coordinated) over vague ones ("responsible for", "led").
- Give a one-line descriptor only to employers a reader is unlikely to know.
- Letter size for US employers, A4 elsewhere.
- Cover letters: 250–380 words; opening (role + strongest fit), two proof paragraphs mapped to the JD's main needs, a specific why-this-company paragraph, a short close with availability. No "I am writing to apply", no "dream job".

## Build
```bash
python3 skills/resume-builder/scripts/build_resume.py content.json out/resume.html
bash skills/resume-builder/scripts/render_pdf.sh out/resume.html "out/<First>_<Last>_Resume.pdf"

python3 skills/resume-builder/scripts/build_cover_letter.py letter.json out/letter.html
bash skills/resume-builder/scripts/render_pdf.sh out/letter.html "out/<First>_<Last>_Cover_Letter.pdf"
```
See `examples/` at the repository root for content files. `render_pdf.sh` fails if the PDF is not exactly one page.

## Check before delivering
1. `render_pdf.sh` reports one page.
2. Look at the page (on macOS: `qlmanage -t -s 1100 -o /tmp file.pdf`, then open the PNG): no orphan lines, dates aligned, no highlighted placeholders left in a letter.
3. `job-fact-check` passes.
4. File names are clean: `<First>_<Last>_Resume.pdf` and `<First>_<Last>_Cover_Letter.pdf`. No page size, variant or company name in submitted file names.
