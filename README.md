# Second Brain Basics

A warm, tested manual for a **personal knowledge base made of plain files** —
no fancy apps required. Fleeting notes, project notes, an archive, and a
daily landing pad, plus naming that survives years, honest tags-vs-folders
advice, free editor options, wiki-style linking, optional agent help from a
local notes MCP server, and a monthly fifteen-minute tidy.

Built for beginners in plain, friendly English. Every chapter stands alone
and ends with a small "do this now" step of under five minutes.

## What is in here

```text
docs/        the manual, chapter by chapter (Markdown)
starter/     a ready-to-copy vault folder template with entry-type templates
site/        the static HTML version of the manual (built by build.py)
build.py     converts docs/ into the site/ folder — Python stdlib only
tests/       test suite: python3 -m unittest discover tests
LICENSE      MIT · Copyright (c) 2026 Asdale Dynamics, LLC
STATUS.md    what was built, how to run it, verification results, gaps
```

## Quick start

1. Read `docs/00-start-here.md` in any editor — it is plain text.
2. Copy the `starter/` folder somewhere comfortable, rename it, done.
3. Want the polished reading version? Open `site/index.html` in a browser,
   or rebuild it locally:

```bash
python3 build.py              # builds ./site (Markdown -> HTML)
python3 -m unittest discover tests -v   # runs the test suite
```

Everything is local-first: your notes stay in your folder, in .md/.txt
format, openable by any editor on any system, forever. Nothing here phones
home. No secrets, keys, or personal data live in this repository.

## Optional: agent help

`docs/06-agent-help.md` explains how a local AI assistant (via a
notes-mcp-server using MCP) can read and tidy your vault — read-only
tools, your confirmation on every write, and an "agent brief" template
included in `starter/templates/agent-brief.md`. The whole manual works
with zero AI, and the chapter is designed that way on purpose.

## Audience and spirit

Written as beginner-friendly education by **Asdale Dynamics, LLC** — plain
English, step by step, never condescending. This is an education manual;
it is not medical advice, even though healthcare workers are warmly
welcomed as readers. Low-energy friendly by design: the monthly tidy is
fifteen minutes timer-capped, and there is an explicit two-minute version
for bad months.

## License

MIT License — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.
