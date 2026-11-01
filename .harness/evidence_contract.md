# Evaluation evidence contract

Each run writes `evidence/evaluation-results/<run_id>/run.json`.

The record must include:

- `run_id`, `mode` (`offline-mock` or `live-external-powershell`), timestamp,
  dataset version, and SHA-256 hash;
- sanitized model configuration, ceilings, `reasoning.effort`, and retry count;
- every `case_id` and category, with input/fixture path or hash;
- application result/output path or hash, structural and property gates;
- judge request context/result path or hash for semantic cases only;
- semantic scores, unsupported-claim findings, failures, `N_semantic`, required
  integer-ceiling pass count, mandatory failures, and aggregate PASS/FAIL.

Offline-mock runs are labeled as offline and cannot establish authentication,
generation access, billing, or live evaluation evidence. Live runs are allowed
only after dataset approval/freeze and only from the external PowerShell
workflow in `quickstart.md`. Secrets and authorization headers are never
written to evidence.

