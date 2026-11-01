Before I approve the Part-1B plan, verify and summarize:

1. The exact application model and judge model proposed.
2. How unsupported claims are detected and how any such finding
   forces overall FAIL under the approved specification.
3. How malformed judge output, judge-call failure, and application-call
   failure are handled without silently excluding cases.
4. The expected number of model calls for the dataset, including
   retry limits, and an estimated maximum evaluation cost.
5. How raw application outputs, judge responses, rubric versions,
   model settings and per-case results are preserved.

Keep schema and deterministic property checks independent of the judge.
Explain the judge's limitations; do not claim it guarantees correctness.

Verify that API access is configured without printing credentials.
Do not make model calls, change approved thresholds, or implement code.
Preserve any plan corrections and report whether it is ready for approval.

@d:\Ajay\WILP\Sem1\AI Augmented SDLC\Lab\Assignment\AI SDLC- Assignment\Part-1A\evidence\harness-log.md
