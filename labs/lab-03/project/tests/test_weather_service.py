"""Unit tests for weather_service module.

Tests the WeatherService class with mocked API calls.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from weather_service import WeatherService, WeatherData
from config import Config


class TestWeatherData:
    """Tests for WeatherData dataclass."""
    
    def test_creation(self):
        """Test creating WeatherData instance."""
        now = datetime.now()
        data = WeatherData(
            temperature=20.5,
            humidity=65,
            description="Clear sky",
            city="London",
            timestamp=now
        )
        
        assert data.temperature == 20.5
        assert data.humidity == 65
        assert data.description == "Clear sky"
        assert data.city == "London"
        assert data.timestamp == now
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        now = datetime.now()
        data = WeatherData(
            temperature=20.5,
            humidity=65,
            description="Clear sky",
            city="London",
            timestamp=now
        )
        
        result = data.to_dict()
        assert result['temperature'] == 20.5
        assert result['humidity'] == 65
        assert result['city'] == "London"
        assert isinstance(result['timestamp'], str)
    
    def test_str_representation(self):
        """Test string representation."""
        now = datetime.now()
        data = WeatherData(
            temperature=20.5,
            humidity=65,
            description="Clear sky",
            city="London",
            timestamp=now
        )
        
        result = str(data)
        assert "London" in result
        assert "20.5°C" in result
        assert "65%" in result
        assert "Clear sky" in result


class TestWeatherService:
    """Tests for WeatherService class."""
    
    def test_initialization(self):
        """Test service initialization."""
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        
        assert service.config == config
        assert service.api_key == "test_key_12345"
    
    def test_initialization_without_api_key(self):
        """Test service initialization without API key."""
        config = Config()
        service = WeatherService(config)
        
        assert service.api_key is None
    
    @patch('weather_service.fetch_data')
    def test_get_weather_success(self, mock_fetch):
        """Test successful weather fetching."""
        mock_fetch.return_value = {
            'main': {
                'temp': 20.5,
                'humidity': 65
            },
            'weather': [
                {'description': 'clear sky'}
            ]
        }
        
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        weather = service.get_weather("London")
        
        assert weather is not None
        assert weather.temperature == 20.5
        assert weather.humidity == 65
        assert weather.description == "clear sky"
        assert weather.city == "London"
    
    def test_get_weather_invalid_city(self):
        """Test with invalid city name."""
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        
        # Empty string
        weather = service.get_weather("")
        assert weather is None
        
        # Non-string
        weather = service.get_weather(None)
        assert weather is None
    
    @patch('weather_service.fetch_data')
    def test_get_weather_api_error(self, mock_fetch):
        """Test handling of API errors."""
        mock_fetch.side_effect = Exception("API Error")
        
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        weather = service.get_weather("London")
        
        assert weather is None
    
    @patch('weather_service.fetch_data')
    def test_get_weather_invalid_response(self, mock_fetch):
        """Test handling of invalid API response."""
        mock_fetch.return_value = {'invalid': 'data'}
        
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        weather = service.get_weather("London")
        
        assert weather is None
    
    @patch('weather_service.fetch_data')
    def test_get_weather_summary(self, mock_fetch):
        """Test getting weather for multiple cities."""
        mock_fetch.return_value = {
            'main': {'temp': 20.0, 'humidity': 60},
            'weather': [{'description': 'sunny'}]
        }
        
        config = Config(API_KEY="test_key_12345")
        service = WeatherService(config)
        
        cities = ["London", "Paris", "Berlin"]
        summary = service.get_weather_summary(cities)
        
        assert len(summary) == 3
        assert all(city in summary for city in cities)
        assert all(isinstance(weather, WeatherData) for weather in summary.values() if weather)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
