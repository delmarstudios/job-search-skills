# Tracker columns

| Col | Header | Written by | Notes |
|---|---|---|---|
| A | Date found | Searcher | YYYY-MM-DD |
| B | Company | Searcher | |
| C | Role | Searcher | Official title |
| D | Job URL | Searcher | Prefer the company or ATS page |
| E | Source | Searcher | Company site / ATS board / LinkedIn / AI platform / Job board / Referral / Other |
| F | Role type | Analyst | Your own families, e.g. Strategy & Ops, Business Ops, Customer support |
| G | Location eligibility | Searcher | Worldwide remote / APAC remote / Country remote OK / City onsite / To verify / Not eligible |
| H | Pay | Searcher | As stated, with currency |
| I | Fit | Analyst | A / B / C |
| J | Key gaps | Analyst | Against confirmed facts only |
| K | Resume version | Analyst → Materials | Suggested base, then the exact version used |
| L | Cover letter | Analyst → Materials | Custom / Base / Not required |
| M | Status | All, per the status flow | Dropdown |
| N | Applied date | Candidate | |
| O | First response date | Candidate | Any reply counts, including rejections |
| P | Response type | Candidate | Rejection / Recruiter screen / Assessment / Interview / Other |
| Q | Next follow-up | Materials / Candidate | 7 days after applying by default |
| R | JD last checked | Searcher | |
| S | JD fingerprint | Analyst | 1–2 lines of key requirements |
| T | Notes | Analyst / Materials | File paths, `QUESTION:` items |
| U | Dedupe key | Formula | `=ARRAYFORMULA(IF(LEN(B2:B),LOWER(TRIM(B2:B))&" | "&LOWER(TRIM(C2:C)),))` |
| V | Duplicate? | Formula | `=ARRAYFORMULA(IF(LEN(U2:U),IF((COUNTIF(U2:U,U2:U)>1)+(LEN(D2:D)>0)*(COUNTIF(D2:D,D2:D)>1),"Duplicate",""),))` |
| W | JD file | Searcher | File name in `jds/` |

Summary tab ideas: applied today vs daily target, applied in the last 7 days, response rate, follow-ups due, and response rate by role type and by source. Count "applied" only from `Applied` onward so pipeline rows do not inflate it.
