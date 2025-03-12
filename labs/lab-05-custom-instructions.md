---
title: "Lab Exercise: Custom Instructions in Cursor"
subtitle: "Practice Creating and Using .cursorrules"
author: Peter Munro
---

## Overview

In this lab, you'll practice creating and using custom instructions for Cursor AI through the `.cursorrules` file. You'll see how different instructions affect the AI's code suggestions.

## Exercise 1: Global Custom Instructions

1. In Cursor, you can specify global custom instructions:
    - Go to `Cursor Settings` > `General` > `Rules for AI`
2. Enter these instructions:

```plaintext
Follow these rules when generating Python code:
- Use snake_case for function and variable names
- Add docstrings for all functions (Google style)
- Use type hints
- Include error handling with specific exceptions
- Follow PEP 8 style guidelines
```

3. Create a new file `user_service.py` and ask Cursor to generate a function to fetch user data
4. Notice how the AI follows your rules in generating the code


## Exercise 2: Project-Specific Rules

However, Cursor will now use these rules _everywhere_!

- So let's instead use a project-specific `.cursorrules` file

1. Create a new project directory called `fastapi-practice`
2. Create a `.cursorrules` file with these FastAPI-specific instructions:

```plaintext
This is a FastAPI project. Follow these rules:
- Use Pydantic models for request/response validation
- Include proper type hints and docstrings
- Follow REST API best practices
- Include basic unit tests using pytest
- Use dependency injection where appropriate
```

3. Ask Cursor to generate a simple user profile endpoint
4. Notice how the AI generates complete components following FastAPI best practices


## Exercise 3: Exploring Ready Made Rules

1. Explore the repositories and directories of ready-made Cursor rules referenced in the slides



## Challenge

Create a `.cursorrules` file for a data science project of your choice. Here's are some example ideas:

1. Uses pandas and numpy
2. Implements proper error handling for data operations
3. Includes data validation
4. Has comprehensive logging
5. Follows scikit-learn best practices

Then use it to generate a function that preprocesses a dataset for machine learning.

## Key Takeaways

- Custom instructions help maintain consistency in code generation
- Project-specific rules can enforce architectural patterns
- The more specific your instructions, the better the AI's output
- Custom instructions can significantly reduce the need for manual editing