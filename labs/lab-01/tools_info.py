"""Part 3: Tool comparison data and CLI helper."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ToolProfile:
    name: str
    pricing: str
    privacy: str
    notes: str


TOOL_PROFILES: Sequence[ToolProfile] = (
    ToolProfile(
        name="ChatGPT (GPT-4o mini)",
        pricing="$0.15 / 1M input tokens, $0.60 / 1M output tokens",
        privacy="Prompts retained for 30 days by default; opt-out via enterprise plans.",
        notes="Balanced option for prototyping; strong reasoning with modest cost.",
    ),
    ToolProfile(
        name="Claude (Haiku 3)",
        pricing="$0.25 / 1M input tokens, $1.25 / 1M output tokens",
        privacy="Anthropic retains data for abuse monitoring; enterprise controls available.",
        notes="Fast, cost-efficient; excels at summarisation and guarded responses.",
    ),
    ToolProfile(
        name="OpenAI GPT-3.5 Turbo",
        pricing="$0.50 / 1M input tokens, $1.50 / 1M output tokens",
        privacy="Data may be retained unless using the enterprise API tier.",
        notes="Lower reasoning depth; good fit for straightforward automation scripts.",
    ),
)


MODEL_CUTOFF_DATES = {
    "gpt-4o-mini": "Knowledge cutoff: October 2023; real-time browsing unavailable.",
    "gpt-3.5-turbo": "Knowledge cutoff: January 2022; weaker handling of new language features.",
    "claude-3-haiku": "Knowledge cutoff: August 2023; refuses speculative or unknown data.",
}


def describe_tool_landscape() -> None:
    """Print the tool comparison and cutoff information."""
    print("=== Tool Profiles ===")
    for profile in TOOL_PROFILES:
        print(f"- {profile.name}")
        print(f"  Pricing: {profile.pricing}")
        print(f"  Privacy: {profile.privacy}")
        print(f"  Notes: {profile.notes}")

    print("\n=== Knowledge Cut-off Dates ===")
    for model, limitation in MODEL_CUTOFF_DATES.items():
        print(f"- {model}: {limitation}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Display AI tool pricing, privacy, and knowledge cutoff data.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress explanatory headers (useful for scripting).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.quiet:
        for profile in TOOL_PROFILES:
            print(f"{profile.name}: {profile.pricing} ({profile.privacy}) - {profile.notes}")
        for model, limitation in MODEL_CUTOFF_DATES.items():
            print(f"{model}: {limitation}")
    else:
        describe_tool_landscape()


if __name__ == "__main__":
    main()
