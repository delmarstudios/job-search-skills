---
name: job-form-answers
description: Fill job application form questions (work authorization, availability, employment history, reasons for leaving, type of business, salary, why this company, short bio) from the candidate's confirmed answer bank. Use whenever application-form questions are pasted, a portal asks for answers beyond the resume, or a role's materials need prefilled answers.
---

# Application form answers

The answer bank is the file at `form_answers_file` in `config/candidate.json` (start from `templates/form_answers.template.md`). Facts behind it live in the facts file.

## Steps
1. Read the bank, the config, and the role's JD.
2. For each question, in form order:
   - **In the bank:** reuse the answer exactly. Employer names, titles, dates and reasons for leaving must be word-for-word identical across applications; background checks compare them.
   - **Role-specific** (why this company, motivation, a relevant example): write 2–4 specific sentences from the JD and the facts file, then run `job-fact-check` on them.
   - **Marked ASK USER, or not answerable from confirmed facts** (salary without a confirmed floor, sponsorship, relocation, criminal record, samples, equipment, anything new): do not guess. Collect them into one short question list for the candidate.
   - **Salary:** use the confirmed floor in the config (`pay_floor`), converted to the unit the form asks for. If the posting states a range above the floor, "Within your posted range" is acceptable.
3. Respect character or word limits by trimming the least relevant sentence first. If line breaks may be lost, use semicolons instead of numbered lines.
4. Output each answer in its own fenced `text` block under its question so it can be copied, then the open questions.
5. When the candidate answers an open question with a reusable fact, update the bank (replace the ASK USER line) and the facts file, dated.

## Never
Submit the form, tick consent boxes, answer demographic or EEO questions on the candidate's behalf, or invent a salary, reference, certification or legal status.
