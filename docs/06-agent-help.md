# Optional: Agent Help from Your Notes

> Your vault is plain files on your own computer. That means a local AI
> agent — running with your permission, on your machine — can read and tidy
> them *with* you. This is optional. The manual works with zero AI.

Everything before this chapter works with nothing but a folder. This
chapter is for when you are curious about letting an **AI agent** help —
safely, with your notes staying yours.

## How agent help works, in plain English

Modern AI assistants can use **tools** through a protocol called
**Model Context Protocol (MCP)** — see the [[glossary]]. An "MCP server"
is a small program that exposes specific abilities (read your notes,
search them, move files) to the assistant. You run it locally; your files
never leave your machine unless the model itself is remote.

For a notebook-like vault, a minimal **notes-mcp-server** typically offers:

- `search_notes` — find notes matching words (filenames + contents)
- `read_note` — open one note's text
- `list_recent` — show the newest notes (handy for the monthly tidy)
- `summarize_inbox` — a quick digest of what is sitting in `00-inbox/`
- `move_note` — file a note into the right corner, only with your
  confirmation

That is a *lot* of cleanup power for five small tools.

## What agents are actually good at here

- **Sorting the inbox.** "Here are the five newest notes in my inbox —
  suggest a destination corner and a better name for each." You approve or
  reject each suggestion. That is the monthly tidy, on a Tuesday, at half
  speed.
- **Writing hub notes.** "List every note from the last three months and
  cluster them by theme" — the raw material for [[linking-ideas]] hubs.
- **Finding gaps.** "Which notes promise `[[links]]` that do not exist
  yet?" A tidy list of your best unwritten next steps.
- **Plain-English recall.** "What did I write in October about handovers?"
  without opening six files.

## The rules of engagement (non-negotiable)

1. **Read-only by default.** Until you trust a setup completely, agent
   tools should look, not touch.
2. **You confirm every write.** Move, rename, update — you are the gate.
3. **Nothing leaves your machine.** Prefer a *local* model (a small model
   running on-device) or an assistant configured so your notes are not
   uploaded to train anything. Check the settings; they matter.
4. **Backups come first.** Before any agent gets write access, make a copy
   of the vault. A copy costs ten seconds and guarantees a bad session is
   undoable.
5. **Secrets stay out.** Never keep passwords, client details, or patient
   information in notes an agent might read. For healthcare workers this is
   the hard rule: use the vault for *education and thinking*, never for
   identifiable clinical information. (This whole manual is education, not
   medical advice — see the README.)

## A fifteen-line "agent brief" prompt

Keep this in your vault as `templates/agent-brief.md` and paste it before
asking for help. It keeps any assistant polite and on-task:

```text
You are helping me tidy a personal knowledge vault.
- Only use tools on files inside the vault folder.
- Never delete anything without asking me first.
- Prefer suggesting renames/moves over doing them; wait for my OK.
- Keep every name boring and searchable (date-first or type-topic).
- If uncertain where a note belongs, say so rather than guess.
- Summarize bold and briefly; no long lectures.
- Tell me if a task would be faster done by hand.
```

## Do this now (optional, 0–10 minutes)

- **Skip it:** totally fine — the manual is complete without agents.
- **Try it lightly:** if you already have an MCP-enabled assistant, ask it
  one read-only question: "List the five newest notes in my inbox with a
  one-line summary of each." That is agent help at its most honest: small,
  local, and telling you things you half-knew, faster.
