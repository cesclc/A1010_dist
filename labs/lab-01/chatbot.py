"""Part 4: helper functions and CLI to invoke OpenAI chat models."""

from __future__ import annotations

import argparse
import os
from importlib import import_module
from typing import Sequence


def invoke_openai_chat(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Call OpenAI's chat completions API with the provided prompt."""
    try:
        openai_module = import_module("openai")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Install the `openai` package to run this example: pip install openai"
        ) from exc

    client = openai_module.OpenAI()  # type: ignore[attr-defined]
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise programming assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def ensure_api_key_present() -> None:
    """Raise a helpful error if OPENAI_API_KEY is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "Set the OPENAI_API_KEY environment variable before running this script."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Invoke the Part 4 OpenAI helper implemented in chatbot.py.",
    )
    parser.add_argument(
        "--prompt",
        default="Summarise Lab 01 takeaways.",
        help="Prompt sent to the chat completion endpoint.",
    )
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="Model passed to invoke_openai_chat (must be supported by your key).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    ensure_api_key_present()
    try:
        response = invoke_openai_chat(args.prompt, model=args.model)
    except Exception as exc:  # pragma: no cover - surface message for students
        raise RuntimeError(f"Call to invoke_openai_chat failed: {exc}") from exc

    print(response)


if __name__ == "__main__":
    main()
