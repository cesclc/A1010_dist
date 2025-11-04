"""Part 2: calculator logic for CLI and Flask server."""

from __future__ import annotations

import argparse
from importlib import import_module
from typing import Iterable, List, Sequence


def parse_number_sequence(raw_numbers: str) -> List[float]:
    """Parse a comma or space separated sequence of numbers."""
    if not raw_numbers.strip():
        raise ValueError("Provide at least one numeric value.")

    separators = [",", " "]
    normalized = raw_numbers
    for sep in separators:
        normalized = normalized.replace(sep, " ")

    tokens = [token for token in normalized.split(" ") if token]
    if not tokens:
        raise ValueError("No numeric tokens detected.")

    parsed: List[float] = []
    for token in tokens:
        try:
            parsed.append(float(token))
        except ValueError as exc:
            raise ValueError(f"Invalid number: {token}") from exc
    return parsed


def compute_sum_and_average(numbers: Iterable[float]) -> tuple[float, float]:
    """Return (sum, average) for a non-empty sequence of floats."""
    data = list(numbers)
    if not data:
        raise ValueError("At least one number is required.")
    total = float(sum(data))
    average = total / len(data)
    return total, average


def run_cli_calculator(raw_numbers: str) -> None:
    """Compute sum and average from a CLI-provided string."""
    numbers = parse_number_sequence(raw_numbers)
    total, average = compute_sum_and_average(numbers)
    formatted = ", ".join(f"{value:g}" for value in numbers)
    print(f"Input values: {formatted}")
    print(f"Sum: {total:g}")
    print(f"Average: {average:g}")


def _lazy_load_flask():
    """Import Flask lazily to avoid mandatory dependency."""
    try:
        return import_module("flask")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Flask is required for the web service. "
            "Install it with `pip install flask` in your environment."
        ) from exc


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Lab 01 Calculator</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; max-width: 720px;}
    form { display: grid; gap: 1rem; }
    textarea { min-height: 4rem; }
    pre { background: #f5f5f5; padding: 1rem; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Sum & Average Calculator</h1>
  <p>Enter numbers separated by commas or spaces, then choose an operation.</p>
  <form id="calc-form">
    <label>
      Numbers
      <textarea id="numbers" placeholder="e.g. 1, 2, 3.5" required></textarea>
    </label>
    <fieldset>
      <legend>Operation</legend>
      <label><input type="radio" name="operation" value="sum" checked> Sum</label>
      <label><input type="radio" name="operation" value="average"> Average</label>
    </fieldset>
    <button type="submit">Calculate</button>
  </form>
  <h2>Result</h2>
  <pre id="result" aria-live="polite">Waiting for input…</pre>

  <script>
    const form = document.getElementById("calc-form");
    const numbersInput = document.getElementById("numbers");
    const resultBox = document.getElementById("result");

    function parseValues(raw) {
      return raw.split(/[\\s,]+/).filter(Boolean).map(Number);
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const rawNumbers = numbersInput.value.trim();
      if (!rawNumbers) {
        resultBox.textContent = "Please enter at least one number.";
        return;
      }

      const values = parseValues(rawNumbers);
      if (values.length === 0 || values.some((value) => Number.isNaN(value))) {
        resultBox.textContent = "One or more entries are not valid numbers.";
        return;
      }

      const operation = document.querySelector('input[name="operation"]:checked').value;
      resultBox.textContent = "Calculating…";

      try {
        const response = await fetch(`/math/${operation}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ values }),
        });

        if (!response.ok) {
          const message = await response.text();
          throw new Error(message || `Request failed (${response.status})`);
        }

        const data = await response.json();
        const sum = Number(data.sum);
        const average = Number(data.average);
        switch (data.operation) {
          case "sum":
            resultBox.textContent = Number.isFinite(sum)
              ? `Sum: ${sum}`
              : "Unexpected response format.";
            break;
          case "average":
            resultBox.textContent = Number.isFinite(average)
              ? `Average: ${average}`
              : "Unexpected response format.";
            break;
          default:
            resultBox.textContent = JSON.stringify(data, null, 2);
        }
      } catch (error) {
        resultBox.textContent = `Error: ${error.message}`;
      }
    });
  </script>
</body>
</html>
"""


def create_app():
    """Create the Flask application exposing sum and average endpoints."""
    flask = _lazy_load_flask()
    Flask = flask.Flask  # type: ignore[attr-defined]
    request = flask.request  # type: ignore[attr-defined]
    jsonify = flask.jsonify  # type: ignore[attr-defined]
    Response = flask.Response  # type: ignore[attr-defined]

    app = Flask(__name__)

    def _extract_numbers() -> List[float]:
        """Extract numbers from query parameters or JSON bodies."""
        values: List[str] = []
        if request.args:
            values.extend(request.args.getlist("value"))
            values.extend(request.args.getlist("values"))
        if not values:
            payload = request.get_json(silent=True) or {}
            candidate = payload.get("values") if isinstance(payload, dict) else []
            if isinstance(candidate, Sequence):
                values.extend(str(item) for item in candidate)

        if not values:
            raise ValueError(
                "Provide numbers as repeated query parameters (?value=1&value=2) "
                "or as a JSON body {'values': [1, 2, 3]}."
            )

        try:
            return [float(item) for item in values]
        except ValueError as exc:
            raise ValueError(f"Non-numeric value in {values}") from exc

    @app.route("/", methods=["GET"])
    def index():
        return Response(INDEX_HTML, mimetype="text/html")

    @app.route("/math/sum", methods=["GET", "POST"])
    def sum_endpoint():
        numbers = _extract_numbers()
        total, _ = compute_sum_and_average(numbers)
        return jsonify({"operation": "sum", "input": numbers, "sum": total})

    @app.route("/math/average", methods=["GET", "POST"])
    def average_endpoint():
        numbers = _extract_numbers()
        total, average = compute_sum_and_average(numbers)
        return jsonify(
            {"operation": "average", "input": numbers, "sum": total, "average": average}
        )

    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Lab 01 calculator demos.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser(
        "calc", help="Compute the sum and average for a sequence of numbers."
    )
    calc_parser.add_argument(
        "numbers",
        help="Comma or space separated numbers, e.g. '1, 2, 3.5'.",
    )

    api_parser = subparsers.add_parser(
        "api", help="Run the Flask API exposing /math/sum and /math/average."
    )
    api_parser.add_argument(
        "--host", default="127.0.0.1", help="Host interface for the Flask dev server."
    )
    api_parser.add_argument(
        "--port", type=int, default=5000, help="Port for the Flask dev server."
    )

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "calc":
        run_cli_calculator(args.numbers)
    elif args.command == "api":
        app = create_app()
        app.run(host=args.host, port=args.port, debug=True)
    else:  # pragma: no cover - defensive
        parser.error(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
