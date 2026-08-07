# CLAUDE.md — Claude Code Entry Point

@AGENTS.md

## Claude Code Notes

The shared rules for this project live in `AGENTS.md` (imported above) so they stay
in sync across every AI tool used on this repo, not just Claude Code. Add Claude
Code–specific notes here — don't duplicate anything already covered in `AGENTS.md`.

- When a branching decision (see the Decision-Making Protocol in `AGENTS.md`)
  involves a schema or architecture change, consider using plan mode first so the
  plan can be reviewed before any file is touched.
- If this file and `AGENTS.md` ever disagree, `AGENTS.md` is the source of truth —
  fix the conflict there, not here.

> Note: Claude Code does not read `AGENTS.md` automatically — the `@AGENTS.md` line
> above is what pulls it in. Keep that import at the top of this file.
