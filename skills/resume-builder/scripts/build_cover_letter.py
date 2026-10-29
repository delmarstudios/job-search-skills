"""Build a one-page cover letter as HTML whose letterhead matches the resume, ready for Chrome PDF export.

Usage: python build_cover_letter.py CONTENT.json OUT.html [--config config/candidate.json]

CONTENT.json:
{
  "page": "Letter" | "A4",
  "date": "29 October 2026",
  "company": "Example Co",
  "recipient": "Hiring Team",
  "paragraphs": ["opening", "proof 1", "proof 2", "why this company", "closing"]
}
Any {field} left in the text is rendered as a highlighted placeholder, so unfinished letters are obvious.
"""
import argparse
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"Letter": "8.5in", "A4": "210mm"}
FONT = ("<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400"
        "&display=swap' rel='stylesheet'>")
CSS = """
@page { size: %(page)s; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
body { width: %(width)s; padding: 0.55in 0.85in; color: #1a1a1a; font-size: 11pt; line-height: 1.38;
       font-family: 'IBM Plex Sans', Arial, sans-serif; -webkit-print-color-adjust: exact; }
header { text-align: center; }
h1 { color: #1F3A3D; font-size: 21pt; line-height: 1.15; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; }
.contact { color: #4a5556; margin-top: 2pt; font-size: 11pt; padding-bottom: 8pt; border-bottom: 0.6pt solid #9AA5A6; }
.contact span + span::before { content: '  ·  '; color: #9AA5A6; }
.meta { margin-top: 20pt; color: #333; }
.salute { margin-top: 16pt; }
p.body { margin-top: 9pt; }
.sign { margin-top: 16pt; }
.sign .name { margin-top: 2pt; font-weight: 700; }
mark { background: #FFF2A8; color: #7a5b00; padding: 0 2pt; border-radius: 2pt; }
"""


def render(text):
    return re.sub(r"\{(\w+)\}", lambda m: f"<mark>[{m.group(1).replace('_', ' ')}]</mark>",
                  html.escape(text, quote=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("out")
    ap.add_argument("--config", default=os.path.join(HERE, "..", "..", "..", "config", "candidate.json"))
    a = ap.parse_args()
    c = json.load(open(a.content, encoding="utf-8"))
    cfg = json.load(open(os.path.expanduser(a.config), encoding="utf-8"))
    page = c.get("page", "Letter")
    doc = [f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(cfg['name'])} Cover Letter</title>{FONT}",
           f"<style>{CSS % dict(page=page, width=PAGES[page])}</style></head><body>",
           f"<header><h1>{html.escape(cfg['name'])}</h1><div class='contact'>"
           + "".join(f"<span>{html.escape(x)}</span>" for x in cfg["contact"]) + "</div></header>",
           f"<div class='meta'>{render(c.get('date', '{date}'))}<br>{render(c.get('recipient', 'Hiring Team'))}, "
           f"{render(c.get('company', '{company}'))}</div>",
           f"<p class='salute'>Dear {render(c.get('recipient', 'Hiring Team'))},</p>"]
    doc += [f"<p class='body'>{render(p)}</p>" for p in c["paragraphs"]]
    doc.append(f"<div class='sign'>Sincerely,<div class='name'>{html.escape(cfg['name'])}</div></div></body></html>")
    open(a.out, "w", encoding="utf-8").write("".join(doc))
    words = len(" ".join(c["paragraphs"]).split())
    print(a.out, f"({words} words in body; aim for 250-380)")


if __name__ == "__main__":
    main()
