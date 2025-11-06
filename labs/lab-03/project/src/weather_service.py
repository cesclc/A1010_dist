"""Weather service module integrating all learned patterns.

This module demonstrates a real-world integration combining:
- Code referencing across files (utils, config, api)
- Proper error handling and logging
- Type hints and documentation
- Dataclasses for structured data
- Async/await patterns (simulated with sync for simplicity)
"""
from typing import Optional, Dict, Any
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from utils import validate_input, format_output
from config import Config
from api import fetch_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class WeatherData:
    """Structured weather data.
    
    Attributes:
        temperature: Temperature in Celsius
        humidity: Humidity percentage (0-100)
        description: Weather description
        city: City name
        timestamp: When the data was fetched
    """
    temperature: float
    humidity: float
    description: str
    city: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format timestamp."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"Weather in {self.city}:\n"
            f"  Temperature: {self.temperature}°C\n"
            f"  Humidity: {self.humidity}%\n"
            f"  Conditions: {self.description}\n"
            f"  Updated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class WeatherService:
    """Service for fetching and processing weather data.
    
    This class integrates configuration management, API calls,
    data validation, and error handling.
    
    Example:
        >>> config = Config(API_KEY="your_api_key")
        >>> service = WeatherService(config)
        >>> weather = service.get_weather("London")
        >>> if weather:
        ...     print(weather)
    """
    
    def __init__(self, config: Config):
        """Initialize weather service with configuration.
        
        Args:
            config: Configuration object with API settings
        """
        self.config = config
        self.api_key = config.API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            logger.warning("No API key configured for weather service")
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        """Fetch and process weather data for a given city.
        
        Args:
            city: Name of the city
            
        Returns:
            WeatherData object or None if request fails
            
        Example:
            >>> service = WeatherService(Config())
            >>> weather = service.get_weather("Paris")
            >>> if weather:
            ...     print(f"Temperature: {weather.temperature}°C")
        """
        try:
            # Validate input
            if not city or not isinstance(city, str):
                raise ValueError("City name must be a non-empty string")
            
            city = city.strip()
            logger.info(f"Fetching weather for city: {city}")
            
            # Fetch raw data from API
            raw_data = self._fetch_weather(city)
            
            # Process and structure the data
            return self._process_weather_data(raw_data, city)
            
        except ValueError as e:
            logger.error(f"Validation error for {city}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to get weather for {city}: {e}")
            return None
    
    def _fetch_weather(self, city: str) -> Dict[str, Any]:
        """Fetch raw weather data from API.
        
        Args:
            city: City name
            
        Returns:
            Raw API response
            
        Raises:
            Exception: If API call fails
        """
        params = {
            'q': city,
            'appid': self.api_key or 'demo',
            'units': 'metric'
        }
        
        # Construct URL with parameters
        url = f"{self.base_url}?q={params['q']}&appid={params['appid']}&units={params['units']}"
        
        # Use configured timeout and retry settings
        raw_data = fetch_data(
            url,
            timeout=self.config.TIMEOUT
        )
        
        return raw_data
    
    def _process_weather_data(
        self, 
        raw_data: Dict[str, Any], 
        city: str
    ) -> WeatherData:
        """Process raw API response into structured WeatherData.
        
        Args:
            raw_data: Raw API response
            city: City name
            
        Returns:
            Structured WeatherData object
            
        Raises:
            KeyError: If required fields are missing
            ValueError: If data is invalid
        """
        try:
            main = raw_data['main']
            weather = raw_data['weather'][0]
            
            weather_data = WeatherData(
                temperature=float(main['temp']),
                humidity=int(main['humidity']),
                description=weather['description'],
                city=city,
                timestamp=datetime.now()
            )
            
            logger.info(f"Successfully processed weather data for {city}")
            return weather_data
            
        except KeyError as e:
            logger.error(f"Missing required field in API response: {e}")
            raise ValueError(f"Invalid API response format: {e}")
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting weather data types: {e}")
            raise ValueError(f"Invalid data types in API response: {e}")
    
    def get_weather_summary(self, cities: list[str]) -> Dict[str, Optional[WeatherData]]:
        """Get weather for multiple cities.
        
        Args:
            cities: List of city names
            
        Returns:
            Dictionary mapping city names to WeatherData objects
            
        Example:
            >>> service = WeatherService(Config())
            >>> summary = service.get_weather_summary(["London", "Paris", "Berlin"])
            >>> for city, weather in summary.items():
            ...     if weather:
            ...         print(f"{city}: {weather.temperature}°C")
        """
        results = {}
        
        for city in cities:
            weather = self.get_weather(city)
            results[city] = weather
            
        return results


def main() -> None:
    """Example usage of the weather service."""
    # Load configuration
    config = Config()
    
    # Create service
    service = WeatherService(config)
    
    # Test cities
    test_cities = ["London", "Paris", "Tokyo"]
    
    print("Weather Service Demo")
    print("=" * 50)
    
    # Get weather for multiple cities
    summary = service.get_weather_summary(test_cities)
    
    for city, weather in summary.items():
        if weather:
            print(f"\n{weather}")
        else:
            print(f"\nFailed to fetch weather for {city}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
