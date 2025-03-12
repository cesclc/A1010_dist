# Working with Language Models for Coding

## Exercise 1: Hallucination Detection

__Objective__: Learn to identify when LLMs generate plausible but incorrect code or documentation.

### Setup:

1. Choose a code assistant (GitHub Copilot, Claude, GPT-4, etc.)

### Tasks:

1. __Fictional Library Detection__

   1. Place the following code in a file called `draw_graph.py`:

        ```python
        import quickgraph

        # Create a visualization
        graph = quickgraph.Graph()
        graph.add_nodes_from(['A', 'B', 'C'])
        graph.visualize(style='force-directed')
        ```

    2. Ask the LLM "How should I use this API?"

    3. Consider:

        - What documentation did the LLM provide?
        - Did it suggest installation commands?
        - How confident did it seem?
        - How would you verify that this library doesn't exist?


2. __Framework Feature Mixing__

    1. Place the following code in a file called `AppComponent.ts`:

        ```typescript
        @Component({
            selector: 'app-root',
            template: `
                <div>
                    <button (click)="setCount(count + 1)">
                        Click me: {{count}}
                    </button>
                </div>
            `
        })
        class AppComponent {
            const [count, setCount] = useState(0);
        }
        ```

    2. Ask the LLM to explain and then help you with the impossible mix of features. The code combines _React hooks_ with _Angular decorators_.

    3. Document:

        - What explanation did it provide?
        - Did it try to make this work?
        - What are the fundamental incompatibilities?

3. __Post Cut-off Features__

   1. Ask about features that didn't exist during training:
        - _Can you tell me anything about PyTime_Monotonic?_
        - _What does PyMutex_Lock do?_
        - _What's typing.TypeIs?_

    2. How does the LLM respond?
        - Different LLMs will respond differently. For example, `gpt-4o` can fetch up-to-date information from the web when needed, and so provide more up-to-date answers, while `claude-3.5-sonnet` may tell you it is at risk of hallucinating!


    3. Consider:
        - Did it recognize the syntax?
        - What alternatives did it suggest?
        - How would you verify the correct modern syntax?



## Exercise 2: Model Comparison

__Objective__: Compare different LLMs on the same coding tasks to understand their strengths and limitations.

### Setup:

1. Access to at least two different LLMs (e.g., Claude and GPT-4)
2. Copy the [Model Comparison Evaluaton Sheet](https://docs.google.com/spreadsheets/d/1YO9u2zu5ny6MSCrdvD5GmQb4c5Cn1dAnEzltZzKJSdE/edit?usp=sharing)
3. Complete the spreadsheet as you work through the following tasks

### Tasks:

1. __Code Generation Task__

    1. Ask each model to create a function with this specification:

        ```text
        """
        Create a function that takes a list of dictionaries containing product information
        (name, price, quantity) and returns:
        1. The total value of inventory
        2. The product with the highest value (price * quantity)
        3. Any products with zero quantity

        Example input:
        products = [
            {"name": "Widget", "price": 10.00, "quantity": 5},
            {"name": "Gadget", "price": 15.00, "quantity": 0},
            {"name": "Tool", "price": 25.00, "quantity": 3}
        ]
        """
        ```

    2. Document:

        - Code correctness
        - Explanation clarity
        - Response speed
        - Edge case handling
        - Documentation Quality
        - Overall usefulness


2. __Code Explanation Task__

    1. Ask each model to explain this code:

        ```python
        def memoize(func):
            cache = {}
            def wrapper(*args):
                if args not in cache:
                    cache[args] = func(*args)
                return cache[args]
            return wrapper

        @memoize
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        ```

    2. Document:

        - Explanation Clarity
        - Response Speed
        - Overall Usefulness


3. __Debugging Task__

    1. Ask each model to debug this code:

        ```python
        class Queue:
            def __init__(self):
                self.items = []
                
            def enqueue(self, item):
                self.items.append(item)
                
            def dequeue(self):
                return self.items.pop()  # Bug: should be pop(0)
                
            def peek(self):
                return self.items[-1]    # Bug: should be items[0]
                
            def is_empty(self):
                return len(self.items) == 0
        ```

    2. Document:

        - Code correctness (quality of suggested fixes)
        - Explanation clarity (how well did it explain the issues?)
        - Response speed
        - Overall usefulness (did it identify the correct bugs? did it make any recommendations?)


## Exercise 3: Leaderboards

__Objective__: To understand when, and when not, leaderboards may be useful in assessing language models for coding.

### Tasks:

1. Various leaderboards exist to assess language models for coding. View the following in a web browser:

    - https://aider.chat/docs/leaderboards/

2. How does this leaderboard rank the language models? And which programming language(s) does it base its ranking on?

3. There are broadly two activities that coding assistants perform:

    1. Code generation (autocomplete, etc)
    2. Explanations, chatting about codebase, design problems, figuring out an approach, etc.

4. Questions:

    1. Are these two areas of activity represented in this leaderboard?
    2. Which do you think developers spend more time on?



## Exercise 4: Cost

__Objective__: To appreciate how different language models vary in price.

### Tasks:

1. Browse to: https://openrouter.ai/models
2. How are the models priced?
3. Which are the cheapest? And which the most expensive?




