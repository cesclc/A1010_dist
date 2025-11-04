"""Part 1 helper: simple Hello World utilities and CLI."""

from __future__ import annotations

import argparse
from typing import Sequence


def build_hello_message(language: str = "Python") -> str:
    """Return a formatted greeting used to validate the setup."""
    return f"Hello World from {language}!"


def demo_hello_world(language: str) -> None:
    """Print the hello message (used by CLI entry points)."""
    print(build_hello_message(language))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the Lab 01 hello message.")
    parser.add_argument(
        "--language",
        default="Python",
        help="Label the runtime or language you used for the hello app.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    demo_hello_world(args.language)


if __name__ == "__main__":
    main()
