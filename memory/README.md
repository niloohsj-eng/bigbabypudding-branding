# Memory snapshot

This folder snapshots the Claude Code memory files for the @bigbabypudding project. Committed so the brand decisions travel with the repo and survive moves between machines.

## Files

- `feedback_bigbabypudding_palette.md` — locked palette, fonts, caption voice, illustration direction, and the locked wafer spec. The source of truth for all design decisions.
- `MEMORY_bigbaby_section.md` — the Big Baby section extracted from the master `MEMORY.md` index (project status, file paths, recent decisions).

## Restoring on a new computer

Two options:

### Option 1 — Restore into Claude's memory (recommended)

So Claude automatically loads these on the new machine:

```bash
# After cloning the repo
mkdir -p ~/.claude/projects/-Users-amir/memory
cp memory/feedback_bigbabypudding_palette.md ~/.claude/projects/-Users-amir/memory/

# Append the Big Baby section into the master MEMORY.md index
# (or create MEMORY.md if it doesn't exist yet)
cat memory/MEMORY_bigbaby_section.md >> ~/.claude/projects/-Users-amir/memory/MEMORY.md
```

### Option 2 — Just reference them

If you don't want to wire into Claude's memory system, point Claude at this folder when you start a new conversation: *"read memory/feedback_bigbabypudding_palette.md before we begin."*

## Keeping in sync

When new design decisions get locked, this folder won't auto-update — re-run the copy commands above (in reverse) to refresh the snapshot before committing:

```bash
cp ~/.claude/projects/-Users-amir/memory/feedback_bigbabypudding_palette.md memory/
```
