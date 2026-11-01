# Sanitized model-access diagnostic

- Capture timestamp: 2026-11-01T13:40:54.837+05:30 (Asia/Kolkata)
- Request: read-only `GET /v1/models`
- HTTP status: `401`
- `gpt-5.4-mini` accessible: `false`
- Credential values, authorization headers, and credential-bearing error
  bodies: not read or recorded.
- Generation calls: none.
- Plan approval: not recorded.

## Model capability verification

The official GPT-5.4 Mini model documentation lists support for
`reasoning.effort`, including `none`. This was verified from documentation,
not by making a model call.

Official reference:
https://developers.openai.com/api/docs/models/gpt-5.4-mini
