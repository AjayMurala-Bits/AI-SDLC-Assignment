# AI Movie Review Summarizer Problem Statement

## Purpose

Help a movie viewer understand a small collection of reviews without reading every review in full.

## Problem statement

Build a simple Python command-line application that reads user-supplied movie reviews from a local text file and uses an AI model to produce a short, structured summary. The result describes the overall sentiment, positive and negative aspects mentioned in the reviews, and a brief recommendation based only on the supplied reviews. The application must not invent movie details or follow instructions embedded in review text.

## Minimal scope

- One movie per input file; users supply the review text themselves.
- One summarization request to an AI model per invocation.
- Structured JSON output with a summary, overall sentiment, positive aspects, negative aspects, and recommendation.
- Sentiment labels: positive, negative, mixed, or unclear.
- Concise output grounded in the supplied reviews; empty aspect lists are allowed when unsupported.
- Clear handling of empty input, irrelevant text, insufficient evidence, malformed output and model/service failures.
- Review text is untrusted data, not instructions to the application.
- No website, review scraping, login, database, booking integration or automatic actions.

## Why this is Part 1B

The model runs inside the application. Its wording may vary for the same input, so evaluation must check acceptable meaning and constraints rather than exact wording.

## Evaluation approach

Before implementation, specify the JSON schema, mandatory behavioural and safety rules, and measurable quality rubric and acceptance thresholds. Use one evaluation harness with structural, property and semantic checks. Keep independent structural and property checks even if an AI judge is chosen later.

Prepare 15 varied cases as a practical target, including positive, negative and mixed reviews; conflicting opinions; missing or irrelevant content; and embedded adversarial instructions. Record expected properties or a quality rubric for each case. Distinguish model/service failures from application and evaluation failures.

## Workflow and evidence

Follow constitution, specification, clarification, plan, tasks, analysis, implementation, evaluation, repair and human decision. Preserve real prompts, outputs, configuration, timestamps, initial/final generations and evaluation results. Do not fabricate failures or lower acceptance thresholds after seeing results. Never include API keys in source or evidence. The student authors assessed narrative logs and reflections.

## Pending decisions

The model provider and access method will be selected during planning. Detailed schema, input limits, ambiguity handling and evaluation thresholds belong in the specification. No implementation, model invocation, evaluation or approval is claimed by this document.

## Status

Draft problem statement for student review. AI Movie Review Summarizer was selected in conversation on 2026-11-01. Exact selection time was not recorded.
