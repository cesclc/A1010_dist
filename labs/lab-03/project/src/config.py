"""Application configuration management.

This module provides configuration management using Pydantic Settings
for type safety, validation, and environment variable support.
"""
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration with environment variable support.
    
    Attributes:
        APP_NAME: Name of the application
        DEBUG: Debug mode flag
        API_KEY: Optional API key for external services
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        MAX_RETRIES: Maximum number of retry attempts for API calls
        TIMEOUT: Request timeout in seconds
        
    Example:
        >>> config = Config()
        >>> config.APP_NAME
        'MyApp'
        >>> config = Config(DEBUG=True, API_KEY="secret123")
        >>> config.DEBUG
        True
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    APP_NAME: str = Field(
        default="MyApp",
        description="Application name"
    )
    
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    API_KEY: Optional[str] = Field(
        default=None,
        description="API key for external services"
    )
    
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    MAX_RETRIES: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retry attempts"
    )
    
    TIMEOUT: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Request timeout in seconds"
    )
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the allowed values."""
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in allowed_levels:
            raise ValueError(
                f"LOG_LEVEL must be one of {allowed_levels}, got '{v}'"
            )
        return v_upper
    
    @field_validator("API_KEY")
    @classmethod
    def validate_api_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate API key format if provided."""
        if v is not None and len(v) < 8:
            raise ValueError("API_KEY must be at least 8 characters long")
        return v


# Singleton instance for easy access
config = Config()


if __name__ == "__main__":
    # Example usage
    cfg = Config()
    print(f"App: {cfg.APP_NAME}")
    print(f"Debug: {cfg.DEBUG}")
    print(f"Log Level: {cfg.LOG_LEVEL}")
    print(f"Max Retries: {cfg.MAX_RETRIES}")
    print(f"Timeout: {cfg.TIMEOUT}s")
