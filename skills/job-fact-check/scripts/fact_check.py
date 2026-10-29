"""Mechanical truthfulness check for resumes, cover letters, outreach and form answers.

Compares a document against the candidate's confirmed facts file and config:
  - resumes: every employer's title and dates must appear exactly as in the config
  - every number must appear in the facts file (or in the config's allowed_numbers)
  - common inflated or unconfirmed claims are flagged (plus the config's extra_banned_claims)

Usage:
  python fact_check.py FILE.html|FILE.md|FILE.txt [...] [--config config/candidate.json]
Resumes are detected by "resume" in the file name. Exit code 0 = no mechanical issues,
1 = issues found. Always follow with the manual review described in SKILL.md.
"""
import argparse
import html
import json
import os
import re
import sys

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "candidate.json")

# Claims that job seekers (and AI tools) inflate most often. Each needs a confirmed fact before use.
BANNED = [
    (r"\bdirect reports?\b|\bmanaged a team\b|\bteam of \d+\b|\bpeople manag", "people management"),
    (r"\bP&L\b|\bprofit and loss\b", "P&L ownership"),
    (r"\bquota\b|\bclosed deals?\b", "sales quota"),
    (r"\bnegotiat\w*\b", "negotiation"),
    (r"\bUAT\b|user acceptance test", "user acceptance testing"),
    (r"\bfine-?tun\w*\b|\btrained (?:a|the|an) (?:model|algorithm)\b", "model training"),
    (r"\bfinancial model\w*\b", "financial modeling"),
    (r"\bspearheaded\b|\bworld-class\b|\bvisionary\b", "inflated wording"),
    (r"\bdream job\b", "cover-letter cliché"),
]
MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def visible_text(path):
    raw = open(path, encoding="utf-8").read()
    if path.lower().endswith((".html", ".htm")):
        raw = re.sub(r"(?is)<(style|script|head)\b.*?</\1>", " ", raw)
        raw = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", raw).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    a = ap.parse_args()
    cfg = json.load(open(os.path.expanduser(a.config), encoding="utf-8"))
    facts = open(os.path.expanduser(cfg["facts_file"]), encoding="utf-8").read().replace(",", "")
    fact_nums = set(re.findall(r"\d+(?:\.\d+)?", facts))
    allowed = set(cfg.get("allowed_numbers", {}))
    for c in cfg.get("contact", []):  # phone numbers and similar in the header
        allowed.update(re.findall(r"\d+", c))
    banned = BANNED + [tuple(x) for x in cfg.get("extra_banned_claims", [])]

    issues = 0
    for f in a.files:
        text = visible_text(f)
        print(f"== {f}")
        if "resume" in os.path.basename(f).lower():
            for e in cfg.get("employers", []):
                if e["company"].lower() not in text.lower():
                    continue
                for key in ("title", "dates"):
                    if e[key] not in text and e[key].upper() not in text:
                        print(f"  [employment] {e['company']}: expected {key} '{e[key]}' not found verbatim")
                        issues += 1
        for m in re.finditer(r"\d[\d,]*(?:\.\d+)?", text):
            n = m.group().replace(",", "").rstrip(".")
            if n in fact_nums or n in allowed or re.fullmatch(r"(19|20)\d\d", n):
                continue
            if int(float(n)) <= 31 and re.search(MONTHS, text[max(0, m.start() - 12):m.end() + 12]):
                continue  # day of month in a letter date
            print(f"  [number] '{m.group()}' not in facts: ...{text[max(0, m.start() - 40):m.end() + 40]}...")
            issues += 1
        for pat, why in banned:
            for m in re.finditer(pat, text):
                print(f"  [claim] {why}: ...{text[max(0, m.start() - 40):m.end() + 40]}...")
                issues += 1
    print(f"\n{issues} mechanical issue(s).")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
