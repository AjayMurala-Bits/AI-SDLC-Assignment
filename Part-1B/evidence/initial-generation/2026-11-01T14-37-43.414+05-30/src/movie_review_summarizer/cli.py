"""JSON-only command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .application import failure, summarize_file
from .provider import OpenAIProvider, ProviderConfig, ProviderError


def _prompt_text(name: str) -> str:
    return Path(__file__).resolve().parents[2].joinpath("prompts", name).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize one movie's review text as grounded JSON.")
    parser.add_argument("--input", required=True, help="path to one UTF-8 review text file")
    args = parser.parse_args(argv)
    try:
        config = ProviderConfig.from_environment()
        provider = OpenAIProvider(config, _prompt_text("summarize.txt"), _prompt_text("judge.txt"))
        result = summarize_file(args.input, provider)
    except ProviderError as exc:
        result = failure("model_failure", str(exc))
    except OSError as exc:
        result = failure("invalid_input", str(exc))
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if "error" not in result else 1

