---
name: job-outreach
description: Draft short recruiter and hiring-manager outreach (LinkedIn connection note, LinkedIn message or email, follow-up) for a job application, to raise response rates. Use for top-fit roles once materials are ready, when the candidate asks for outreach or a follow-up, or when a posting names a recruiter or hiring manager.
---

# Recruiter and hiring-manager outreach

Goal: turn an application into a conversation. Produce drafts only. The candidate sends every message personally; never sign in, connect, send or message anyone.

## 1. Inputs
- The role's tracker row (company, role, URL, fit, gaps) and its saved JD.
- The candidate's facts file and config (`config/candidate.json`).

## 2. Find who to contact (public information only)
In order: the person named in the posting; the hiring manager implied by the reporting line, found on the company site or a public web search; the regional recruiting lead. Record name, title and the public URL where you found them. If nobody can be identified with confidence, address "the hiring team" and say so. Never guess a name or an email address.

## 3. Write
Plain and specific: no flattery, no clichés, no emoji. Lead with the role and one concrete overlap from the candidate's real experience, state that the application is in and when they can start, and end with one small ask.

- **Connection note** (≤ 300 characters including spaces):
  `Hi {Name}, I've applied for the {Role} role at {Company}. I spent {N} years in {field} at {employers}, including {one overlap}. Would be glad to connect.`
- **Message or email** (≤ 120 words; email subject `{Role} application – {Candidate name}`):
  1. One line: applied for {Role}; the JD need it matches.
  2. Two lines: the single most relevant result from the facts file, with its real number.
  3. One line: availability and location from the config.
  4. "Happy to share more if useful." Name and LinkedIn from the config.
- **Follow-up** (7–10 days after applying with no reply, ≤ 70 words): role and application date, one new relevant fact not used before, one-line ask.

Write in the language the contact or company works in; offer a second language version when unsure.

## 4. Check and save
Run `job-fact-check` on the drafts. Save them to the role's output folder as `outreach.md`, with the contact's name, title and source URL at the top. If the tracker has a follow-up date column, set it to 7 days after the applied date when empty.
