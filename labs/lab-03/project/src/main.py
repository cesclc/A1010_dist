"""Main application entry point.

This module demonstrates proper error handling and function integration
from the utils module.
"""
from utils import process_data, validate_input, format_output


def main() -> None:
    """Main application logic with proper error handling.
    
    Processes a list of numbers and displays the result.
    Includes validation and comprehensive error handling.
    """
    try:
        data = [1, 2, 3]
        
        # Validate input before processing
        if validate_input(data):
            processed = process_data(data)
            print(format_output(processed))
            
    except TypeError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
