#!/usr/bin/env python3
"""Build the book PDF from the Markdown chapters.

Setup (once):   python3 -m venv .venv && .venv/bin/pip install markdown
Run:            .venv/bin/python tools/make_diagrams.py && .venv/bin/python tools/build_pdf.py
Needs Google Chrome or Chromium on PATH (used headless to print the PDF).
"""
import glob, os, re, shutil, subprocess, sys, tempfile
import markdown

BOOK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(BOOK, "Secure_Coding_FE_BE_AI_Agent_Era.pdf")

CSS = """
@page { size: A4; margin: 17mm 15mm 18mm 15mm;
        @bottom-center { content: counter(page); font: 8.5pt 'DejaVu Sans', sans-serif; color: #5b6b79; } }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', Verdana, Arial, sans-serif; font-size: 9.8pt; line-height: 1.55; color: #1a1a1a; }
section.chapter { break-before: page; }
section.cover { height: 235mm; display: flex; flex-direction: column; justify-content: center; }
section.cover h1 { font-size: 34pt; border: 0; margin: 0 0 6px 0; }
section.cover .bar { height: 5px; width: 110px; background: #1b8a9a; margin: 10px 0 18px 0; }
section.cover .sub { font-size: 15pt; color: #1b6f8a; margin: 0 0 22px 0; }
section.cover p { margin: 6px 0; }
section.cover .meta { color: #5b6b79; font-size: 9pt; margin-top: 26px; }
h1 { font-size: 21pt; color: #12304a; border-bottom: 3px solid #1b8a9a; padding-bottom: 6px; margin: 0 0 12px 0; }
h2 { font-size: 13.5pt; color: #1b6f8a; margin: 20px 0 6px 0; break-after: avoid; }
h3 { font-size: 11pt; color: #12304a; margin: 14px 0 4px 0; break-after: avoid; }
p { margin: 6px 0; }
a { color: #1b6f8a; }
hr { border: 0; border-top: 1px solid #d5dde3; margin: 14px 0; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8.8pt; }
tr { break-inside: avoid; }
th { background: #12304a; color: #fff; text-align: left; padding: 5px 7px; }
td { border: 1px solid #d5dde3; padding: 5px 7px; vertical-align: top; }
tr:nth-child(even) td { background: #f4f8fa; }
code { background: #eef2f5; padding: 1px 4px; border-radius: 3px; font-family: 'DejaVu Sans Mono', monospace; font-size: 8.6pt; }
pre { background: #f4f7f9; border: 1px solid #dde4ea; border-radius: 6px; padding: 8px 10px; break-inside: avoid; white-space: pre-wrap; }
pre code { background: none; padding: 0; font-size: 8.3pt; }
blockquote { margin: 10px 0; padding: 7px 12px; border-left: 4px solid #5b6b79; background: #f4f6f8; border-radius: 4px; break-inside: avoid; }
blockquote p { margin: 4px 0; }
blockquote.goal { background: #e6f3f7; border-color: #1b8a9a; }
blockquote.analogy { background: #fdf3e0; border-color: #c77d0a; }
blockquote.case { background: #f1ecf8; border-color: #6b4fa0; }
blockquote.mistake { background: #fbeaea; border-color: #c0392b; }
blockquote.interview { background: #e7f5ec; border-color: #2e8b57; }
img { display: block; max-width: 100%; margin: 10px auto; border: 1px solid #e3e8ec; border-radius: 6px; break-inside: avoid; }
"""

KIND = [("Goal", "goal"), ("Not a goal", "goal"), ("Why labs", "goal"), ("Legal rule", "goal"), ("Rule zero", "goal"),
        ("Definition of done", "goal"), ("How to drill", "goal"), ("Analogy", "analogy"), ("Real case", "case"),
        ("AI-agent era", "case"), ("Common mistake", "mistake"), ("Interview angle", "interview")]


def kind(label):
    for prefix, cls in KIND:
        if label.startswith(prefix):
            return cls
    return ""


NAMES = {"00": "Start here", "09": "Interview Q&A", "10": "Cheat sheets", "11": "Labs", "12": "Sources"}


def link_text(m):
    n = m.group(1)
    return "[%s]" % NAMES.get(n, "Chapter %d" % int(n))


def render(md_text, stem):
    md_text = re.sub(r"\[(\d\d)-[\w-]+\.md\]", link_text, md_text)                  # [NN-name.md] -> [Chapter N]
    md_text = re.sub(r"(\n>[^\n]*)\n\n(> \*\*)", r"\1\n\n<!-- split -->\n\n\2", md_text)  # keep callouts separate
    md_text = re.sub(r"\]\((\d\d-[\w-]+)\.md#([\w-]+)\)", r"](#\2)", md_text)      # file.md#anchor -> #anchor
    md_text = re.sub(r"\]\((\d\d-[\w-]+)\.md\)", r"](#chap-\1)", md_text)           # file.md -> chapter section
    html = markdown.markdown(md_text, extensions=["tables", "sane_lists", "fenced_code", "toc"])
    html = re.sub(r"<blockquote>(\s*<p><strong>([^<]*)</strong>)",
                  lambda m: '<blockquote class="%s">%s' % (kind(m.group(2)), m.group(1)), html)
    return '<section class="chapter" id="chap-%s">%s</section>' % (stem, html)


def main():
    files = sorted(glob.glob(os.path.join(BOOK, "[0-9][0-9]-*.md")))
    body = ['<section class="cover"><h1>Secure Coding for Frontend and Backend Engineers</h1><div class="bar"></div>'
            '<p class="sub">AI-Agent-Era Edition, 2026</p>'
            '<p>A compact interview book for engineers who build web apps and APIs, and who write code with AI agents. The bugs you create or prevent in a pull request, plus how to use coding agents without giving attackers your tokens, your laptop or your pipeline.</p>'
            '<p>Browser and HTTP security &middot; identity and access &middot; injection &middot; supply chain and CI &middot; using coding agents safely &middot; building AI features &middot; code-review drill &middot; 45 interview questions &middot; labs.</p>'
            '<p class="meta">See the last chapter for sources and accuracy notes. Written 18 November 2026.</p></section>']
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        body.append(render(open(f, encoding="utf-8").read(), stem))
    html = ('<!doctype html><meta charset="utf-8"><title>Secure Coding for FE and BE Engineers (AI-Agent Era)</title>'
            '<base href="file://%s/"><style>%s</style>%s' % (BOOK, CSS, "".join(body)))

    ids = set(re.findall(r'id="([^"]+)"', html))
    missing = sorted({h for h in re.findall(r'href="#([^"]+)"', html) if h not in ids})
    if missing:
        print("WARNING: links with no target:", missing)
    srcs = set(re.findall(r'<img[^>]+src="([^"]+)"', html))
    absent = sorted(s for s in srcs if not os.path.exists(os.path.join(BOOK, s)))
    if absent:
        print("WARNING: missing images:", absent)

    chrome = next((shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    if not chrome:
        sys.exit("Chrome/Chromium not found on PATH")
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "book.html")
        open(page, "w", encoding="utf-8").write(html)
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=" + OUT, "file://" + page], check=True, capture_output=True)
    print("wrote", OUT, "(%d KB)" % (os.path.getsize(OUT) // 1024))


if __name__ == "__main__":
    main()
