"""Unit tests for api module.

Tests API functions with mocking to avoid real HTTP calls.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import requests

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api import fetch_data, process_response, api_call


class TestFetchData:
    """Tests for fetch_data function."""
    
    @patch('api.requests.get')
    def test_successful_fetch(self, mock_get):
        """Test successful data fetching."""
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'ok', 'data': {'value': 42}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = fetch_data("https://api.example.com/test")
        
        assert result == {'status': 'ok', 'data': {'value': 42}}
        mock_get.assert_called_once()
    
    def test_invalid_url(self):
        """Test with invalid URL."""
        with pytest.raises(ValueError, match="Invalid URL"):
            fetch_data("not-a-url")
    
    def test_empty_url(self):
        """Test with empty URL."""
        with pytest.raises(ValueError, match="Invalid URL"):
            fetch_data("")
    
    @patch('api.requests.get')
    def test_timeout_handling(self, mock_get):
        """Test timeout error handling."""
        mock_get.side_effect = requests.Timeout("Connection timeout")
        
        with pytest.raises(requests.Timeout):
            fetch_data("https://api.example.com/test", timeout=1)
    
    @patch('api.requests.get')
    def test_http_error_handling(self, mock_get):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            fetch_data("https://api.example.com/test")


class TestProcessResponse:
    """Tests for process_response function."""
    
    def test_successful_response(self):
        """Test processing successful response."""
        response = {'status': 'ok', 'data': {'value': 42}}
        result = process_response(response)
        assert result == {'value': 42}
    
    def test_error_response(self):
        """Test processing error response."""
        response = {'status': 'error', 'error': 'Something went wrong'}
        result = process_response(response)
        assert result is None
    
    def test_missing_data(self):
        """Test response with missing data field."""
        response = {'status': 'ok'}
        result = process_response(response)
        assert result is None
    
    def test_invalid_response_type(self):
        """Test with non-dict response."""
        with pytest.raises(TypeError, match="Response must be a dictionary"):
            process_response("not a dict")
    
    def test_none_response(self):
        """Test with None response."""
        with pytest.raises(TypeError, match="Response must be a dictionary"):
            process_response(None)


class TestApiCall:
    """Tests for api_call function."""
    
    @patch('api.fetch_data')
    def test_successful_call(self, mock_fetch):
        """Test successful API call."""
        mock_fetch.return_value = {'status': 'ok', 'data': {'value': 42}}
        
        result = api_call("https://api.example.com/test")
        
        assert result == {'value': 42}
    
    @patch('api.fetch_data')
    def test_failed_call(self, mock_fetch):
        """Test failed API call."""
        mock_fetch.side_effect = requests.RequestException("Network error")
        
        result = api_call("https://api.example.com/test")
        
        assert result is None
    
    @patch('api.fetch_data')
    def test_timeout_call(self, mock_fetch):
        """Test API call with timeout."""
        mock_fetch.side_effect = requests.Timeout("Timeout")
        
        result = api_call("https://api.example.com/test")
        
        assert result is None
    
    @patch('api.fetch_data')
    def test_invalid_url_call(self, mock_fetch):
        """Test API call with invalid URL."""
        mock_fetch.side_effect = ValueError("Invalid URL")
        
        result = api_call("invalid-url")
        
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
