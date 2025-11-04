"""Lab 01 - Simple AI tools orchestrator.

Each lab part now lives in its own module:
- hello.py       -> Part 1: console hello world helper.
- calculator.py  -> Part 2: CLI calculator + Flask web app.
- tools_info.py  -> Part 3: tool comparison data and print helper.
- chatbot.py     -> Part 4: OpenAI chat invocation scaffold.

Run `python lab-01-FLC.py --help` for a CLI that delegates to these modules,
or execute each module directly for standalone usage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

MODULE_DIR = Path(__file__).parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import hello  # type: ignore
import calculator  # type: ignore
import tools_info  # type: ignore
import chatbot  # type: ignore


# Legacy per-part functions live in dedicated modules above. CLI wiring below.


# ============================================================
# CLI Entrypoint
# ============================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solutions for Lab 01 - Simple AI Tools.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello_parser = subparsers.add_parser(
        "hello", help="Print the Hello World message (Part 1)."
    )
    hello_parser.add_argument(
        "--language",
        default="Python",
        help="Label the language or runtime used for the hello app.",
    )

    calc_parser = subparsers.add_parser(
        "calc", help="Compute the sum and average for a sequence of numbers (Part 2)."
    )
    calc_parser.add_argument(
        "numbers",
        help="Comma or space separated numbers, e.g. '1, 2, 3.5'.",
    )

    api_parser = subparsers.add_parser(
        "api", help="Run the Flask API exposing /math/sum and /math/average (Part 2)."
    )
    api_parser.add_argument(
        "--host", default="127.0.0.1", help="Host interface for the Flask dev server."
    )
    api_parser.add_argument(
        "--port", type=int, default=5000, help="Port for the Flask dev server."
    )

    tools_parser = subparsers.add_parser(
        "tools", help="Display AI tooling comparisons and knowledge cutoffs (Part 3)."
    )
    tools_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress explanatory headers (useful for scripting).",
    )

    chatbot_parser = subparsers.add_parser(
        "chatbot", help="Invoke the OpenAI chat helper with a prompt (Part 4)."
    )
    chatbot_parser.add_argument(
        "--prompt",
        default="Summarise Lab 01 takeaways.",
        help="Prompt sent to the chat completion endpoint.",
    )
    chatbot_parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="Model passed to invoke_openai_chat (must be supported by your key).",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "hello":
        hello.demo_hello_world(args.language)
    elif args.command == "calc":
        calculator.run_cli_calculator(args.numbers)
    elif args.command == "api":
        app = calculator.create_app()
        app.run(host=args.host, port=args.port, debug=True)
    elif args.command == "tools":
        if args.quiet:
            for profile in tools_info.TOOL_PROFILES:
                print(
                    f"{profile.name}: {profile.pricing} ({profile.privacy}) - {profile.notes}"
                )
            for model, limitation in tools_info.MODEL_CUTOFF_DATES.items():
                print(f"{model}: {limitation}")
        else:
            tools_info.describe_tool_landscape()
    elif args.command == "chatbot":
        chatbot.ensure_api_key_present()
        response = chatbot.invoke_openai_chat(args.prompt, model=args.model)
        print(response)
    else:
        parser.error(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
