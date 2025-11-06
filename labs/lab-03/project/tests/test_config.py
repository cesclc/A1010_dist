"""Unit tests for config module.

Tests configuration validation and loading.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config


class TestConfig:
    """Tests for Config class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = Config()
        assert config.APP_NAME == "MyApp"
        assert config.DEBUG is False
        assert config.API_KEY is None
        assert config.LOG_LEVEL == "INFO"
        assert config.MAX_RETRIES == 3
        assert config.TIMEOUT == 30
    
    def test_custom_values(self):
        """Test setting custom values."""
        config = Config(
            APP_NAME="TestApp",
            DEBUG=True,
            API_KEY="test_key_12345",
            LOG_LEVEL="DEBUG"
        )
        assert config.APP_NAME == "TestApp"
        assert config.DEBUG is True
        assert config.API_KEY == "test_key_12345"
        assert config.LOG_LEVEL == "DEBUG"
    
    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid log levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = Config(LOG_LEVEL=level)
            assert config.LOG_LEVEL == level
        
        # Invalid log level
        with pytest.raises(ValueError, match="LOG_LEVEL must be one of"):
            Config(LOG_LEVEL="INVALID")
    
    def test_log_level_case_insensitive(self):
        """Test that log level is case-insensitive."""
        config = Config(LOG_LEVEL="info")
        assert config.LOG_LEVEL == "INFO"
        
        config = Config(LOG_LEVEL="DeBuG")
        assert config.LOG_LEVEL == "DEBUG"
    
    def test_api_key_validation(self):
        """Test API key validation."""
        # Valid API key
        config = Config(API_KEY="validkey123")
        assert config.API_KEY == "validkey123"
        
        # Too short API key
        with pytest.raises(ValueError, match="API_KEY must be at least 8 characters"):
            Config(API_KEY="short")
    
    def test_max_retries_bounds(self):
        """Test MAX_RETRIES boundary validation."""
        # Valid values
        Config(MAX_RETRIES=0)
        Config(MAX_RETRIES=5)
        Config(MAX_RETRIES=10)
        
        # Invalid values (pydantic validates bounds)
        with pytest.raises(ValueError):
            Config(MAX_RETRIES=-1)
        
        with pytest.raises(ValueError):
            Config(MAX_RETRIES=11)
    
    def test_timeout_bounds(self):
        """Test TIMEOUT boundary validation."""
        # Valid values
        Config(TIMEOUT=1)
        Config(TIMEOUT=60)
        Config(TIMEOUT=300)
        
        # Invalid values
        with pytest.raises(ValueError):
            Config(TIMEOUT=0)
        
        with pytest.raises(ValueError):
            Config(TIMEOUT=301)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
