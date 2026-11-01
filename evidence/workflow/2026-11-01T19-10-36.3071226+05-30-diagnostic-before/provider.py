"""Single OpenAI adapter. Credentials are read only from the process environment."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from .schema import success_schema


class ProviderError(RuntimeError):
    """Observable provider failure without exposing credential details."""

    def __init__(self, message: str, diagnostic: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.diagnostic = diagnostic or {"category": "unknown"}


class InvalidProviderOutput(ProviderError):
    """Provider returned content that was not valid JSON."""

    def __init__(self, message: str) -> None:
        super().__init__(message, {"category": "malformed_response"})


def _safe_status_code(exc: BaseException) -> int | None:
    for source in (exc, getattr(exc, "response", None)):
        value = getattr(source, "status_code", None)
        if isinstance(value, int) and 100 <= value <= 599:
            return value
    return None


def _safe_error_code(exc: BaseException) -> str | None:
    candidates: list[Any] = [getattr(exc, "code", None)]
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            candidates.append(error.get("code"))
    for candidate in candidates:
        if isinstance(candidate, str) and re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", candidate):
            return candidate
    return None


def sanitized_provider_diagnostic(exc: BaseException) -> dict[str, Any]:
    """Return category/status/code only; never serialize provider messages or requests."""
    if isinstance(exc, ProviderError) and exc.diagnostic:
        diagnostic = dict(exc.diagnostic)
    else:
        name = type(exc).__name__.lower()
        status = _safe_status_code(exc)
        code = _safe_error_code(exc)
        code_text = (code or "").lower()
        if isinstance(exc, InvalidProviderOutput):
            category = "malformed_response"
        elif "quota" in name or "billing" in name or "quota" in code_text or "billing" in code_text or "insufficient" in code_text or status == 402:
            category = "quota_billing"
        elif status in (401, 403) or "authentication" in name or "permissiondenied" in name or "auth" in code_text:
            category = "authentication"
        elif "ratelimit" in name or "rate_limit" in name or status == 429 or "rate" in code_text:
            category = "rate_limit"
        elif "timeout" in name or isinstance(exc, TimeoutError):
            category = "timeout"
        elif "connection" in name or isinstance(exc, ConnectionError):
            category = "connection"
        else:
            category = "unknown"
        diagnostic = {"category": category}
        if status is not None:
            diagnostic["status_code"] = status
        if code is not None:
            diagnostic["error_code"] = code
    return diagnostic


@dataclass(frozen=True)
class ProviderConfig:
    api_key: str
    model: str
    max_input_tokens: int = 7000
    max_output_tokens: int = 1200
    judge_max_input_tokens: int = 10000
    judge_max_output_tokens: int = 2000
    reasoning_effort: str = "none"
    retries: int = 0

    @classmethod
    def from_environment(cls) -> "ProviderConfig":
        key = os.environ.get("OPENAI_API_KEY", "")
        model = os.environ.get("MOVIE_REVIEW_MODEL", "gpt-5.4-mini")
        if not key:
            raise ProviderError("OPENAI_API_KEY is required")
        return cls(
            api_key=key,
            model=model,
            max_input_tokens=_integer_env("MOVIE_REVIEW_MAX_INPUT_TOKENS", 7000),
            max_output_tokens=_integer_env("MOVIE_REVIEW_MAX_OUTPUT_TOKENS", 1200),
            judge_max_input_tokens=_integer_env("MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS", 10000),
            judge_max_output_tokens=_integer_env("MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS", 2000),
        )

    def sanitized(self) -> dict[str, Any]:
        return {
            "provider": "openai",
            "model": self.model,
            "credential_present": bool(self.api_key),
            "max_input_tokens": self.max_input_tokens,
            "max_output_tokens": self.max_output_tokens,
            "judge_max_input_tokens": self.judge_max_input_tokens,
            "judge_max_output_tokens": self.judge_max_output_tokens,
            "reasoning_effort": self.reasoning_effort,
            "retries": self.retries,
        }


def _integer_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ProviderError(f"{name} must be an integer") from exc
    if parsed <= 0:
        raise ProviderError(f"{name} must be positive")
    return parsed


class OpenAIProvider:
    def __init__(self, config: ProviderConfig, summarize_prompt: str, judge_prompt: str) -> None:
        self.config = config
        self.summarize_prompt = summarize_prompt
        self.judge_prompt = judge_prompt
        self._client = None

    def _client_or_raise(self):
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ProviderError("OpenAI client dependency is unavailable") from exc
            self._client = OpenAI(api_key=self.config.api_key, max_retries=self.config.retries)
        return self._client

    @staticmethod
    def _output_text(response: Any) -> str:
        text = getattr(response, "output_text", None)
        if text:
            return text
        chunks: list[str] = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                value = getattr(content, "text", None)
                if value:
                    chunks.append(value)
        return "".join(chunks)

    def summarize(self, review_text: str) -> dict[str, Any]:
        try:
            response = self._client_or_raise().responses.create(
                model=self.config.model,
                instructions=self.summarize_prompt,
                input=review_text,
                max_output_tokens=self.config.max_output_tokens,
                reasoning={"effort": self.config.reasoning_effort},
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "movie_review_summary",
                        "strict": True,
                        "schema": success_schema(),
                    }
                },
            )
            return _parse_json(self._output_text(response))
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("model request failed", sanitized_provider_diagnostic(exc)) from exc

    def judge(self, review_text: str, application_result: dict[str, Any], rubric: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps({"review": review_text, "application_result": application_result, "rubric": rubric}, ensure_ascii=False)
        try:
            response = self._client_or_raise().responses.create(
                model=self.config.model,
                instructions=self.judge_prompt,
                input=payload,
                max_output_tokens=self.config.judge_max_output_tokens,
                reasoning={"effort": self.config.reasoning_effort},
            )
            return _parse_json(self._output_text(response))
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("judge request failed", sanitized_provider_diagnostic(exc)) from exc


def _parse_json(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise InvalidProviderOutput("model returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise InvalidProviderOutput("model returned a non-object JSON value")
    return value

