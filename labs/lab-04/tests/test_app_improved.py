"""Unit tests for improved Flask application."""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

# Add solutions directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from app_improved import (
    validate_input_data,
    transform_to_dataframe,
    calculate_statistics,
    generate_category_report,
    process_data,
    merge_sort,
    process_user_data,
    ValidationError,
    DatabaseManager,
    app
)


# ============================================================================
# Validation Tests
# ============================================================================

class TestValidateInputData:
    """Tests for validate_input_data function."""
    
    def test_valid_data(self):
        """Test with valid input."""
        data = [
            {'id': 1, 'value': 100, 'category': 'A'},
            {'id': 2, 'value': 200, 'category': 'B'}
        ]
        validate_input_data(data)  # Should not raise
    
    def test_not_a_list(self):
        """Test with non-list input."""
        with pytest.raises(ValidationError, match="Input must be a list"):
            validate_input_data("not a list")
    
    def test_empty_list(self):
        """Test with empty list."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_input_data([])
    
    def test_too_large_list(self):
        """Test with list exceeding max size."""
        data = [{'id': i, 'value': 100, 'category': 'A'} for i in range(1001)]
        with pytest.raises(ValidationError, match="too large"):
            validate_input_data(data)
    
    def test_missing_required_field(self):
        """Test with missing required field."""
        data = [{'id': 1, 'value': 100}]  # Missing 'category'
        with pytest.raises(ValidationError, match="Missing required field 'category'"):
            validate_input_data(data)
    
    def test_invalid_id_type(self):
        """Test with invalid ID type."""
        data = [{'id': 'one', 'value': 100, 'category': 'A'}]
        with pytest.raises(ValidationError, match="'id' must be a positive integer"):
            validate_input_data(data)
    
    def test_duplicate_id(self):
        """Test with duplicate IDs."""
        data = [
            {'id': 1, 'value': 100, 'category': 'A'},
            {'id': 1, 'value': 200, 'category': 'B'}
        ]
        with pytest.raises(ValidationError, match="Duplicate ID"):
            validate_input_data(data)
    
    def test_invalid_value_type(self):
        """Test with non-numeric value."""
        data = [{'id': 1, 'value': 'hundred', 'category': 'A'}]
        with pytest.raises(ValidationError, match="'value' must be numeric"):
            validate_input_data(data)
    
    def test_invalid_category_type(self):
        """Test with non-string category."""
        data = [{'id': 1, 'value': 100, 'category': 123}]
        with pytest.raises(ValidationError, match="'category' must be a non-empty string"):
            validate_input_data(data)
    
    def test_non_alphanumeric_category(self):
        """Test with special characters in category."""
        data = [{'id': 1, 'value': 100, 'category': 'A@B'}]
        with pytest.raises(ValidationError, match="'category' must be alphanumeric"):
            validate_input_data(data)


# ============================================================================
# Transformation Tests
# ============================================================================

class TestTransformToDataframe:
    """Tests for transform_to_dataframe function."""
    
    def test_basic_transformation(self):
        """Test basic data transformation."""
        data = [
            {'id': 1, 'value': 100, 'category': 'a'},
            {'id': 2, 'value': 200, 'category': 'b'}
        ]
        df = transform_to_dataframe(data)
        
        assert len(df) == 2
        assert list(df.columns) == ['id', 'value', 'category', 'processed']
        assert df['category'].tolist() == ['A', 'B']
        assert df['processed'].tolist() == [200.0, 400.0]
    
    def test_value_conversion(self):
        """Test value type conversion."""
        data = [{'id': 1, 'value': 100, 'category': 'a'}]
        df = transform_to_dataframe(data)
        assert df['value'].dtype == float
    
    def test_category_uppercase(self):
        """Test category uppercase conversion."""
        data = [{'id': 1, 'value': 100, 'category': 'lowercase'}]
        df = transform_to_dataframe(data)
        assert df['category'].iloc[0] == 'LOWERCASE'


# ============================================================================
# Statistics Tests
# ============================================================================

class TestCalculateStatistics:
    """Tests for calculate_statistics function."""
    
    def test_basic_statistics(self):
        """Test basic statistical calculations."""
        df = pd.DataFrame({'value': [10, 20, 30, 40, 50]})
        stats = calculate_statistics(df)
        
        assert stats['total'] == 150.0
        assert stats['average'] == 30.0
        assert stats['max'] == 50.0
        assert stats['min'] == 10.0
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({'value': []})
        stats = calculate_statistics(df)
        
        assert stats['total'] == 0.0
        assert stats['average'] == 0.0
    
    def test_single_value(self):
        """Test with single value."""
        df = pd.DataFrame({'value': [42]})
        stats = calculate_statistics(df)
        
        assert stats['total'] == 42.0
        assert stats['average'] == 42.0
        assert stats['max'] == 42.0
        assert stats['min'] == 42.0


# ============================================================================
# Report Generation Tests
# ============================================================================

class TestGenerateCategoryReport:
    """Tests for generate_category_report function."""
    
    def test_basic_report(self):
        """Test basic category report."""
        df = pd.DataFrame({
            'category': ['A', 'A', 'B', 'B', 'B'],
            'value': [10, 20, 30, 40, 50]
        })
        report = generate_category_report(df)
        
        assert 'A' in report
        assert 'B' in report
        assert report['A']['count'] == 2
        assert report['A']['total'] == 30.0
        assert report['A']['average'] == 15.0
        assert report['B']['count'] == 3
    
    def test_single_category(self):
        """Test with single category."""
        df = pd.DataFrame({
            'category': ['A', 'A', 'A'],
            'value': [10, 20, 30]
        })
        report = generate_category_report(df)
        
        assert len(report) == 1
        assert report['A']['count'] == 3


# ============================================================================
# Merge Sort Tests
# ============================================================================

class TestMergeSort:
    """Tests for merge_sort function."""
    
    def test_basic_sort(self):
        """Test basic sorting."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = merge_sort(arr)
        assert result == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_empty_array(self):
        """Test with empty array."""
        assert merge_sort([]) == []
    
    def test_single_element(self):
        """Test with single element."""
        assert merge_sort([42]) == [42]
    
    def test_already_sorted(self):
        """Test with already sorted array."""
        arr = [1, 2, 3, 4, 5]
        assert merge_sort(arr) == [1, 2, 3, 4, 5]
    
    def test_reverse_sorted(self):
        """Test with reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        assert merge_sort(arr) == [1, 2, 3, 4, 5]
    
    def test_duplicates(self):
        """Test with duplicates."""
        arr = [3, 1, 3, 2, 1, 2]
        assert merge_sort(arr) == [1, 1, 2, 2, 3, 3]
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        arr = [-5, 3, -1, 0, 2]
        assert merge_sort(arr) == [-5, -1, 0, 2, 3]
    
    def test_does_not_modify_original(self):
        """Test that original array is not modified."""
        arr = [3, 1, 2]
        result = merge_sort(arr)
        assert arr == [3, 1, 2]
        assert result == [1, 2, 3]


# ============================================================================
# Process User Data Tests
# ============================================================================

class TestProcessUserData:
    """Tests for process_user_data function."""
    
    def test_valid_input(self):
        """Test with valid input."""
        result = process_user_data(("Alice", 30))
        assert result == "User Alice is 30 years old"
    
    def test_none_input(self):
        """Test with None input."""
        result = process_user_data(None)
        assert result == "No user information provided"
    
    def test_invalid_type(self):
        """Test with invalid type."""
        with pytest.raises(TypeError, match="must be a tuple or list"):
            process_user_data("not a tuple")
    
    def test_wrong_length(self):
        """Test with wrong tuple length."""
        with pytest.raises(ValueError, match="must have exactly 2 elements"):
            process_user_data(("Alice", 30, "extra"))
    
    def test_invalid_name_type(self):
        """Test with invalid name type."""
        with pytest.raises(TypeError, match="name must be a string"):
            process_user_data((123, 30))
    
    def test_invalid_age_type(self):
        """Test with invalid age type."""
        with pytest.raises(TypeError, match="age must be an integer"):
            process_user_data(("Alice", "thirty"))
    
    def test_negative_age(self):
        """Test with negative age."""
        with pytest.raises(ValueError, match="age must be non-negative"):
            process_user_data(("Alice", -5))


# ============================================================================
# Database Manager Tests
# ============================================================================

class TestDatabaseManager:
    """Tests for DatabaseManager class."""
    
    def test_initialization(self):
        """Test database manager initialization."""
        db = DatabaseManager('sqlite:///:memory:')
        assert db.engine is not None
        assert db.max_retries == 3
    
    def test_check_connection(self):
        """Test connection health check."""
        db = DatabaseManager('sqlite:///:memory:')
        assert db.check_connection() is True
    
    @patch('app_improved.create_engine')
    def test_connection_failure(self, mock_create_engine):
        """Test handling of connection failure."""
        mock_create_engine.side_effect = Exception("Connection failed")
        db = DatabaseManager('sqlite:///test.db')
        assert db.engine is None


# ============================================================================
# Integration Tests
# ============================================================================

class TestProcessData:
    """Integration tests for process_data function."""
    
    @patch('app_improved.save_processed_data')
    def test_complete_processing(self, mock_save):
        """Test complete data processing pipeline."""
        mock_save.return_value = True
        
        data = [
            {'id': 1, 'value': 100, 'category': 'A'},
            {'id': 2, 'value': 200, 'category': 'B'}
        ]
        
        result = process_data(data)
        
        assert 'total' in result
        assert 'average' in result
        assert 'report' in result
        assert 'data_saved' in result
        assert result['total'] == 300.0
        assert result['data_saved'] is True
    
    @patch('app_improved.save_processed_data')
    def test_processing_with_failed_save(self, mock_save):
        """Test processing continues even if save fails."""
        mock_save.return_value = False
        
        data = [{'id': 1, 'value': 100, 'category': 'A'}]
        result = process_data(data)
        
        assert result['data_saved'] is False
        assert 'total' in result


# ============================================================================
# Flask API Tests
# ============================================================================

class TestFlaskAPI:
    """Tests for Flask API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @patch('app_improved.process_data')
    def test_valid_request(self, mock_process, client):
        """Test valid API request."""
        mock_process.return_value = {'total': 100.0, 'average': 100.0}
        
        response = client.post(
            '/api/data',
            json=[{'id': 1, 'value': 100, 'category': 'A'}],
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total' in data
    
    def test_missing_content_type(self, client):
        """Test request without JSON content type."""
        response = client.post('/api/data', data='not json')
        assert response.status_code == 415
    
    def test_invalid_json(self, client):
        """Test request with invalid JSON."""
        response = client.post(
            '/api/data',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_validation_error(self, client):
        """Test request with validation error."""
        response = client.post(
            '/api/data',
            json=[{'id': 'invalid', 'value': 100, 'category': 'A'}],
            content_type='application/json'
        )
        assert response.status_code == 422
        data = response.get_json()
        assert 'error' in data
        assert 'details' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
