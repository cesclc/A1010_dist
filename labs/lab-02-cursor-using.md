# Lab Exercise 2: Getting Started with AI Dev Tools

__Objective__: Learn the fundamental features of an AI Dev tool (eg Cursor) and become comfortable with basic interactions.

This exercice focusses on Cursor but feel free to use another tool such as Github Copilot, Windsurf or Claude Code.

## Prerequisites
- AI IDE such as Cursor installed on your computer
- Basic familiarity with code editing

## Exercise Overview
This lab will guide you through the essential features of Cursor, focusing on the core tools you'll use daily. Each section includes hands-on tasks with solutions that can be revealed if needed.

### Part 1: Basic Chat Interaction
Let's start by learning how to interact with Cursor's AI assistant.

1. Open a new file in Cursor and name it `hello.py`.
2. Open the Chat panel from the sidebar.
3. Try the following tasks:
   - Ask the assistant to write a "Hello, World!" program in Python
   - Ask it to explain how the code works
   - Ask it to modify the code to accept a user's name as input

<details>
<summary>Reveal Solution</summary>

Example chat interactions:

```
You: "Write a Hello World program in Python"
Assistant: Here's a simple Hello World program:

name = input("What is your name? ")
print(f"Hello, {name}!")

You: "Can you explain how this code works?"
Assistant: [Will explain the f-string and input function...]
```
</details>

### Part 2: Quick Questions
Practice using Quick Questions for immediate code-related queries.

1. Write or paste this simple function into your editor:
```python
def calculate_average(numbers):
    return sum(numbers)/len(numbers)
```
2. Highlight the function and try these tasks:
   - Right-click and select "Ask Cursor" (or use the shortcut)
   - Ask "What could go wrong with this function?"
   - Ask "How can I make this function more robust?"

<details>
<summary>Reveal Solution</summary>

The assistant should point out:
- Division by zero error for empty lists
- No type checking
- Suggested improvements like error handling
</details>

### Part 3: CMD-K Fast Edits
Practice using CMD-K (or CTRL-K) for quick code modifications.

1. Create a new file called `calculator.py` with this code:
```python
def calc(x, y):
    return x + y
```
2. Complete these tasks using CMD-K:
   - Rename the function to `add_numbers`
   - Add parameter type hints
   - Add a docstring explaining what the function does
   - Add error handling for non-numeric inputs

<details>
<summary>Reveal Solution</summary>

After completing all tasks, your code should look similar to this:

```python
def add_numbers(x: float, y: float) -> float:
    """
    Add two numbers together and return the result.
    
    Args:
        x (float): First number to add
        y (float): Second number to add
    
    Returns:
        float: Sum of x and y
        
    Raises:
        TypeError: If inputs are not numeric
    """
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise TypeError("Inputs must be numeric")
    return x + y
```
</details>

### Part 4: Terminal Integration
Learn to use Cursor's integrated terminal and Terminal CMD-K feature.

1. Open the integrated terminal
2. Try these tasks:
   - Create a new virtual environment
   - Install a Python package (e.g., `requests`)
   - Deliberately cause an error (e.g., type `python nonexistent.py`)
   - Use Terminal CMD-K to understand and fix the error

<details>
<summary>Reveal Solution</summary>

```bash
# Create virtual environment
python -m venv venv
# (or `python3` on Mac if default Python is version 2)

# Activate it (Windows)
.\venv\Scripts\activate
# or (Mac/Linux)
source venv/bin/activate

# Install package
pip install requests

# Cause error
python nonexistent.py
# Use CMD-K to ask about the error
```
</details>

### Part 5: Using Cursor Chat’s “Apply”
Practice applying AI suggestions to your code.

1. Create a new file called `data_processor.py`
2. Copy this basic list processing function into it:
```python
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
```
3. Complete these tasks:
   - Ask Cursor to convert this to a list comprehension
   - Use the Apply feature to implement the suggestion
   - Ask Cursor to add input validation
   - Apply the suggested changes

<details>
<summary>Reveal Solution</summary>

Final code should look similar to:

```python
def process_data(data):
    if not isinstance(data, list):
        raise TypeError("Input must be a list")
    return [item * 2 for item in data]
```
</details>

## Final Challenge
Combine all the features you've learned in a single task:

1. Create a new Python file called `text_analyzer.py`
2. Using Chat, Quick Questions, and CMD-K:
   - Create a function that counts words in a text file
   - Add proper error handling
   - Add documentation
   - Add type hints
   - Create a test case
3. Use the terminal to run your tests
4. Use Apply to implement any suggestions for improvement

<details>
<summary>Reveal Solution</summary>

```python
from typing import Dict
from pathlib import Path

def analyze_text(filepath: str | Path) -> Dict[str, int]:
    """
    Analyze a text file and return word frequency.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        Dictionary with words and their frequencies
        
    Raises:
        FileNotFoundError: If file doesn't exist
        TypeError: If filepath is not str or Path
    """
    if not isinstance(filepath, (str, Path)):
        raise TypeError("Filepath must be string or Path")
        
    with open(filepath, 'r') as file:
        text = file.read().lower()
        words = text.split()
        return {word: words.count(word) for word in set(words)}

# Test case
if __name__ == "__main__":
    with open("test.txt", "w") as f:
        f.write("hello world hello python")
    
    result = analyze_text("test.txt")
    print(result)  # Expected: {'hello': 2, 'world': 1, 'python': 1}
```
</details>

## Wrap-up
By completing this lab, you should now be comfortable with:
- Using the Chat feature for code assistance
- Making Quick Questions about specific code
- Using CMD-K for fast edits
- Working with the integrated terminal
- Applying AI suggestions to your code

In the next lab, we'll explore more advanced features of Cursor that build upon these fundamentals.