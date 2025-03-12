---
title: "Lab 3A: Prompt Engineering for Development"
subtitle: "Learning to Write Effective Prompts for AI Coding Assistants"
author: Peter Munro
---

# Lab 3A: Prompt Engineering for Development

## Overview

This lab will help you develop practical skills in writing effective prompts for AI coding assistants. You'll learn to identify what makes a prompt effective or ineffective, and practice improving prompts through iterative refinement using a real Python project.

## Learning Objectives

By completing this lab, you will be able to:
- Identify characteristics of effective and ineffective prompts
- Transform vague prompts into clear, specific instructions
- Apply best practices in prompt engineering
- Evaluate and improve prompt effectiveness
- Practice with real code in a Flask application

## Lab Structure

This is a hands-on lab where you'll:
1. Analyze example prompts
2. Improve ineffective prompts
3. Create your own prompts
4. Test and refine your prompts with a real codebase

## Setup

Before starting the exercises:
1. Navigate to the `prompt-practice-project` directory
2. Follow the setup instructions in the README.md file
3. Familiarize yourself with the codebase

## Part 1: Analyzing Prompt Effectiveness

Below are pairs of prompts for the same task. For each pair, analyze why one is more effective than the other. You can test these prompts against the provided practice project in the `prompt-practice-project` directory.

### Example 1: Writing a Function

**Ineffective Prompt:**
```
Write a function that sorts stuff
```

**Effective Prompt:**
```
Looking at the basic_sort() function in app.py, please improve it by:
1. Adding Python type hints for an array of integers
2. Adding a comprehensive docstring with examples
3. Implementing proper empty input handling
4. Using merge sort instead of bubble sort for better performance
5. Making it return a new sorted array instead of modifying the input

The improved function should maintain the same interface but be more robust and efficient.
```

**Why the second is better:**
- Specifies the exact function to improve
- Names the specific sorting algorithm (merge sort)
- Defines the input type (array of integers)
- Requests specific features (type hints, docstring)
- Clarifies behavior (not modifying original array)
- Mentions edge cases to handle (empty arrays)

### Example 2: Debugging Code

**Ineffective Prompt:**
```
My code doesn't work, please fix it
```

**Effective Prompt:**
```
In the process_user_data() function in app.py, I'm getting a "TypeError: cannot unpack non-iterable NoneType object" when the input is None. Please help me:
1. Identify why this error occurs
2. Add proper input validation
3. Implement error handling that returns a meaningful error message
4. Add type hints and documentation
```

**Why the second is better:**
- Identifies the specific function
- Includes the exact error message
- Provides context about when the error occurs
- Requests specific improvements
- Structures the request clearly

## Part 2: Practice Improving Prompts

Try improving these ineffective prompts. Write your improved version, then compare with the suggested improvements below.

### Exercise 1
**Ineffective Prompt:**
```
Make my code faster
```

Take a moment to improve this prompt. What additional information would make it more effective?

<details>
<summary>Click to see a suggested improvement</summary>

```
The process_data() function in app.py is processing large datasets inefficiently. Please analyze the code for performance bottlenecks and suggest optimizations, specifically:
1. Identify inefficient pandas operations
2. Suggest more memory-efficient alternatives
3. Recommend any relevant pandas optimizations or tools
4. Provide example code for the optimized solution
5. Consider parallel processing for the report generation
```
</details>

### Exercise 2
**Ineffective Prompt:**
```
Add tests
```

Improve this prompt before checking the suggestion.

<details>
<summary>Click to see a suggested improvement</summary>

```
Please help me write unit tests for the process_data() function in app.py using pytest:

Requirements for the tests:
1. Test successful data processing with valid input
2. Test error handling with missing required fields
3. Test different data types and categories
4. Test edge cases (empty input, single record, large datasets)
5. Include fixtures for test data
6. Add docstrings explaining each test case
```
</details>

## Part 3: Creating Your Own Prompts

Now it's your turn to write effective prompts for real tasks. Use the code in the `prompt-practice-project` directory for these exercises:

1. Write a prompt to refactor the complex `process_data()` function into smaller, more manageable pieces
2. Write a prompt to add input validation to the `/api/data` REST API endpoint
3. Write a prompt to implement proper error handling for the database connection

Write your prompts first, then test them with an AI coding assistant.

## Part 4: Testing and Refinement

For this part:

1. Take one of the prompts you wrote in Part 3
2. Test it with an AI coding assistant on the practice project
3. Analyze the response:
   - Did you get what you needed?
   - Was anything missing?
   - Was the response too broad or too narrow?
4. Refine your prompt based on the response
5. Test again with the refined prompt
6. Document what improved between iterations

## Best Practices Checklist

Use this checklist when crafting prompts:

- [ ] Specified programming language/framework
- [ ] Included relevant code or context
- [ ] Defined clear requirements
- [ ] Mentioned important constraints
- [ ] Listed edge cases to handle
- [ ] Requested specific output format
- [ ] Asked for explanations when needed
- [ ] Structured the request logically

## Common Patterns for Effective Prompts

1. **Context Setting**
   ```
   I'm working on [specific file/function] in the project.
   The current code [describe current state/issue].
   ```

2. **Specific Requirements**
   ```
   Please help me:
   1. [First specific task]
   2. [Second specific task]
   3. [Third specific task]
   ```

3. **Constraints and Preferences**
   ```
   Requirements:
   - Must be compatible with [version/environment]
   - Should follow [specific pattern/practice]
   - Need to handle [specific edge cases]
   ```

## Lab Challenge

Take one of the tasks from the practice project and:
1. Write an initial prompt
2. Test it
3. Refine it based on the response
4. Document what you learned about effective prompt writing

Share your experience and insights with others to help build better understanding of effective prompt engineering.

## Key Takeaways

Remember:
- Good prompts are specific, contextual, and structured
- Iteration is key to improving prompt effectiveness
- Different tasks may require different prompt structures
- Always include relevant context and constraints
- Be explicit about what you want to learn or achieve