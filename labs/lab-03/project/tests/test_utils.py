"""Unit tests for utils module.

Tests cover all utility functions including error handling,
edge cases, and proper functionality.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import (
    process_data,
    validate_input,
    format_output,
    calculate_statistics
)


class TestProcessData:
    """Tests for process_data function."""
    
    def test_basic_processing(self):
        """Test basic data doubling."""
        assert process_data([1, 2, 3]) == [2, 4, 6]
    
    def test_empty_list(self):
        """Test with empty list."""
        assert process_data([]) == []
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert process_data([-1, -2, -3]) == [-2, -4, -6]
    
    def test_zero(self):
        """Test with zeros."""
        assert process_data([0, 0, 0]) == [0, 0, 0]


class TestValidateInput:
    """Tests for validate_input function."""
    
    def test_valid_list(self):
        """Test with valid list input."""
        assert validate_input([1, 2, 3]) is True
    
    def test_empty_list(self):
        """Test with empty list."""
        assert validate_input([]) is True
    
    def test_invalid_string(self):
        """Test with string input."""
        with pytest.raises(TypeError, match="Expected list, got str"):
            validate_input("not a list")
    
    def test_invalid_dict(self):
        """Test with dictionary input."""
        with pytest.raises(TypeError, match="Expected list, got dict"):
            validate_input({"key": "value"})
    
    def test_invalid_none(self):
        """Test with None input."""
        with pytest.raises(TypeError, match="Expected list, got NoneType"):
            validate_input(None)


class TestFormatOutput:
    """Tests for format_output function."""
    
    def test_list_formatting(self):
        """Test formatting a list."""
        assert format_output([1, 2, 3]) == "Result: [1, 2, 3]"
    
    def test_string_formatting(self):
        """Test formatting a string."""
        assert format_output("test") == "Result: test"
    
    def test_dict_formatting(self):
        """Test formatting a dictionary."""
        result = format_output({"key": "value"})
        assert result == "Result: {'key': 'value'}"


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""
    
    def test_basic_statistics(self):
        """Test basic statistical calculations."""
        stats = calculate_statistics([1, 2, 3, 4, 5])
        assert stats['mean'] == 3.0
        assert stats['median'] == 3
        assert stats['range'] == 4
    
    def test_single_number(self):
        """Test with single number."""
        stats = calculate_statistics([42])
        assert stats['mean'] == 42.0
        assert stats['median'] == 42
        assert stats['range'] == 0
    
    def test_duplicate_numbers(self):
        """Test with duplicate numbers."""
        stats = calculate_statistics([2, 2, 2, 2])
        assert stats['mean'] == 2.0
        assert stats['median'] == 2
        assert stats['range'] == 0
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        stats = calculate_statistics([-5, -2, 0, 2, 5])
        assert stats['mean'] == 0.0
        assert stats['median'] == 0
        assert stats['range'] == 10
    
    def test_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate statistics for empty list"):
            calculate_statistics([])
    
    def test_non_numeric_raises_error(self):
        """Test that non-numeric values raise TypeError."""
        with pytest.raises(TypeError, match="All elements must be numeric"):
            calculate_statistics([1, 2, "three", 4])
    
    def test_mixed_int_float(self):
        """Test with mixed integers and floats."""
        stats = calculate_statistics([1, 2.5, 3, 4.5, 5])
        assert stats['mean'] == 3.2
        assert stats['median'] == 3
        assert stats['range'] == 4.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
