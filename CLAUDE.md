# Notes for Claude sessions

## Backups and scratch files stay out of the home folder

- Before a risky change to the stores, back them up to `backups/<yyyy-mm-dd>-<label>/` in this
  repo (gitignored), not `C:\Users\kk\ontario-db-backup-*`. Older notes in `TODO-archive/` (and
  a few in TODO.md) and tool docstrings name home-folder backups; that was the old habit, not a
  place to keep writing to.
- Once the change is verified, backups older than a week can go.
- Throwaway scripts go in the session's scratchpad, never in a new folder under `C:\Users\kk`.

## TODO.md holds open items only

- TODO.md is the operator's list of **open** items. Keep it short (well under 60 KB).
- When an item is done, move its text verbatim to `TODO-archive/` (the section's file, or a new
  `TODO-archive/<yyyy-mm-dd>-<slug>.md`) and leave TODO.md linking there. Don't leave it
  ticked in place, and don't append dated history to TODO.md.
- `TODO.md §N` references (in TOMLs, skills, TODO-skills.md) resolve through the section
  headings, which stay, each linking its archive file. Keep the section numbers.
