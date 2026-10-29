"""Build a one-page resume as HTML in the "Slate" style, ready for Chrome PDF export.

Usage: python build_resume.py CONTENT.json OUT.html [--config config/candidate.json]

CONTENT.json:
{
  "page": "Letter" | "A4",
  "show_availability": true,
  "summary": "...",
  "jobs": [{"company": "...", "city": "...", "title": "...", "dates": "...",
            "descriptor": "optional one-line company description", "bullets": ["..."]}],
  "skills": [["Label", "comma-separated items"]],
  "education": [["School", "Degree; honors", "Year"]]
}
Name, contact line, work authorization and availability come from the config.
"""
import argparse
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"Letter": "8.5in", "A4": "210mm"}
FONT = ("<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400"
        "&display=swap' rel='stylesheet'>")
CSS = """
@page { size: %(page)s; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
body { width: %(width)s; padding: 0.42in 0.62in; color: #1a1a1a; line-height: %(lh)s; font-size: 11pt;
       font-family: 'IBM Plex Sans', Arial, sans-serif; -webkit-print-color-adjust: exact; }
header { text-align: center; }
h1 { color: #1F3A3D; font-size: 21pt; line-height: 1.15; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; }
.contact { color: #4a5556; margin-top: 2pt; font-size: 11pt; }
.contact span + span::before { content: '  ·  '; color: #9AA5A6; }
h2 { color: #1F3A3D; font-size: 12pt; margin: 9pt 0 3pt; padding-top: 3pt; border-top: 0.6pt solid #9AA5A6;
     font-variant: small-caps; letter-spacing: 0.06em; font-weight: 600; }
.row { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
.job { margin-top: 4pt; }
.job:first-of-type { margin-top: 0; }
.co { font-weight: 600; color: #1F3A3D; }
.city, .dates { color: #555; white-space: nowrap; }
.role, .desc { font-style: italic; }
.desc { color: #555; }
ul { margin: 1.5pt 0 0 0; padding-left: 13pt; }
li { margin-bottom: 1pt; padding-left: 2pt; }
li { list-style: none; position: relative; }
li::before { content: '–'; position: absolute; left: -11pt; color: #6F7F80; }
.skills p, .edu .row { margin-bottom: 1pt; }
"""


def esc(t):
    return html.escape(t, quote=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("out")
    ap.add_argument("--config", default=os.path.join(HERE, "..", "..", "..", "config", "candidate.json"))
    a = ap.parse_args()
    c = json.load(open(a.content, encoding="utf-8"))
    cfg = json.load(open(os.path.expanduser(a.config), encoding="utf-8"))
    page = c.get("page", "Letter")
    second = [cfg["work_authorization"]] + ([cfg["availability"]] if c.get("show_availability") else [])
    out = [f"<!doctype html><html><head><meta charset='utf-8'><title>{esc(cfg['name'])} Resume</title>{FONT}",
           f"<style>{CSS % dict(page=page, width=PAGES[page], lh=c.get('line_height', '1.14'))}</style></head><body>",
           f"<header><h1>{esc(cfg['name'])}</h1>",
           "<div class='contact'>" + "".join(f"<span>{esc(x)}</span>" for x in cfg["contact"]) + "</div>",
           "<div class='contact'>" + "".join(f"<span>{esc(x)}</span>" for x in second) + "</div></header>",
           f"<h2>Summary</h2><p>{esc(c['summary'])}</p><h2>Experience</h2>"]
    for j in c["jobs"]:
        desc = f" <span class='desc'>· {esc(j['descriptor'])}</span>" if j.get("descriptor") else ""
        out.append(f"<div class='job'><div class='row'><div><span class='co'>{esc(j['company'])}</span>{desc}</div>"
                   f"<div class='city'>{esc(j['city'])}</div></div>"
                   f"<div class='row'><div class='role'>{esc(j['title'])}</div><div class='dates'>{esc(j['dates'])}</div></div>"
                   "<ul>" + "".join(f"<li>{esc(b)}</li>" for b in j["bullets"]) + "</ul></div>")
    out.append("<h2>Skills</h2><div class='skills'>"
               + "".join(f"<p><b>{esc(l)}:</b> {esc(t)}</p>" for l, t in c["skills"]) + "</div>")
    out.append("<h2>Education</h2><div class='edu'>"
               + "".join(f"<div class='row'><div><span class='co'>{esc(s)}</span>, {esc(d)}</div><div class='dates'>{esc(y)}</div></div>"
                         for s, d, y in c["education"]) + "</div></body></html>")
    open(a.out, "w", encoding="utf-8").write("".join(out))
    print(a.out)


if __name__ == "__main__":
    main()
