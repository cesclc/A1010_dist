# Lab 04 Quick Reference - Prompt Engineering

## Quick Start

```bash
# Setup
cd labs/lab-04/solutions
source ../../.venv/bin/activate
pip install -r requirements.txt

# Run app
python app_improved.py

# Run tests
cd ../tests
pytest test_app_improved.py -v
```

## Effective Prompt Template

```
[CONTEXT]
I'm working on [specific file/function] at line [X].
The current code [describe issue/behavior].

[PROBLEM]
This causes [specific problem] because [reason].

[REQUEST]
Please help me:
1. [Specific task with details]
2. [Another specific task]
   - [Sub-requirement]
   - [Sub-requirement]

[CONSTRAINTS]
Requirements:
- Must [constraint 1]
- Should [constraint 2]
- Need to handle [edge case]

[DELIVERABLES]
Please provide:
- [Code/tests/documentation]
- [Examples demonstrating usage]
- [Explanation of approach]
```

## Checklist for Good Prompts

Before submitting a prompt, verify:

- [ ] Named specific file and function
- [ ] Included line numbers if relevant
- [ ] Explained current problem/behavior
- [ ] Listed specific requirements (numbered)
- [ ] Mentioned constraints and requirements
- [ ] Requested examples or test cases
- [ ] Asked for explanations when learning
- [ ] Structured with clear sections

## Common Mistakes to Avoid

| ❌ Bad | ✓ Good |
|--------|---------|
| "Fix this" | "Fix the TypeError in process_user_data() (line 85) when input is None" |
| "Make it faster" | "Optimize process_data() for 100K+ rows by improving pandas operations" |
| "Add tests" | "Write pytest tests for validate_input_data() covering edge cases" |
| "Refactor" | "Split process_data() into validate(), transform(), calculate() functions" |

## Quick Patterns

### Debugging
```
In [function] at line [X], I get error "[error message]" when [condition].
Please:
1. Explain why this occurs
2. Add input validation
3. Implement error handling
4. Add logging
```

### Refactoring
```
The [function] in [file] (lines [X-Y]) handles [list responsibilities].
Please split into:
1. [function_name](args) -> return_type  # Purpose
2. [function_name](args) -> return_type  # Purpose
Each with type hints, docstrings, and error handling.
```

### Adding Features
```
The [endpoint/function] currently [current behavior].
Please add [feature] that:
1. [Requirement 1 with details]
2. [Requirement 2 with details]
Maintain backwards compatibility and add tests.
```

### Performance
```
The [function] is slow with [data size/condition].
Please optimize by:
1. Identifying bottlenecks
2. Suggesting efficient alternatives
3. Providing benchmarks
Context: [runtime environment, constraints]
```

## Iteration Example

### Iteration 1: Too Vague
```
Make the sorting function better
```
Result: ❌ Generic, unclear suggestions

### Iteration 2: Better
```
Improve basic_sort() with a faster algorithm
```
Result: ⚠️ Better but missing details

### Iteration 3: Good
```
Replace bubble sort in basic_sort() (line 67) with merge sort.
Add type hints, docstring, and handle edge cases.
```
Result: ✓ Specific, actionable

### Iteration 4: Excellent
```
The basic_sort() function in app.py (lines 67-80) uses bubble sort O(n²).
For sorting 1000+ integers, this is too slow.

Please refactor to:
1. Use merge sort (O(n log n))
2. Return NEW sorted array (don't modify input)
3. Add type hints: def merge_sort(arr: List[int]) -> List[int]
4. Add docstring with complexity analysis
5. Handle edge cases: empty [], single [x], already sorted

Maintain backwards compatibility with same function name.
```
Result: ✓✓ Complete, production-ready implementation

## File Reference

- **Improved Prompts:** `solutions/improved_prompts.md`
- **Custom Prompts:** `solutions/my_prompts.md`
- **Complete Solution:** `solutions/app_improved.py`
- **Tests:** `tests/test_app_improved.py`
- **Full Documentation:** `solutions/SOLUTIONS.md`

## Key Principles

1. **Be Specific:** Files, functions, line numbers
2. **Provide Context:** Current state, why change needed
3. **Structure Clearly:** Numbered lists, sections
4. **Request Deliverables:** Code, tests, docs, examples
5. **Mention Constraints:** Compatibility, performance, security
6. **Iterate:** Refine based on results

## Example Requests

### Good Request for Refactoring
```
The process_data() function in prompt-practice-project/app.py (lines 11-56)
does 5 different things: validation, transformation, statistics, reporting,
and database operations.

Please refactor following Single Responsibility Principle by extracting:

1. validate_input_data(data: List[Dict[str, Any]]) -> None
   - Check required fields: id, value, category
   - Validate types: id (int), value (numeric), category (str)
   - Raise ValidationError with specific field if fails

2. transform_to_dataframe(data: List[Dict]) -> pd.DataFrame
   - Convert to DataFrame
   - Cast value to float, category to uppercase
   - Add processed column (value * 2)

[Continue with other functions...]

Please add:
- Complete type hints
- Comprehensive docstrings (args, returns, raises, examples)
- Error handling at each step
- Maintain same external interface for backwards compatibility
```

### Good Request for Adding Validation
```
The /api/data POST endpoint in app.py (lines 58-62) accepts any JSON
without validation, causing crashes and security issues.

Please implement:

1. Content-Type validation (return 415 if not JSON)
2. JSON parsing with error handling (return 400 on malformed JSON)
3. Schema validation:
   - Input must be list of dicts
   - Required fields: id (positive int), value (numeric), category (non-empty str)
   - IDs must be unique
   - Max 1000 items
4. Error response format:
   {"error": "Type", "details": ["Specific errors"], "status": code}
5. Appropriate HTTP status codes (200, 400, 415, 422, 500)

Include example curl commands for testing valid and invalid requests.
```

## Testing Your Prompts

After getting a response:

1. **Check Completeness:** Did it address all requirements?
2. **Verify Quality:** Type hints? Docstrings? Error handling?
3. **Test Code:** Does it work? Any edge cases missed?
4. **Evaluate Explanation:** Did you understand the approach?
5. **Identify Gaps:** What could be improved?
6. **Refine Prompt:** Iterate based on gaps

## Pro Tips

1. **Save Good Prompts:** Reuse effective patterns
2. **Start Specific:** Easier to broaden than narrow
3. **Request Examples:** Helps verify understanding
4. **Ask "Why":** Learn don't just get code
5. **Iterate Freely:** First prompt rarely perfect
6. **Include Context:** More detail = better results
7. **Be Explicit:** Don't assume AI knows your intent

## Common Scenarios

| Scenario | Key Elements to Include |
|----------|------------------------|
| **Bug Fix** | Error message, when it occurs, expected behavior |
| **Refactoring** | Current structure, desired structure, constraints |
| **New Feature** | Requirements, edge cases, integration points |
| **Optimization** | Performance metrics, constraints, acceptable trade-offs |
| **Testing** | What to test, test framework, coverage expectations |
| **Documentation** | Audience, format, level of detail |

## Remember

- Good prompts lead to good code
- Specificity trumps verbosity
- Context enables better solutions
- Iteration improves results
- Learning compounds over time

## Next Steps

1. Review the complete solutions in `solutions/`
2. Try the prompts with an AI assistant
3. Compare results with provided implementations
4. Practice writing prompts for your own code
5. Build a library of effective prompt patterns
