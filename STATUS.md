# STATUS — Second Brain Basics

## What was built

A complete, local-first manual for a personal knowledge base made of plain
files, plus everything needed to use and rebuild it:

- **Manual (`docs/`, 9 Markdown chapters, ~600 lines):** start here; the
  four corners (fleeting / projects / archive / daily landing pad);
  naming that survives years (ISO dates, type-topic-slice, worked
  examples); tags vs folders compared honestly with a recommended split;
  free editors in three tiers (from Notepad to Obsidian/Zettlr/VS Code);
  wiki-style `[[linking]]` including promise-links and hub notes;
  optional agent help via a notes-mcp-server with non-negotiable rules
  (read-only default, confirm every write, local-first, secrets stay
  out) and a paste-ready agent brief; the monthly fifteen-minute tidy
  with a 2-minute fallback; and an alphabetical plain-English glossary.
  Warm, plain-English, low-energy-friendly tone throughout; every chapter
  ends with a small "do this now" step.
- **Starter vault (`starter/`):** copy-and-rename folder template with
  `00-inbox/`, `10-projects/`, `20-archive/`, `50-hubs/`, `90-daily/`
  (including one filled example daily note dated ISO-style), six
  entry-type templates (`daily-note`, `fleeting-note`, `project-note`,
  `archive-note`, `hub-note`, `agent-brief`), worked example notes, and
  its own README.
- **Static HTML site (`site/`):** a clean, self-contained offline-reading
  site — one page per chapter with navigation, prev/next links, styled
  tables/blockquotes/code, clickable `[[wiki-links]]`, glossary anchors,
  and a homepage index. Built by **`build.py` using only the Python
  standard library** (no pip installs). The built `site/` is committed so
  the manual reads immediately; rebuild any time.
- **Cross-linking:** every `[[wiki-link]]` in the manual resolves to a
  chapter or glossary anchor; unresolved-style "promise" links only
  appear inside fenced code examples.

## How to run it

```bash
python3 build.py                        # rebuild site/ from docs/ (stdlib only)
python3 build.py --out /tmp/preview     # build anywhere else
python3 -m unittest discover tests -v   # full test suite
```

Read the manual as Markdown (`docs/00-start-here.md`) or open
`site/index.html` in any browser. To use the system: copy `starter/`,
rename it, open any editor.

## Verification results

- `python3 -m unittest discover tests` — **15 tests, all passing (OK)**
  after several real fixes made during verification (quote handling, code-
  span protection, glossary anchor slugs, wiki-link resolution rules).
  Coverage includes: every doc builds; no unresolved wiki-links in the
  site; no broken internal links; glossary anchors exist; footer/title on
  every page; CLI build runs clean; source-level wiki-links resolve;
  glossary alphabetical; all six starter templates exist; starter daily
  notes follow the ISO date-name rule; starter wiki-links resolve inside
  the vault; no secret-like strings anywhere; LICENSE contains the exact
  line `Copyright (c) 2026 Asdale Dynamics, LLC`; README credits
  Asdale Dynamics, LLC.
- `python3 build.py` — exits 0, emits 10 HTML pages into `site/`; output
  spot-checked (tables, blockquotes, headings, anchors render correctly).
- `python3 -m py_compile build.py tests/test_build.py` — clean.
- One git commit, plain message, made with the existing repo identity; no
  remote added, nothing pushed or published.

## Known gaps

- The HTML reader is deliberately minimal (single-page-per-chapter); it
  does not include search, a backlinks view, or dark mode.
- No bundled notes-mcp-server implementation yet — `docs/06-agent-help.md`
  specifies the design and safety rules; building the actual MCP server
  would be a natural follow-up for this folder.
- Glossary "backlink" explanation is prose-only; no worked backlink
  example file ships in the starter.
- Site is not localization-ready (English only) and assumes a UTF-8
  editor/terminal.
- `site/` is both committed and rebuildable; that is intentional
  (open-instant, source-of-truth stays `docs/`), but it means the HTML
  must be rebuilt after doc edits to stay in sync — a build check step
  could be added to the tests to enforce that.
