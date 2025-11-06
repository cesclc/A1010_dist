"""Utility functions for data processing and validation.

This module provides helper functions for processing, validating,
and formatting data used throughout the application.
"""
import logging
from typing import List, Any, Dict
from statistics import mean, median

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_data(data: List[int]) -> List[int]:
    """Process data by doubling each element.
    
    Args:
        data: List of integers to process
        
    Returns:
        List with each element doubled
        
    Example:
        >>> process_data([1, 2, 3])
        [2, 4, 6]
    """
    return [x * 2 for x in data]


def validate_input(data: Any) -> bool:
    """Validate that input is a list.
    
    Args:
        data: Data to validate
        
    Returns:
        True if data is a list
        
    Raises:
        TypeError: If data is not a list
        
    Example:
        >>> validate_input([1, 2, 3])
        True
        >>> validate_input("not a list")
        Traceback (most recent call last):
        ...
        TypeError: Expected list, got str
    """
    if not isinstance(data, list):
        raise TypeError(f"Expected list, got {type(data).__name__}")
    return True


def format_output(data: Any) -> str:
    """Format data for display.
    
    Args:
        data: Data to format
        
    Returns:
        Formatted string representation
        
    Example:
        >>> format_output([2, 4, 6])
        'Result: [2, 4, 6]'
    """
    return f"Result: {data}"


def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """Calculate statistical measures for a list of numbers.
    
    This function computes mean, median, and range for a given list of numbers.
    It includes proper error handling for edge cases like empty lists.
    
    Args:
        numbers: List of numeric values to analyze
        
    Returns:
        Dictionary containing 'mean', 'median', and 'range' statistics
        
    Raises:
        ValueError: If the numbers list is empty
        TypeError: If numbers contains non-numeric values
        
    Example:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3, 'range': 4}
        >>> calculate_statistics([])
        Traceback (most recent call last):
        ...
        ValueError: Cannot calculate statistics for empty list
    """
    logger.info(f"Calculating statistics for {len(numbers)} numbers")
    
    if not numbers:
        logger.error("Attempted to calculate statistics on empty list")
        raise ValueError("Cannot calculate statistics for empty list")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        logger.error("Non-numeric values found in input")
        raise TypeError("All elements must be numeric")
        
    try:
        stats = {
            'mean': mean(numbers),
            'median': median(numbers),
            'range': max(numbers) - min(numbers)
        }
        logger.debug(f"Calculated statistics: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise


# Example usage with proper error handling
if __name__ == "__main__":
    # Test with valid data
    test_data = [1, 2, 2, 3, 4, 4, 5]
    try:
        result1 = calculate_statistics(test_data)
        print(f"Statistics for {test_data}:")
        print(f"  Mean: {result1['mean']:.2f}")
        print(f"  Median: {result1['median']}")
        print(f"  Range: {result1['range']}")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    
    # Test with empty data (will raise error)
    empty_data = []
    try:
        result2 = calculate_statistics(empty_data)
    except ValueError as e:
        print(f"\nExpected error for empty list: {e}")

