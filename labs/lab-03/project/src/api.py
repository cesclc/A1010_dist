"""API client module with proper error handling and security practices.

This module demonstrates best practices for making HTTP requests including:
- Proper error handling and logging
- Type safety with type hints
- Timeout configurations
- Security headers
- PEP 8 compliance
"""
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException, Timeout, HTTPError
import logging

logger = logging.getLogger(__name__)


def fetch_data(
    url: str, 
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Fetch JSON data from URL with proper error handling.
    
    Args:
        url: The URL to fetch from
        timeout: Request timeout in seconds (default: 30)
        headers: Optional custom headers to include in request
        
    Returns:
        Dictionary containing the JSON response
        
    Raises:
        ValueError: If URL is invalid
        Timeout: If request times out
        HTTPError: If HTTP error status is returned
        RequestException: If the request fails for other reasons
        
    Example:
        >>> data = fetch_data("https://api.example.com/data")
        >>> print(data['status'])
        'ok'
    """
    if not url or not url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid URL: {url}")
    
    # Set default headers with User-Agent for identification
    default_headers = {
        'User-Agent': 'MyApp/1.0',
        'Accept': 'application/json'
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(
            url,
            timeout=timeout,
            headers=default_headers,
            # Security: Verify SSL certificates
            verify=True
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        logger.debug(f"Successfully fetched data from {url}")
        return response.json()
        
    except Timeout as e:
        logger.error(f"Request timeout for {url} after {timeout}s: {e}")
        raise
    except HTTPError as e:
        logger.error(f"HTTP error for {url}: {e}")
        raise
    except RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        raise


def process_response(resp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process API response and extract data if status is ok.
    
    Args:
        resp: Dictionary containing the API response
        
    Returns:
        Data from response if status is 'ok', None otherwise
        
    Raises:
        TypeError: If response is not a dictionary
        
    Example:
        >>> response = {'status': 'ok', 'data': {'value': 42}}
        >>> process_response(response)
        {'value': 42}
        >>> response = {'status': 'error'}
        >>> process_response(response)
        None
    """
    if not isinstance(resp, dict):
        raise TypeError(
            f"Response must be a dictionary, got {type(resp).__name__}"
        )
    
    status = resp.get('status')
    logger.debug(f"Processing response with status: {status}")
    
    if status == 'ok':
        return resp.get('data')
    
    # Log non-ok status for debugging
    error_msg = resp.get('error', 'Unknown error')
    logger.warning(f"Response status is not 'ok': {status}, error: {error_msg}")
    return None


def api_call(
    url: str, 
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """Make API call and process response with proper error handling.
    
    This is a high-level wrapper that combines fetching and processing
    with comprehensive error handling.
    
    Args:
        url: The URL to call
        timeout: Request timeout in seconds (default: 30)
        headers: Optional custom headers
        
    Returns:
        Processed data from the API, or None if the call fails
        
    Example:
        >>> result = api_call("https://api.example.com/endpoint")
        >>> if result:
        ...     print(f"Received data: {result}")
        ... else:
        ...     print("API call failed")
    """
    try:
        data = fetch_data(url, timeout=timeout, headers=headers)
        return process_response(data)
    except ValueError as e:
        logger.error(f"Validation error in API call: {e}")
        return None
    except Timeout as e:
        logger.error(f"Timeout in API call: {e}")
        return None
    except HTTPError as e:
        logger.error(f"HTTP error in API call: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in API call: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Test with a mock URL (will fail, but demonstrates error handling)
    test_url = "https://api.example.com/test"
    result = api_call(test_url)
    
    if result:
        print(f"Success: {result}")
    else:
        print("API call failed (expected for demo URL)")
