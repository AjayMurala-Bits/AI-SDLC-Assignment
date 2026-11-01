# Evidence Preservation

This directory preserves workflow prompts, generated artifacts, and explicit
approvals. Each capture records the actual capture time in ISO 8601 with the
Asia/Kolkata offset (`+05:30`). Capture time is distinct from an earlier event
time; when only a date is known, the event time is recorded as `exact time not
recorded`.

Future Spec Kit steps MUST use a new timestamped folder and MUST preserve the
exact supplied prompt, generated artifacts, and any explicit approval. Existing
evidence MUST NOT be overwritten.

Implementation snapshots belong in `../initial-generation/` before repair and
in `../final-generation/` after completion. Harness runs belong in a new folder
under `../harness-results/`, with timestamps, commands, exit codes,
stdout/stderr, and PASS/FAIL. `../harness-log.md` is reserved for the
student-authored narrative and is not populated by this setup.
