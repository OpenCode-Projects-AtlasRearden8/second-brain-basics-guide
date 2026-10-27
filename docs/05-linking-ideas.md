# Linking Ideas: The Little Web

> A note that connects to nothing is a stone. A note linked to two others
> is a conversation. Ten linked notes are a second brain starting to hum.

Plain files become powerful the moment they point at each other. This
chapter shows the smallest possible way to do that: **wiki-style links**,
written as `[[something]]`, in any editor, with zero setup.

## What a wiki-link looks like

Anywhere in a note, write the title of another note in double brackets:

```text
Read [[the-four-corners]] before the [[monthly-tidy]].
```

When the files are served as HTML by this manual's build system, those
double brackets become real, clickable links between the pages. In
Obsidian or Zettlr, typing `[[` pops up suggestions from your vault as you
type. In Notepad they are just text that your *eyes* (and Ctrl+F) can
follow. All three behaviors are correct. The format is durable either way.

## Two kinds of links, one habit

### 1. Links that point *at real notes*

```text
[[2026-10-27]]  ← links to the daily landing pad for that day
[[pharmacy-refill-loop]] ← links to a note you have or will write
```

### 2. Links that "point at notes you have not written yet"

This is the trick that feels like magic. You can write
`[[evergreen-note]]` knowing no file has that name yet. You have then made
a **promise**: there is a page with that title, and past-you wrote a
sentence pointing at it. When you later write that note — even months
later, out of the blue — the link lights up. This is the cheapest most
people ever pay for a "knowledge graph."

## Why links beat tags for connecting

From the [[tags-vs-folders]] chapter: tags describe; links **connect**.
A wiki-link remembers *context*: the sentence around it says *why* you
linked. Six months later you do not just find related notes — you find
your *thinking* about why they are related. That is the part worth gold.

## Building a note that wants to be a hub

The most powerful pattern in this manual costs eleven words:

> When a new idea arrives, write it, then ask: *what does this remind me
> of?*

Then add 1–3 links. Over weeks, some notes naturally accumulate links and
become **hub notes** (sometimes called "maps of content" or "index notes").
A hub note is just a page with a list:

```text
# Projects hub
- [[2026-11-kdp-paperback]] — the book checklist
- [[shift-handover-tool]] — nursing + automation crossover idea
- [[investment-calm-plan]] — the boring-account setup
```

Keep 2–4 hub notes for the big areas of life (Work, Health/Life, Creations,
Learning). They are handrails; you will use them on tired days instead of
searching.

## Honest do's and do-nots

- **Do** link freely, even lazily. A broken-but-promising link is fine.
- **Do** keep link titles short and stable ([[monthly-tidy]] covers the
  style) — stable titles make links survive renames.
- **Do not** fear orphan notes (notes with no links). Some are just
  receipts, and receipts are fine.
- **Do not** try to build a "system" of links before writing lots of
  notes. Links grow downward like roots, not up like scaffolding.

## Do this now (4 minutes)

Open today's daily note. Write two `[[links]]` to anything — one to a note
that exists, one to a note that does not yet. That second link is your
first promise, and the whole web starts from there.
