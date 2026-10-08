#!/usr/bin/env python3
"""
Bands in Bend — build the weekly newsletter HTML from shows.js.

Reads shows.js and newsletter-template.html and writes a ready-to-paste
Custom HTML email for the Sender.net campaign.

    python3 scripts/build_email.py                  # -> drafts/email-<week>.html
    python3 scripts/build_email.py --out /tmp/e.html

Then in Sender: duplicate last week's campaign, update name/subject/preview,
Design -> Edit design, paste into the Ace editor, and **Save and continue**
before doing anything else (Sender's autosave lags; a test or send can
otherwise go out with the previous week's HTML).

Structure rules that must not change (learned the hard way):
  * The entire lineup - radar plus all seven days - lives in ONE full-width
    table. Day headers are colspan=2 rows; every show row is
    [name + venue | time] sharing that table's right-aligned column. Separate
    per-day tables shrink to their own content width and stagger on mobile
    Gmail, and no per-table width/table-layout reliably fixes it.
  * Dark-only color-scheme in the head, not "light dark".
  * Keep the Sender unsubscribe tag and the "shows subject to change" line.
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

READ_SHOWS_JS = (
    "const s=require('fs').readFileSync('shows.js','utf8')"
    "+';module.exports={SHOWS,HIGHLIGHTS,WEEK}';"
    "const m={exports:{}};new Function('module',s)(m);"
    "console.log(JSON.stringify(m.exports))"
)

DISCLAIMER = ('<div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;'
              'color:#6B6560;padding-top:16px;">Shows subject to change — check with '
              'the venue to confirm.</div>')
COPYRIGHT = ('<div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;'
             'color:#6B6560;padding-top:16px;">© 2026 Bands in Bend')


def e(s):
    return html.escape(s or "", quote=False)


def radar_row(h):
    return (f'<tr><td style="padding:7px 0 7px 0;font-family:Arial,Helvetica,sans-serif;'
            f'font-size:15px;color:#F5F0E8;">{e(h["artist"])}</td>'
            f'<td align="right" valign="top" width="96" style="width:96px;padding:9px 0 0 0;'
            f'font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#C4973A;'
            f'white-space:nowrap;">{e(h["day"])}</td></tr>')


def day_header(d):
    return (f'<tr><td colspan="2" style="padding-top:34px;">'
            f'<div style="font-family:Georgia,\'Times New Roman\',serif;font-size:25px;'
            f'font-weight:bold;color:#F5F0E8;">{e(d["day"]).upper()} '
            f'<span style="font-family:Arial,Helvetica,sans-serif;font-size:11px;'
            f'letter-spacing:2px;color:#E8632A;font-weight:normal;">{e(d["date"]).upper()}</span></div>'
            f'<div style="font-size:1px;line-height:1px;height:2px;background-color:#E8632A;'
            f'margin:10px 0 2px;">&nbsp;</div></td></tr>')


def show_row(s):
    return (f'<tr><td style="padding:13px 12px 13px 0;border-bottom:1px solid #2A2825;">'
            f'<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;'
            f'color:#F5F0E8;line-height:1.35;">{e(s["artist"])}</div>'
            f'<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#C4973A;'
            f'padding-top:4px;">{e(s["venue"])}</div></td>'
            f'<td align="right" valign="top" width="58" style="width:58px;padding:15px 0 0 8px;'
            f'border-bottom:1px solid #2A2825;font-family:Arial,Helvetica,sans-serif;'
            f'font-size:13px;color:#A09890;white-space:nowrap;">{e(s["time"])}</td></tr>')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="output path (default: drafts/email-<week>.html)")
    args = ap.parse_args()

    data = json.loads(subprocess.check_output(["node", "-e", READ_SHOWS_JS], cwd=ROOT))
    tpl = open(os.path.join(ROOT, "newsletter-template.html"), encoding="utf-8").read()

    # hero date label
    tpl, n = re.subn(r'(font-size:13px;color:#A09890;">)[^<]*?( &nbsp;·&nbsp; Bend, Oregon)',
                     lambda m: m.group(1) + data["WEEK"]["label"] + m.group(2), tpl, count=1)
    if n != 1:
        raise SystemExit("ERROR: could not find the hero date label in the template.")

    # one full-width table: radar + every day
    start = tpl.index('<tr><td colspan="2"><div style="padding:20px 0 8px 0;')
    end = tpl.index('</tbody></table></td></tr><tr><td align="center" style="padding:36px 0 10px;">')
    rows = ['<tr><td colspan="2"><div style="padding:20px 0 8px 0;font-family:Arial,Helvetica,'
            'sans-serif;font-size:10px;letter-spacing:2px;color:#E8632A;font-weight:bold;">'
            'SHOWS ON OUR RADAR</div></td></tr>']
    rows += [radar_row(h) for h in data["HIGHLIGHTS"]]
    rows.append('<tr><td colspan="2" style="font-size:10px;line-height:10px;;padding:0 0 0 0">'
                '&nbsp;</td></tr>')
    for d in data["SHOWS"]:
        rows.append(day_header(d))
        rows += [show_row(s) for s in d["shows"]]
    tpl = tpl[:start] + "".join(rows) + tpl[end:]

    # required disclaimer, above the copyright line
    if "Shows subject to change" not in tpl:
        if tpl.count(COPYRIGHT) != 1:
            raise SystemExit("ERROR: could not place the disclaimer (copyright line not found).")
        tpl = tpl.replace(COPYRIGHT, DISCLAIMER + COPYRIGHT.replace("padding-top:16px",
                                                                   "padding-top:8px"))

    total = sum(len(d["shows"]) for d in data["SHOWS"])
    written = tpl.count('border-bottom:1px solid #2A2825;"><div')
    if written != total:
        raise SystemExit(f"ERROR: {total} shows in shows.js but {written} rows written.")

    out = args.out or os.path.join(ROOT, "drafts", f"email-{data['WEEK']['label'].replace(' ', '')}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(tpl)

    print(f"week:        {data['WEEK']['label']}")
    print(f"shows:       {total} ({written} rows)")
    print(f"highlights:  {len(data['HIGHLIGHTS'])}")
    dark_meta = tpl.count('content="dark"')
    light_dark = "light dark" in tpl
    has_disc = "Shows subject to change" in tpl
    has_unsub = "{{unsubscribe_text}}" in tpl
    print(f"dark-only:   {dark_meta} meta tags, 'light dark' present: {light_dark}")
    print(f"disclaimer:  {has_disc} | unsubscribe tag: {has_unsub}")
    print(f"wrote:       {out} ({len(tpl)} bytes)")


if __name__ == "__main__":
    main()
