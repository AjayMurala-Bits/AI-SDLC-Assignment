# Ruff repair diff

- Repair capture start: 2026-10-31T20:37:48.370+05:30 (Asia/Kolkata)
- Repair capture end: 2026-10-31T20:38:14.353+05:30 (Asia/Kolkata)
- Source/test behaviour and approved requirements were not changed.

`src/movie_booking/__main__.py`

- Removed one excess blank line between the import and the module entry-point guard.

`src/movie_booking/cli.py`

- Changed `Sequence` import from `typing` to `collections.abc`, as required by Ruff UP035.

`tests/test_booking.py`

- Combined `subTest` and `assertRaises` into one context manager, resolving SIM117.

`tests/test_storage.py`

- Combined `TemporaryDirectory` and `assertRaises` into one context manager, resolving SIM117.

Before and after files are preserved in the sibling `before/` and `after/` folders. The initial-generation snapshot and the earlier failed harness result were not modified.
