"""
Improved Flask Application - Lab 04 Solutions

This is the refactored version of the original app.py with all improvements:
- Refactored process_data() into smaller, focused functions
- Added comprehensive input validation to /api/data endpoint
- Implemented robust database connection error handling
- Improved sorting function with merge sort
- Fixed TypeError in process_user_data()
"""
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import NullPool
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import logging
from functools import wraps
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ============================================================================
# Database Connection Management (Exercise 3 Solution)
# ============================================================================

class DatabaseManager:
    """Manages database connections with error handling and retry logic."""
    
    def __init__(self, database_url: Optional[str] = None, max_retries: int = 3):
        """
        Initialize database manager.
        
        Args:
            database_url: SQLAlchemy database URL
            max_retries: Maximum number of retry attempts
        """
        self.database_url = database_url or os.getenv(
            'DATABASE_URL', 
            'sqlite:///example.db'
        )
        self.max_retries = max_retries
        self.engine = None
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize database connection with error handling."""
        try:
            # Configure engine parameters conditionally based on dialect
            is_sqlite = self.database_url.startswith("sqlite:")
            if is_sqlite:
                # For SQLite, avoid QueuePool-specific args and use NullPool
                self.engine = create_engine(
                    self.database_url,
                    poolclass=NullPool,
                    connect_args={"check_same_thread": False}
                )
            else:
                # For non-SQLite databases, enable pooling knobs
                self.engine = create_engine(
                    self.database_url,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=3600
                )
            logger.info(f"Database connection initialized: {self.database_url}")
            
            # Test connection
            if self.check_connection():
                logger.info("Database connection test successful")
            else:
                logger.warning("Database connection test failed")
                
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to initialize database connection: {e}")
            self.engine = None
    
    def check_connection(self) -> bool:
        """
        Test database connection health.
        
        Returns:
            True if connection is healthy, False otherwise
        """
        if not self.engine:
            return False
        
        try:
            with self.engine.connect() as conn:
                # Use exec_driver_sql for SQLAlchemy 2.x compatibility
                conn.exec_driver_sql("SELECT 1")
            return True
        except exc.SQLAlchemyError as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute database operation with retry logic.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Exception: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except exc.OperationalError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(
                        f"Database operation failed (attempt {attempt + 1}/{self.max_retries}). "
                        f"Retrying in {wait_time}s: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Database operation failed after {self.max_retries} attempts")
        
        raise last_exception


# Initialize database manager
db_manager = DatabaseManager()


# ============================================================================
# Data Validation (Exercise 1 & 2 Solution)
# ============================================================================

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_input_data(data: List[Dict[str, Any]]) -> None:
    """
    Validate input data structure and types.
    
    Args:
        data: List of dictionaries to validate
        
    Raises:
        ValidationError: If validation fails
        
    Example:
        >>> validate_input_data([{'id': 1, 'value': 100, 'category': 'A'}])
        # No exception raised
        >>> validate_input_data([{'id': 1, 'value': 'invalid'}])
        ValidationError: Missing required field 'category'
    """
    if not isinstance(data, list):
        raise ValidationError("Input must be a list")
    
    if len(data) == 0:
        raise ValidationError("Input list cannot be empty")
    
    if len(data) > 1000:
        raise ValidationError("Input list too large (max 1000 items)")
    
    required_fields = ['id', 'value', 'category']
    seen_ids = set()
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValidationError(f"Item {idx} must be a dictionary")
        
        # Check required fields
        for field in required_fields:
            if field not in item:
                raise ValidationError(f"Item {idx}: Missing required field '{field}'")
        
        # Validate types
        if not isinstance(item['id'], int) or item['id'] <= 0:
            raise ValidationError(f"Item {idx}: 'id' must be a positive integer")
        
        if item['id'] in seen_ids:
            raise ValidationError(f"Item {idx}: Duplicate ID {item['id']}")
        seen_ids.add(item['id'])
        
        if not isinstance(item['value'], (int, float)):
            raise ValidationError(f"Item {idx}: 'value' must be numeric")
        
        if not isinstance(item['category'], str) or not item['category'].strip():
            raise ValidationError(f"Item {idx}: 'category' must be a non-empty string")
        
        if not item['category'].replace('_', '').isalnum():
            raise ValidationError(f"Item {idx}: 'category' must be alphanumeric")


def transform_to_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform input data to pandas DataFrame.
    
    Args:
        data: List of dictionaries
        
    Returns:
        Transformed DataFrame
        
    Example:
        >>> data = [{'id': 1, 'value': 100, 'category': 'a'}]
        >>> df = transform_to_dataframe(data)
        >>> df['category'].iloc[0]
        'A'
    """
    df = pd.DataFrame(data)
    df['value'] = df['value'].astype(float)
    df['processed'] = df['value'] * 2
    df['category'] = df['category'].str.upper()
    return df


def calculate_statistics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate statistical measures from DataFrame.
    
    Args:
        df: DataFrame with 'value' column
        
    Returns:
        Dictionary with total, average, max, min
        
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'value': [10, 20, 30]})
        >>> stats = calculate_statistics(df)
        >>> stats['total']
        60.0
    """
    if df.empty:
        return {'total': 0.0, 'average': 0.0, 'max': 0.0, 'min': 0.0}
    
    return {
        'total': float(df['value'].sum()),
        'average': float(df['value'].mean()),
        'max': float(df['value'].max()),
        'min': float(df['value'].min())
    }


def generate_category_report(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Generate report grouped by category.
    
    Args:
        df: DataFrame with 'category' and 'value' columns
        
    Returns:
        Nested dictionary with category statistics
        
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'category': ['A', 'A', 'B'], 'value': [10, 20, 30]})
        >>> report = generate_category_report(df)
        >>> report['A']['count']
        2
    """
    report = {}
    
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        report[category] = {
            'count': len(cat_data),
            'total': float(cat_data['value'].sum()),
            'average': float(cat_data['value'].mean())
        }
    
    return report


def save_processed_data(df: pd.DataFrame) -> bool:
    """
    Save processed data to database with error handling.
    
    Args:
        df: DataFrame to save
        
    Returns:
        True if successful, False otherwise
    """
    if not db_manager.engine:
        logger.error("Database engine not initialized")
        return False
    
    try:
        def _save():
            df.to_sql('processed_data', db_manager.engine, if_exists='append', index=False)
        
        db_manager.execute_with_retry(_save)
        logger.info(f"Saved {len(df)} records to database")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save data to database: {e}")
        return False


def process_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process input data through validation, transformation, and analysis.
    
    This is the refactored main function that orchestrates smaller functions.
    
    Args:
        data: List of dictionaries with 'id', 'value', 'category' fields
        
    Returns:
        Dictionary with statistics, report, and metadata
        
    Raises:
        ValidationError: If input validation fails
        
    Example:
        >>> data = [{'id': 1, 'value': 100, 'category': 'A'}]
        >>> result = process_data(data)
        >>> 'total' in result
        True
    """
    logger.info(f"Processing {len(data)} records")
    
    # Step 1: Validate
    validate_input_data(data)
    logger.debug("Input validation passed")
    
    # Step 2: Transform
    df = transform_to_dataframe(data)
    logger.debug("Data transformation completed")
    
    # Step 3: Calculate statistics
    result = calculate_statistics(df)
    logger.debug("Statistics calculated")
    
    # Step 4: Generate report
    result['report'] = generate_category_report(df)
    logger.debug("Category report generated")
    
    # Step 5: Save to database
    saved = save_processed_data(df)
    result['data_saved'] = saved
    if not saved:
        logger.warning("Data processing completed but not saved to database")
    
    return result


# ============================================================================
# REST API Endpoint with Validation (Exercise 2 Solution)
# ============================================================================

@app.route('/api/data', methods=['POST'])
def submit_data():
    """
    Submit data for processing with comprehensive validation.
    
    Request body must be JSON array of objects with:
    - id: positive integer (unique)
    - value: numeric
    - category: non-empty alphanumeric string
    
    Returns:
        JSON response with statistics and report
        
    Error Responses:
        400: Bad Request (invalid JSON or schema)
        415: Unsupported Media Type
        422: Unprocessable Entity (business rule violation)
        500: Internal Server Error
    """
    # Validate Content-Type
    if not request.is_json:
        return jsonify({
            'error': 'Unsupported Media Type',
            'details': ['Content-Type must be application/json'],
            'status': 415
        }), 415
    
    # Parse JSON
    try:
        data = request.json
    except Exception as e:
        return jsonify({
            'error': 'Invalid JSON',
            'details': [str(e)],
            'status': 400
        }), 400
    
    # Validate and process
    try:
        result = process_data(data)
        logger.info("Data processed successfully")
        return jsonify(result), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({
            'error': 'Validation failed',
            'details': [str(e)],
            'status': 422
        }), 422
        
    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'details': ['An unexpected error occurred'],
            'status': 500
        }), 500


# ============================================================================
# Improved Sorting Function (Example 1 Solution)
# ============================================================================

def merge_sort(arr: List[int]) -> List[int]:
    """
    Sort an array of integers using merge sort algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: List of integers to sort
        
    Returns:
        New sorted list (does not modify original)
        
    Example:
        >>> merge_sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
        >>> merge_sort([])
        []
        >>> merge_sort([42])
        [42]
    """
    # Handle edge cases
    if len(arr) <= 1:
        return arr.copy()
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.
    
    Args:
        left: Sorted list
        right: Sorted list
        
    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0
    
    # Merge elements in order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# Maintain backwards compatibility with original function name
basic_sort = merge_sort


# ============================================================================
# Fixed process_user_data (Example 2 Solution)
# ============================================================================

def process_user_data(user_info: Optional[Tuple[str, int]]) -> str:
    """
    Process user information with proper validation.
    
    Args:
        user_info: Tuple of (name, age) or None
        
    Returns:
        Formatted string with user information
        
    Raises:
        TypeError: If user_info is not a tuple or None
        ValueError: If user_info format is invalid
        
    Example:
        >>> process_user_data(("Alice", 30))
        'User Alice is 30 years old'
        >>> process_user_data(None)
        'No user information provided'
    """
    # Handle None input
    if user_info is None:
        return "No user information provided"
    
    # Validate type
    if not isinstance(user_info, (tuple, list)):
        raise TypeError(f"user_info must be a tuple or list, got {type(user_info).__name__}")
    
    # Validate length
    if len(user_info) != 2:
        raise ValueError(f"user_info must have exactly 2 elements, got {len(user_info)}")
    
    # Unpack and validate
    name, age = user_info
    
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")
    
    if not isinstance(age, int):
        raise TypeError(f"age must be an integer, got {type(age).__name__}")
    
    if age < 0:
        raise ValueError(f"age must be non-negative, got {age}")
    
    return f"User {name} is {age} years old"


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)
