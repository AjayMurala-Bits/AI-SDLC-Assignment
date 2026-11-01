"""Configurable OpenAI/Ollama adapters with sanitized diagnostics."""

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


def _capture_usage(response: Any, telemetry: dict[str, Any] | None) -> None:
    """Copy only numeric token counters from a provider response."""
    if telemetry is None:
        return
    usage = getattr(response, "usage", None)
    if usage is None:
        return
    counters: dict[str, int] = {}
    aliases = {
        "input_tokens": ("input_tokens", "prompt_tokens"),
        "output_tokens": ("output_tokens", "completion_tokens"),
        "total_tokens": ("total_tokens",),
    }
    for name, candidates in aliases.items():
        value = next((getattr(usage, candidate, None) for candidate in candidates if getattr(usage, candidate, None) is not None), None)
        if isinstance(value, int) and value >= 0:
            counters[name] = value
    telemetry.update(counters)


@dataclass(frozen=True)
class ProviderConfig:
    api_key: str
    model: str
    provider: str = "openai"
    base_url: str | None = None
    max_input_tokens: int = 7000
    max_output_tokens: int = 1200
    judge_max_input_tokens: int = 10000
    judge_max_output_tokens: int = 2000
    reasoning_effort: str = "none"
    retries: int = 0

    @classmethod
    def from_environment(cls) -> "ProviderConfig":
        provider = os.environ.get("MOVIE_REVIEW_PROVIDER", "ollama").strip().lower()
        if provider not in {"openai", "ollama"}:
            raise ProviderError("MOVIE_REVIEW_PROVIDER must be openai or ollama")
        key = os.environ.get("OPENAI_API_KEY", "") if provider == "openai" else ""
        if provider == "openai" and not key:
            raise ProviderError("OPENAI_API_KEY is required")
        model = os.environ.get("MOVIE_REVIEW_MODEL", "gpt-5.4-mini" if provider == "openai" else "llama3.2:latest")
        base_url = os.environ.get("MOVIE_REVIEW_BASE_URL") if provider == "openai" else os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
        return cls(
            api_key=key,
            model=model,
            provider=provider,
            base_url=base_url,
            max_input_tokens=_integer_env("MOVIE_REVIEW_MAX_INPUT_TOKENS", 7000),
            max_output_tokens=_integer_env("MOVIE_REVIEW_MAX_OUTPUT_TOKENS", 1200),
            judge_max_input_tokens=_integer_env("MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS", 10000),
            judge_max_output_tokens=_integer_env("MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS", 2000),
        )

    def sanitized(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "credential_present": bool(self.api_key),
            "base_url": self.base_url,
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
            kwargs: dict[str, Any] = {
                "api_key": self.config.api_key,
                "max_retries": self.config.retries,
            }
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            self._client = OpenAI(**kwargs)
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

    def summarize(self, review_text: str, telemetry: dict[str, Any] | None = None) -> dict[str, Any]:
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
            _capture_usage(response, telemetry)
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


class OllamaProvider(OpenAIProvider):
    """Ollama's local OpenAI-compatible Chat Completions adapter."""

    @staticmethod
    def _response_format() -> dict[str, Any]:
        """Use Ollama's schema mode with the unchanged application contract."""
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "movie_review_summary",
                "strict": True,
                "schema": success_schema(),
            },
        }

    def _client_or_raise(self):
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ProviderError("OpenAI-compatible client dependency is unavailable") from exc
            self._client = OpenAI(
                api_key="ollama",
                base_url=self.config.base_url or "http://127.0.0.1:11434/v1",
                max_retries=self.config.retries,
            )
        return self._client

    @staticmethod
    def _chat_text(response: Any) -> str:
        choices = getattr(response, "choices", []) or []
        if not choices:
            raise InvalidProviderOutput("model returned no chat choices")
        message = getattr(choices[0], "message", None)
        text = getattr(message, "content", None)
        if isinstance(text, str) and text:
            return text
        raise InvalidProviderOutput("model returned empty chat content")

    def summarize(self, review_text: str, telemetry: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = self._client_or_raise().chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.summarize_prompt},
                    {"role": "user", "content": review_text},
                ],
                max_tokens=self.config.max_output_tokens,
                response_format=self._response_format(),
            )
            _capture_usage(response, telemetry)
            return _parse_json(self._chat_text(response))
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("model request failed", sanitized_provider_diagnostic(exc)) from exc

    def judge(self, review_text: str, application_result: dict[str, Any], rubric: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps({"review": review_text, "application_result": application_result, "rubric": rubric}, ensure_ascii=False)
        try:
            response = self._client_or_raise().chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.judge_prompt},
                    {"role": "user", "content": payload},
                ],
                max_tokens=self.config.judge_max_output_tokens,
                response_format={"type": "json_object"},
            )
            return _parse_json(self._chat_text(response))
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("judge request failed", sanitized_provider_diagnostic(exc)) from exc


def provider_from_environment(summarize_prompt: str, judge_prompt: str) -> tuple[ProviderConfig, OpenAIProvider]:
    config = ProviderConfig.from_environment()
    adapter = OllamaProvider if config.provider == "ollama" else OpenAIProvider
    return config, adapter(config, summarize_prompt, judge_prompt)


def _parse_json(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise InvalidProviderOutput("model returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise InvalidProviderOutput("model returned a non-object JSON value")
    return value

