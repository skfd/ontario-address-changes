# Notes for Claude sessions

## Backups and scratch files stay out of the home folder

- Before a risky change to the stores, back them up to `backups/<yyyy-mm-dd>-<label>/` in this
  repo (gitignored), not `C:\Users\kk\ontario-db-backup-*`. Older notes in TODO.md and tool
  docstrings name home-folder backups; that was the old habit, not a place to keep writing to.
- Once the change is verified, backups older than a week can go.
- Throwaway scripts go in the session's scratchpad, never in a new folder under `C:\Users\kk`.
