# Lab 03 Quick Reference Guide

## Overview
This lab demonstrates advanced AI development tool features through practical implementations.

## File Locations

```
labs/lab-03/project/
├── src/                     # All source code
│   ├── main.py             # Entry point
│   ├── utils.py            # Utilities & statistics
│   ├── config.py           # Configuration
│   ├── api.py              # HTTP client
│   └── weather_service.py  # Integration example
├── tests/                   # Unit tests
├── SOLUTIONS.md            # Detailed solutions
└── README.md               # Project overview
```

## Quick Start

```bash
# Navigate to project
cd labs/lab-03/project

# Install dependencies (optional for basic examples)
pip install -r requirements.txt

# Run examples
python src/main.py              # Basic processing
python src/utils.py             # Statistics demo
python src/api.py               # API client demo
python src/config.py            # Config demo

# Run tests
pytest tests/test_utils.py -v  # Runs without dependencies
```

## Exercise Solutions at a Glance

### Part 1: Advanced Code Context
- **File**: `src/utils.py` + `src/main.py`
- **Features**: Error handling, validation, type hints
- **Key Function**: `validate_input()` → `process_data()` → `format_output()`

### Part 2: Code Snippets & Templates
- **File**: `src/config.py`
- **Features**: Pydantic Settings, environment variables, validation
- **Key Class**: `Config` with field validators

### Part 3: Advanced Debugging
- **File**: `src/utils.py` (calculate_statistics)
- **Features**: Logging, error handling, edge case coverage
- **Fixed Issues**: Empty list, non-numeric values, proper statistics

### Part 4: Code Reviews
- **File**: `src/api.py`
- **Improvements**:
  - ✓ Security (SSL, User-Agent)
  - ✓ Timeout configuration
  - ✓ Proper error handling
  - ✓ Type safety
  - ✓ PEP 8 compliance

### Final Challenge: Weather Service
- **File**: `src/weather_service.py`
- **Integration**: Uses config, api, utils modules
- **Features**: DataClass, service pattern, batch processing

## Code Patterns Demonstrated

### Error Handling Pattern
```python
try:
    if validate_input(data):
        result = process_data(data)
        print(format_output(result))
except TypeError as e:
    print(f"Validation Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

### Configuration Pattern
```python
from config import Config

config = Config(
    DEBUG=True,
    API_KEY="your_key",
    LOG_LEVEL="DEBUG"
)
```

### API Client Pattern
```python
from api import api_call

result = api_call(
    url="https://api.example.com/data",
    timeout=30,
    headers={"Custom-Header": "value"}
)
```

### Service Pattern
```python
from weather_service import WeatherService
from config import Config

service = WeatherService(Config(API_KEY="key"))
weather = service.get_weather("London")
if weather:
    print(weather)
```

## Testing Examples

### Run Specific Tests
```bash
# All tests for a module
pytest tests/test_utils.py -v

# Specific test class
pytest tests/test_utils.py::TestCalculateStatistics -v

# Specific test
pytest tests/test_utils.py::TestCalculateStatistics::test_empty_list_raises_error -v
```

### Test Results
- `test_utils.py`: 19 tests ✓
- `test_api.py`: 12 tests (requires mocking)
- `test_config.py`: 8 tests (requires pydantic)
- `test_weather_service.py`: 10 tests (requires pydantic)

## Key Takeaways

1. **Type Hints**: Every function has complete type annotations
2. **Error Handling**: Specific exceptions with meaningful messages
3. **Logging**: Structured logging at INFO, DEBUG, ERROR levels
4. **Documentation**: Comprehensive docstrings with examples
5. **Testing**: Unit tests with proper mocking
6. **Security**: Input validation, SSL verification, timeouts
7. **Best Practices**: PEP 8, clean code, separation of concerns

## Common Issues & Solutions

### Import Errors
**Issue**: "Import could not be resolved"
**Solution**: Install dependencies or add src to PYTHONPATH
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Pydantic Errors
**Issue**: "No module named 'pydantic'"
**Solution**: Install dependencies
```bash
pip install pydantic pydantic-settings
```

### Test Collection Errors
**Issue**: Tests can't import modules
**Solution**: Run from project root with correct path
```bash
cd labs/lab-03/project
pytest tests/ -v
```

## Advanced Usage

### Environment Variables
Create `.env` file in project root:
```env
APP_NAME=MyWeatherApp
DEBUG=true
API_KEY=your_api_key_here
LOG_LEVEL=DEBUG
MAX_RETRIES=5
TIMEOUT=60
```

### Custom Configuration
```python
from config import Config

config = Config(
    _env_file="custom.env",  # Custom env file
    API_KEY="override_key"   # Override specific values
)
```

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

## Next Steps

1. Extend the weather service with caching
2. Add async/await for concurrent API calls
3. Implement rate limiting
4. Add database persistence
5. Create a REST API wrapper
6. Add monitoring and metrics

## Resources

- Full solutions: `SOLUTIONS.md`
- Test examples: `tests/` directory
- Lab instructions: `../lab-03-cursor features.md`
