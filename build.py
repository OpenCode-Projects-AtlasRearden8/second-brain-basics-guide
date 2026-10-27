#!/usr/bin/env python3
"""Build docs/ Markdown into a static HTML site using only the stdlib."""

import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
STARTER = ROOT / "starter"

CSS = """
:root { --ink:#2b2a27; --soft:#6b675e; --paper:#faf8f4; --card:#fff;
  --line:#e5e1d8; --accent:#0f6b5c; --accent-soft:#e7f2ef; --code:#f1eee7; }
* { box-sizing:border-box; }
body { margin:0; font:17px/1.65 Georgia,'Times New Roman',serif;
  color:var(--ink); background:var(--paper); }
.wrap { max-width:960px; margin:0 auto; padding:2.5rem 1.5rem 4rem; }
header.site { border-bottom:1px solid var(--line); padding-bottom:.75rem;
  margin-bottom:2.5rem; }
header.site .brand { font-size:1rem; letter-spacing:.02em;
  color:var(--soft); text-decoration:none; }
header.site .brand strong { color:var(--accent); }
nav.chapters { font-size:.92rem; margin-top:1rem; display:flex;
  flex-wrap:wrap; gap:.4rem 1.1rem;
  font-family:'Segoe UI',system-ui,sans-serif; }
nav.chapters a { color:var(--soft); text-decoration:none;
  border-bottom:2px solid transparent; }
nav.chapters a:hover, nav.chapters a.active { color:var(--ink);
  border-bottom-color:var(--accent); }
h1, h2, h3 { font-family:'Avenir Next','Segoe UI',system-ui,sans-serif;
  line-height:1.25; }
h1 { font-size:2.1rem; margin:.2rem 0 2rem; }
h2 { font-size:1.4rem; margin:2.2rem 0 .6rem; }
h3 { font-size:1.15rem; margin:1.8rem 0 .5rem; }
p, li { max-width:70ch; }
a { color:var(--accent); }
blockquote { margin:1.5rem 0; padding:.9rem 1.2rem;
  border-left:4px solid var(--accent); background:var(--accent-soft);
  border-radius:0 8px 8px 0; font-style:italic; }
blockquote p { margin:0; }
code { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.88em;
  background:var(--code); padding:.1em .35em; border-radius:4px; }
pre { background:var(--code); padding:.9rem 1.1rem; border-radius:8px;
  overflow-x:auto; line-height:1.5; }
pre code { background:none; padding:0; }
table { border-collapse:collapse; width:100%; margin:1.2rem 0;
  font-size:.95rem; }
th, td { border:1px solid var(--line); padding:.45rem .7rem;
  text-align:left; vertical-align:top; }
th { background:var(--code); }
li { margin:.3rem 0; }
hr { border:0; border-top:1px solid var(--line); margin:2.5rem 0; }
.promised { color:var(--soft); font-style:italic; }
footer.foot { margin-top:3rem; padding-top:1rem;
  border-top:1px solid var(--line); color:var(--soft); font-size:.9rem;
  font-family:'Segoe UI',system-ui,sans-serif; }
.pagenav { display:flex; justify-content:space-between; gap:1rem;
  margin-top:3rem; font-family:'Segoe UI',system-ui,sans-serif;
  font-size:.95rem; }
.pagenav a { text-decoration:none; }
.card { background:var(--card); border:1px solid var(--line);
  border-radius:10px; padding:1.3rem 1.6rem; margin:1.2rem 0; }
.chapterlist li { border-bottom:1px dashed var(--line);
  padding:.5rem 0; margin:0; }
.chapterlist a { text-decoration:none; font-weight:600; }
"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Second Brain Basics</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
<header class="site">
  <a class="brand" href="index.html"><strong>Second Brain Basics</strong> —
   a plain-file personal knowledge base</a>
  <nav class="chapters">{nav}</nav>
</header>
{body}
<footer class="foot">
  Second Brain Basics · MIT License · Copyright (c) 2026 Asdale Dynamics, LLC
</footer>
</div>
</body>
</html>
"""


def slugify(text):
    text = re.sub(r"\s+", "-", text.strip().lower())
    return re.sub(r"[^a-z0-9-]", "", text)


def page_slug(path):
    return re.sub(r"^\d+-", "", Path(path).stem)


def strip_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def read_docs():
    docs = {}
    for path in sorted(DOCS.glob("*.md")):
        slug = page_slug(path)
        raw = strip_front_matter(path.read_text(encoding="utf-8"))
        m = re.search(r"^# (.+)$", raw, re.M)
        title = m.group(1).strip() if m else slug
        terms = []
        if slug == "glossary":
            for term in re.findall(r"^### (.+)$", raw, re.M):
                terms.append(term_slug(term))
        docs[slug] = {"source": path, "raw": raw, "title": title,
                      "terms": terms}
    return docs


def term_slug(heading):
    return slugify(heading.split(" (")[0])


def inline(text):
    codes = []

    def keep(m):
        codes.append(html.escape(m.group(1)))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    for i, code in enumerate(codes):
        text = text.replace(f"\x00{i}\x00", f"<code>{code}</code>")
    return text


def resolve_wiki_links(text, doc_map, glossary_terms):
    codes = []

    def keep(m):
        codes.append(m.group(0))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`[^`]+`", keep, text)

    def repl(m):
        target = m.group(1).strip()
        if target in doc_map:
            return f'<a href="{target}.html">{target.replace("-", " ")}</a>'
        if target.lower() in glossary_terms:
            return (f'<a href="glossary.html#{target.lower()}">'
                    f'{target.replace("-", " ")}</a>')
        return f'<span class="promised">[[{target}]]</span>'

    text = re.sub(r"\[\[(\S[^\]]*?)\]\]", repl, text)
    for i, code in enumerate(codes):
        text = text.replace(f"\x00{i}\x00", code)
    return text


def markdown_to_html(text, doc_map, glossary_terms):
    text = resolve_wiki_links(text, doc_map, glossary_terms)
    lines = text.split("\n")
    out = []
    i = 0
    structure_re = re.compile(
        r"^(```|<!--|(-{3,}|\*{3,})\s*$|#{1,4}\s|>|\||(-|\*|\+|\d+\.)\s+)")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(code) + "</code></pre>")
            continue
        if line.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", line.strip()):
            out.append("<hr>")
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, content = len(m.group(1)), m.group(2)
            id_attr = ""
            slugged = term_slug(content) if level == 3 else slugify(content)
            if level in (1, 2) or slugged in glossary_terms:
                id_attr = f' id="{slugged}"'
            out.append(f"<h{level}{id_attr}>{inline(content)}</h{level}>")
            i += 1
            continue
        if line.lstrip().startswith(">"):
            quote = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>"
                       + markdown_to_html("\n".join(quote), {}, set())
                       + "</blockquote>")
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            parsed = []
            for r in rows:
                cells = [c.strip() for c in r.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    continue
                parsed.append(cells)
            html_rows = ["<table>"]
            if parsed:
                html_rows.append("<thead><tr>"
                    + "".join(f"<th>{inline(c)}</th>" for c in parsed[0])
                    + "</tr></thead><tbody>")
                for r in parsed[1:]:
                    html_rows.append("<tr>"
                        + "".join(f"<td>{inline(c)}</td>" for c in r)
                        + "</tr>")
                html_rows.append("</tbody>")
            html_rows.append("</table>")
            out.append("\n".join(html_rows))
            continue
        m = re.match(r"^(-|\*|\+|\d+\.)\s+", line)
        if m:
            ordered = re.match(r"^\d+\.", line)
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                l2 = lines[i]
                if l2.startswith("  ") and not re.match(r"\S", l2.lstrip() or " "):
                    break
                if not ordered and re.match(r"^(-|\*|\+)\s+", l2):
                    items.append(inline(re.sub(r"^(-|\*|\+)\s+", "", l2)))
                    i += 1
                elif ordered and re.match(r"^\d+\.\s+", l2):
                    items.append(inline(re.sub(r"^\d+\.\s+", "", l2)))
                    i += 1
                else:
                    break
            out.append(f"<{tag}>"
                       + "".join(f"<li>{it}</li>" for it in items)
                       + f"</{tag}>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not structure_re.match(lines[i]):
            para.append(lines[i])
            i += 1
        out.append("<p>" + "<br>\n".join(inline(p) for p in para) + "</p>")
    return "\n".join(out)


def build(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = read_docs()
    order = sorted(docs, key=lambda s: docs[s]["source"].name)
    titles = {s: docs[s]["title"] for s in order}
    glossary_terms = {t for s in order for t in docs[s]["terms"]}

    for idx, slug in enumerate(order):
        doc = docs[slug]
        body = markdown_to_html(doc["raw"], titles, glossary_terms)
        nav = " | ".join(
            f'<a href="{s}.html" class="active">{t}</a>' if s == slug
            else f'<a href="{s}.html">{t}</a>'
            for s, t in titles.items())
        prev = (f'<a href="{order[idx - 1]}.html">← '
                f'{titles[order[idx - 1]]}</a>') if idx > 0 else "<span></span>"
        nxt = (f'<a href="{order[idx + 1]}.html">{titles[order[idx + 1]]} →</a>'
               ) if idx < len(order) - 1 else "<span></span>"
        body += f'<div class="pagenav">{prev}{nxt}</div>'
        page = SHELL.format(css=CSS, nav=nav, body=body, title=doc["title"])
        (out_dir / f"{slug}.html").write_text(page, encoding="utf-8")

    navlinks = " | ".join(f'<a href="{s}.html">{t}</a>'
                          for s, t in titles.items())
    chapter_list = "".join(
        f'<li><a href="{slug}.html">{titles[slug]}</a></li>'
        for slug in order)
    intro = f"""<h1>Second Brain Basics</h1>
<p>A manual for a personal knowledge base made of <strong>plain files</strong> —
no fancy apps required, nothing to subscribe to, nothing that locks you in.
Written for busy people, in plain friendly English, one small step at a time.</p>
<div class="card">
<p><strong>Read it in order:</strong></p>
<ol class="chapterlist">{chapter_list}</ol>
</div>
<p>Every chapter stands alone and ends with a tiny “do this now” step, each
one under five minutes. The starter vault template lives in
<code>starter/</code> — copy it, rename it, open any editor, and you are
running.</p>
<p><strong>Run locally:</strong> this whole site is pre-built, and you can
rebuild it any time with <code>python3 build.py</code>.</p>"""
    index = SHELL.format(css=CSS, nav=navlinks, body=intro, title="Home")
    (out_dir / "index.html").write_text(index, encoding="utf-8")

    starter_out = out_dir / "starter"
    if starter_out.exists():
        shutil.rmtree(starter_out)
    if STARTER.exists():
        shutil.copytree(STARTER, starter_out)
    return sorted(p.name for p in out_dir.glob("*.html"))


def main():
    args = sys.argv[1:]
    out = "site"
    if args and args[0] == "--out":
        out = args[1] if len(args) > 1 else "site"
    pages = build(out)
    print(f"Built {len(pages)} pages into {out}/")


if __name__ == "__main__":
    main()
