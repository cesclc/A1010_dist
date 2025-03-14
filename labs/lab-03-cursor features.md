# Lab Exercise 3: Advanced Cursor Features

__Objective__: Master advanced features of Cursor AI IDE to enhance your coding workflow and productivity.

## Prerequisites
- Completion of Lab Exercise 1: Getting Started with Cursor
- Basic understanding of Git and collaborative coding
- A sample project with multiple files (provided in setup)

## Setup
Before starting the lab, create a small project structure:

```
project/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config.py
├── tests/
│   └── test_utils.py
└── README.md
```

You can create this structure using the following commands in the terminal:
```bash
mkdir -p project/src project/tests
touch project/src/{main,utils,config}.py project/tests/test_utils.py project/README.md
```

## Exercise Overview
This lab explores advanced Cursor features through practical scenarios developers encounter daily.

### Part 1: Advanced Code Context and References

1. In `utils.py`, paste this code:
```python
def process_data(data):
    return [x * 2 for x in data]

def validate_input(data):
    if not isinstance(data, list):
        raise TypeError("Expected list")
    return True

def format_output(data):
    return f"Result: {data}"
```

2. In `main.py`, add:
```python
from utils import process_data, validate_input, format_output

def main():
    data = [1, 2, 3]
    processed = process_data(data)
    print(format_output(processed))
```

3. Complete these tasks using Cursor's advanced referencing:
   - Ask Cursor to explain how `main.py` uses the functions from `utils.py`
   - Request suggestions for improving the code organization
   - Ask about potential circular dependencies

<details>
<summary>Reveal Solution</summary>

Example interaction:
```
You: "Analyze how main.py uses the functions from utils.py and suggest improvements"

Assistant will suggest:
- Moving input validation before processing
- Creating a proper module structure
- Adding error handling in main()
- Suggested improved code:

```python
# main.py
from utils import process_data, validate_input, format_output

def main():
    try:
        data = [1, 2, 3]
        if validate_input(data):
            processed = process_data(data)
            print(format_output(processed))
    except TypeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```
</details>

### Part 2: Code Snippets and Templates

1. Use Cursor to create these common code patterns:
   - Create a Python logger configuration
   - Add a context manager class
   - Generate a FastAPI endpoint template

2. In `config.py`, ask Cursor to generate a configuration class using best practices:
   - Should support environment variables
   - Include type hints
   - Add validation

<details>
<summary>Reveal Solution</summary>

```python
from typing import Optional
from pydantic import BaseSettings

class Config(BaseSettings):
    """Application configuration."""
    
    APP_NAME: str = "MyApp"
    DEBUG: bool = False
    API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
```
</details>

### Part 3: Advanced Debugging Assistance

1. Add this intentionally buggy code to `utils.py`:
```python
def calculate_statistics(numbers):
    stats = {
        'mean': sum(numbers) / len(numbers),
        'median': sorted(numbers)[len(numbers) // 2],
        'range': max(numbers) - min(numbers)
    }
    return stats

test_data = [1, 2, 2, 3, 4, 4, 5]
empty_data = []
result1 = calculate_statistics(test_data)
result2 = calculate_statistics(empty_data)
```

2. Use Cursor's debugging features to:
   - Identify potential issues
   - Add proper error handling
   - Generate unit tests
   - Add logging for debugging

<details>
<summary>Reveal Solution</summary>

```python
import logging
from typing import List, Dict
from statistics import mean, median

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """Calculate statistical measures for a list of numbers."""
    logger.info(f"Calculating statistics for {len(numbers)} numbers")
    
    if not numbers:
        raise ValueError("Cannot calculate statistics for empty list")
        
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
```
</details>

### Part 4: Code Reviews and Best Practices

1. Create a new feature branch in your project
2. Add this code to `src/api.py`:
```python
from typing import Dict, Any
import requests

def fetch_data(url: str) -> Dict[Any, Any]:
    r = requests.get(url)
    return r.json()

def process_response(resp):
    if resp['status'] == 'ok':
        return resp['data']
    return None

def api_call(url: str):
    try:
        data = fetch_data(url)
        return process_response(data)
    except:
        print('Error occurred')
        return None
```

3. Use Cursor to:
   - Review the code for security issues
   - Check for PEP 8 compliance
   - Identify error handling problems
   - Suggest improvements for type safety

<details>
<summary>Reveal Solution</summary>

```python
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

def fetch_data(url: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Fetch JSON data from URL with proper error handling.
    
    Args:
        url: The URL to fetch from
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing the JSON response
        
    Raises:
        RequestException: If the request fails
    """
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={'User-Agent': 'MyApp/1.0'}
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        raise

def process_response(resp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process API response and extract data if status is ok."""
    if not isinstance(resp, dict):
        raise TypeError("Response must be a dictionary")
        
    return resp.get('data') if resp.get('status') == 'ok' else None

def api_call(url: str) -> Optional[Dict[str, Any]]:
    """Make API call and process response with proper error handling."""
    try:
        data = fetch_data(url)
        return process_response(data)
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None
```
</details>


### Final Challenge: Real-World Integration

Create a complete feature implementing all advanced Cursor features:

1. Create a new module that:
   - Fetches data from an API
   - Processes the data using functions from multiple files
   - Implements proper error handling and logging
   - Includes type hints and documentation
   - Has comprehensive tests

2. Use all of Cursor's advanced features:
   - Code referencing across files
   - Debugging assistance
   - Code review
   - Documentation generation
   - Collaborative tools

<details>
<summary>Reveal Solution</summary>

Example project structure and implementation:

```python
# weather_service.py
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from dataclasses import dataclass
from .utils import validate_input, format_output
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    timestamp: datetime

class WeatherService:
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.API_KEY
        
    async def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Fetch and process weather data for a given city.
        
        Args:
            city: Name of the city
            
        Returns:
            WeatherData object or None if request fails
        """
        try:
            validate_input(city)
            raw_data = await self._fetch_weather(city)
            return self._process_weather_data(raw_data)
        except Exception as e:
            logger.error(f"Failed to get weather for {city}: {e}")
            return None
            
    # Additional methods and implementation...
```
</details>

## Wrap-up
After completing this lab, you should be comfortable with:
- Using advanced code referencing and context
- Implementing code snippets and templates
- Utilizing debugging assistance
- Conducting code reviews
- Using collaborative features
- Integrating multiple features in a real-world scenario

## Next Steps
- Review the official Cursor documentation for additional features
- Practice using these features in your daily workflow
- Share your knowledge with team members

