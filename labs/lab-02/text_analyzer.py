"""Small text analysis helpers for lab-02.

Provides:
- count_words_in_file(path: str) -> int
- CLI to print word count for a file

Note: the directory `lab-02` contains a hyphen, so this module may not be importable
as a normal package; tests should load it by path if needed.

Example:
    >>> from pathlib import Path
    >>> # Create a sample file
    >>> p = Path("sample.txt")
    >>> p.write_text("Hello, world! This is a test.")
    >>> count_words_in_file("sample.txt")
    6
    >>> # Or use from command line:
    >>> # python text_analyzer.py sample.txt
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional

WORD_RE = re.compile(r"\b[\w']+\b", flags=re.UNICODE)


def count_words_in_file(path: str) -> int:
    r"""Return the number of words in the given text file.

    Words are tokens matched by the regular expression ``WORD_RE``. This
    treats contractions like "don't" as a single word and counts numbers
    and underscores as word characters (Python ``\w`` semantics).

    Args:
        path: path to a UTF-8 encoded text file. Must not be empty.

    Raises:
        ValueError: if path is empty or None.
        FileNotFoundError: if the file does not exist.
        IsADirectoryError: if path points to a directory.
        PermissionError: if the file cannot be read due to permissions.
        UnicodeDecodeError: if the file is not valid UTF-8.
        OSError: for other I/O errors (disk full, etc.).

    Returns:
        Number of word tokens found in the file.
        
    Example:
        >>> count_words_in_file("sample.txt")
        42
    """
    if not path:
        raise ValueError("path cannot be empty")
    
    p = Path(path)
    
    # Check if it's a directory before attempting to open
    if p.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")
    
    try:
        with p.open("r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {path}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Could not decode file as UTF-8: {path}"
        )
    except OSError as e:
        raise OSError(f"Error reading file {path}: {e}")

    words = WORD_RE.findall(text)
    return len(words)


def _main() -> int:
    """Main entry point for command-line usage.
    
    Returns:
        Exit code: 0 for success, non-zero for errors.
    """
    parser = argparse.ArgumentParser(
        description="Count words in a text file",
        epilog="Example: python text_analyzer.py document.txt"
    )
    parser.add_argument("path", help="Path to the text file to analyze")
    args = parser.parse_args()

    try:
        count = count_words_in_file(args.path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except IsADirectoryError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3
    except PermissionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 4
    except UnicodeDecodeError as e:
        print(f"Error: Could not decode file as UTF-8: {args.path}", file=sys.stderr)
        return 5
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 6
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 99

    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
