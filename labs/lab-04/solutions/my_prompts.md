# My Custom Prompts - Lab 04 Part 3

This document contains custom prompts for the three exercises in Part 3.

## Exercise 1: Refactor process_data() Function

### My Prompt

```
The process_data() function in the prompt-practice-project/app.py (lines 11-56) is handling 
too many responsibilities and needs to be refactored following SOLID principles, specifically 
the Single Responsibility Principle.

Current analysis:
- The function has 45 lines and performs 5 distinct operations
- It mixes business logic, data transformation, and persistence
- It's difficult to test individual pieces
- Error handling is inconsistent across sections

Please help me refactor this into a modular design with these separate functions:

1. **validate_input_data(data: List[Dict[str, Any]]) -> None**
   - Validate that required fields exist: 'id', 'value', 'category'
   - Validate data types (id: int, value: numeric, category: str)
   - Raise descriptive ValidationError with field name if validation fails
   - Should NOT modify the input data

2. **transform_to_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame**
   - Convert input list to pandas DataFrame
   - Cast 'value' column to float
   - Create 'processed' column (value * 2)
   - Convert 'category' to uppercase
   - Return the transformed DataFrame

3. **calculate_statistics(df: pd.DataFrame) -> Dict[str, float]**
   - Calculate: total, average, max, min from 'value' column
   - Return as dictionary
   - Handle empty DataFrame gracefully

4. **generate_category_report(df: pd.DataFrame) -> Dict[str, Dict[str, float]]**
   - Group by category
   - For each category calculate: count, total, average
   - Return nested dictionary structure
   - Use efficient pandas groupby operations

5. **save_processed_data(df: pd.DataFrame, engine) -> None**
   - Save DataFrame to SQL table 'processed_data'
   - Use 'append' mode
   - Include error handling for database errors
   - Log successful save operation

6. **process_data(data: List[Dict[str, Any]]) -> Dict[str, Any]** (refactored main function)
   - Orchestrate the above functions in order
   - Catch and re-raise exceptions with context
   - Maintain the same return format for backwards compatibility
   - Add logging at key steps

Requirements:
- All functions must have complete type hints
- All functions must have comprehensive docstrings (description, args, returns, raises, examples)
- Add error handling at each step with specific exception types
- Use Python 3.10+ features where appropriate
- Ensure functions are testable in isolation
- Add inline comments for complex logic

Please also suggest improvements to make the code more maintainable and explain the benefits 
of this refactoring approach.
```

### Rationale

This prompt is effective because:
- It references the specific file and line numbers
- It explains WHY refactoring is needed (testability, maintainability)
- It provides a clear decomposition strategy
- It specifies exact function signatures with types
- It requests comprehensive documentation
- It maintains backwards compatibility
- It asks for explanations to aid learning

---

## Exercise 2: Add Input Validation to /api/data Endpoint

### My Prompt

```
The /api/data POST endpoint in prompt-practice-project/app.py (lines 58-62) currently accepts 
any JSON data without validation, which can cause crashes and security issues.

Current problems:
- No check for Content-Type header
- No validation of JSON structure
- No type checking of fields
- No handling of malformed JSON
- process_data() crashes instead of returning proper HTTP errors

Please implement comprehensive input validation for this endpoint with the following:

1. **Request Validation**
   - Verify Content-Type is 'application/json'
   - Return 415 Unsupported Media Type if not
   - Catch JSON decode errors and return 400 Bad Request with helpful message

2. **Schema Validation**
   - Input must be a list of dictionaries
   - Each dictionary must have exactly these fields: 'id', 'value', 'category'
   - 'id': must be positive integer
   - 'value': must be numeric (int or float)
   - 'category': must be non-empty string
   - Return 400 Bad Request with specific field errors if validation fails

3. **Business Rule Validation**
   - List must contain at least 1 item
   - List must not exceed 1000 items (rate limiting)
   - All IDs must be unique
   - Category must be alphanumeric
   - Return 422 Unprocessable Entity for business rule violations

4. **Error Response Format**
   - Use consistent error response structure:
     ```json
     {
       "error": "Validation failed",
       "details": ["Specific error 1", "Specific error 2"],
       "status": 400
     }
     ```

5. **Implementation Approach**
   - Create a validate_request_data() helper function
   - Use try/except to catch validation errors
   - Wrap process_data() call in try/except for graceful error handling
   - Return appropriate HTTP status codes (200, 400, 415, 422, 500)

6. **Logging**
   - Log validation failures with request details
   - Log successful processing
   - Don't log sensitive data

Please also:
- Use pydantic for schema validation if it simplifies the code
- Add type hints to the endpoint function
- Include docstring explaining the endpoint behavior and error responses
- Provide example curl commands demonstrating valid and invalid requests
- Suggest security best practices for this endpoint

Testing: Include a few example requests (valid and invalid) that I can test with.
```

### Rationale

This prompt is effective because:
- It identifies the specific endpoint and current issues
- It breaks down validation into logical categories
- It specifies exact error codes and response formats
- It requests both implementation and testing examples
- It mentions security considerations
- It suggests using appropriate libraries (pydantic)
- It's structured for easy implementation

---

## Exercise 3: Implement Database Connection Error Handling

### My Prompt

```
The database connection in prompt-practice-project/app.py (line 9) is created without any error 
handling, which can cause the entire application to crash on startup or during database operations.

Current code:
```python
engine = create_engine('sqlite:///example.db')
```

Problems:
- No error handling if database file is locked or inaccessible
- No connection pooling configuration
- No retry logic for transient failures
- No graceful degradation if database is unavailable
- save_processed_data() can crash the entire request

Please implement robust database connection handling with these features:

1. **Connection Initialization**
   - Wrap create_engine in try/except block
   - Handle common SQLAlchemy exceptions (OperationalError, DatabaseError)
   - Implement connection pooling with appropriate pool_size and max_overflow
   - Add connection timeout configuration
   - Log successful connection with database path

2. **Connection Health Check**
   - Create a check_database_connection() function
   - Test connection on startup
   - Return boolean indicating if database is available
   - Log connection status

3. **Retry Logic**
   - Implement exponential backoff for transient failures
   - Create a retry_database_operation() decorator
   - Max retries: 3
   - Initial delay: 1 second
   - Backoff factor: 2
   - Log each retry attempt

4. **Graceful Degradation**
   - If database is unavailable, application should still start
   - save_processed_data() should catch exceptions and log errors
   - Return response to user even if save fails
   - Include warning in response if data wasn't persisted

5. **Context Manager**
   - Create a database_session() context manager
   - Properly handle connection acquisition and release
   - Ensure connections are returned to pool
   - Handle exceptions within the context

6. **Configuration**
   - Make database URL configurable via environment variable
   - Provide sensible defaults
   - Document configuration options

Implementation structure:
```python
class DatabaseManager:
    def __init__(self, database_url: str, ...):
        # Initialize with error handling
        
    def check_connection(self) -> bool:
        # Test connection
        
    def get_session(self):
        # Return session with error handling
        
    @retry_on_failure(max_attempts=3)
    def execute_with_retry(self, func):
        # Execute database operation with retry logic
```

Please:
- Use SQLAlchemy best practices
- Add comprehensive logging at each step
- Include type hints and docstrings
- Handle all likely exception types
- Provide configuration examples
- Explain the rationale for each design decision

Testing: Suggest how to test the error handling without breaking the actual database.
```

### Rationale

This prompt is effective because:
- It identifies the exact line with the problem
- It lists specific issues with the current approach
- It provides a detailed implementation structure
- It specifies error handling strategies (retry, degradation)
- It requests a specific class design with methods
- It asks for configuration flexibility
- It requests testing guidance
- It asks for explanations

---

## Prompt Quality Self-Assessment

For each prompt above, I've ensured:

✓ **Specificity**: Referenced exact files, functions, line numbers
✓ **Context**: Explained current problems and why change is needed
✓ **Structure**: Used clear numbered lists and sections
✓ **Requirements**: Stated explicit expectations for each component
✓ **Constraints**: Mentioned compatibility, security, performance
✓ **Deliverables**: Requested code, documentation, examples
✓ **Learning**: Asked for rationale and best practices
✓ **Testability**: Requested testing strategies

## Lessons Learned

1. **Be Specific**: The more specific the prompt, the better the response
2. **Provide Context**: Explaining "why" helps AI understand intent
3. **Structure Matters**: Numbered lists and sections improve clarity
4. **Request Examples**: Always ask for usage examples and test cases
5. **Think About Edge Cases**: Mention potential failure scenarios
6. **Ask for Explanations**: This helps you learn, not just get code
