Review the draft specification for these points before approval:

1. Define the scoring scale and concrete anchors for faithfulness,
   coverage, and uncertainty/usefulness. If using 0–4, state:
   normalized score =
   (0.40 × faithfulness + 0.35 × coverage +
    0.25 × uncertainty/usefulness) / 4.

2. Define which cases receive semantic scores. Cases expecting input
   rejection or insufficient-evidence handling must have their own
   deterministic expected outcomes.

3. Define the semantic-case denominator and round the required 90%
   pass count upward. Service failures must not be silently excluded
   or counted as passes.

4. Clarify that unsupported claims cause overall failure as a mandatory
   grounding rule, rather than being tolerated by the 90% allowance.

5. Confirm that typed failure results describe observable application
   errors. Semantic evaluation results belong in the harness report;
   do not require the application to judge its own semantic correctness.

6. Require at least 15 varied evaluation cases, rather than exactly 15,
   so additional useful cases are allowed.

Keep the application simple. Preserve the current draft, save the
revised specification and checklist with timestamps, and summarize
changes. Do not approve, implement, or generate my narrative log.
