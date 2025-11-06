"""Tests for labs/lab-02/text_analyzer.py

Because the folder name contains a hyphen (`lab-02`), import the module by
file path using importlib utilities rather than by package name.

Test Coverage:
- Basic functionality: empty files, sample text
- Error handling: missing files, directories, empty paths, permissions
- Edge cases: Unicode, large files, special characters
"""
import importlib.util
import pathlib
import pytest


def load_text_analyzer_module():
    """Load the text_analyzer module by file path."""
    root = pathlib.Path(__file__).resolve().parents[1]
    module_path = root / "labs" / "lab-02" / "text_analyzer.py"
    spec = importlib.util.spec_from_file_location("text_analyzer", str(module_path))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


# Basic functionality tests

def test_empty_file(tmp_path):
    """Test that an empty file returns 0 words."""
    p = tmp_path / "empty.txt"
    p.write_text("")
    mod = load_text_analyzer_module()
    assert mod.count_words_in_file(str(p)) == 0


def test_sample_text(tmp_path):
    """Test word counting with sample text including contractions."""
    p = tmp_path / "sample.txt"
    text = "Hello, world! This is a test. Don't split contractions."
    p.write_text(text)
    mod = load_text_analyzer_module()
    # Expected tokens: Hello world This is a test Don't split contractions -> 9
    assert mod.count_words_in_file(str(p)) == 9


def test_numbers_and_underscores(tmp_path):
    """Test that numbers and underscores are counted as word characters."""
    p = tmp_path / "numbers.txt"
    text = "Python3 has snake_case and 42 numbers"
    p.write_text(text)
    mod = load_text_analyzer_module()
    # Expected: Python3 has snake_case and 42 numbers -> 6
    assert mod.count_words_in_file(str(p)) == 6


def test_unicode_text(tmp_path):
    """Test that Unicode text is handled correctly."""
    p = tmp_path / "unicode.txt"
    text = "Café naïve résumé 日本語 العربية"
    p.write_text(text, encoding="utf-8")
    mod = load_text_analyzer_module()
    # Expected: Café naïve résumé 日本語 العربية -> 5
    assert mod.count_words_in_file(str(p)) == 5


def test_punctuation_only(tmp_path):
    """Test that punctuation-only text returns 0 words."""
    p = tmp_path / "punct.txt"
    text = "!!! ??? ... --- ,,,"
    p.write_text(text)
    mod = load_text_analyzer_module()
    assert mod.count_words_in_file(str(p)) == 0


def test_multiline_text(tmp_path):
    """Test word counting across multiple lines."""
    p = tmp_path / "multiline.txt"
    text = """Line one has words.
Line two has more words.
Line three too."""
    p.write_text(text)
    mod = load_text_analyzer_module()
    # Expected: 12 words total
    assert mod.count_words_in_file(str(p)) == 12


# Error handling tests

def test_file_not_found():
    """Test that FileNotFoundError is raised for non-existent files."""
    mod = load_text_analyzer_module()
    with pytest.raises(FileNotFoundError, match="File not found"):
        mod.count_words_in_file("/nonexistent/path/to/file.txt")


def test_empty_path():
    """Test that ValueError is raised for empty path."""
    mod = load_text_analyzer_module()
    with pytest.raises(ValueError, match="path cannot be empty"):
        mod.count_words_in_file("")


def test_directory_path(tmp_path):
    """Test that IsADirectoryError is raised when path is a directory."""
    mod = load_text_analyzer_module()
    with pytest.raises(IsADirectoryError, match="Path is a directory"):
        mod.count_words_in_file(str(tmp_path))


def test_permission_error(tmp_path):
    """Test that PermissionError is raised for unreadable files."""
    import os
    import sys
    
    # Skip on Windows where chmod doesn't work the same way
    if sys.platform == "win32":
        pytest.skip("Permission test not supported on Windows")
    
    p = tmp_path / "noperm.txt"
    p.write_text("test content")
    os.chmod(str(p), 0o000)  # Remove all permissions
    
    mod = load_text_analyzer_module()
    try:
        with pytest.raises(PermissionError, match="Permission denied"):
            mod.count_words_in_file(str(p))
    finally:
        # Restore permissions for cleanup
        os.chmod(str(p), 0o644)


def test_non_utf8_file(tmp_path):
    """Test that UnicodeDecodeError is raised for non-UTF-8 files."""
    p = tmp_path / "latin1.txt"
    # Write Latin-1 encoded text with special characters
    p.write_bytes(b"Caf\xe9")  # Latin-1 encoding of "Café"
    
    mod = load_text_analyzer_module()
    with pytest.raises(UnicodeDecodeError, match="Could not decode file as UTF-8"):
        mod.count_words_in_file(str(p))


# Edge case tests

def test_very_long_word(tmp_path):
    """Test that very long words are counted correctly."""
    p = tmp_path / "longword.txt"
    long_word = "a" * 10000
    p.write_text(long_word)
    mod = load_text_analyzer_module()
    assert mod.count_words_in_file(str(p)) == 1


def test_whitespace_only(tmp_path):
    """Test that whitespace-only text returns 0 words."""
    p = tmp_path / "whitespace.txt"
    text = "   \n\t\r\n   "
    p.write_text(text)
    mod = load_text_analyzer_module()
    assert mod.count_words_in_file(str(p)) == 0
