# Lab Exercise 1: Using Simple AI Tools.

__Objective__: Use simple AI tools to complete coding tasks. 

## Prerequisites
- Basic familiarity with code editing
- Optionally OpenAI and Claude API keys

## Exercise Overview

This lab will give you chance to practice or refresh Prompting techniques using simple online tools and web pages. 

Work in pairs to compare the different tools and techniques explored throughout the exercise.

### Part 1: Environment setup and simple "Hello" app

1. Decide on two simple AI tools that you and your partner will use, such as ChatGPT, Perplexity, Claude, OpenAI, Mistral etc.
2. Choose a familiar programming language, preferably different from your partner's choice.
3. Perform any necessary setup for your chosen languauges, such as Java runtime path, Python Virtual Environment, etc. 
4. Use the AI tool to write a simple "Hello World" app. Copy / paste and run it to prove that your setup works.

### Part 2: Calculator app

Use the AI tool to perform the following steps

1. Write a program that inputs some numbers and calculates their sum and average.
2. Make this into a Web Service using a framework of your choice (Flask, SpringBoot, Express etc). Consider whether to pass the data as request parameters for easy testing in a browser, or in the request body for use with a Client Tool such as Curl, Postman or Swagger.
3. Separate the Sum and Average features into two separate REST endpoints.

### Part 3: Explore limitations of chosen Tools / LLMs

1. Research and compare the costs and privacy aspects of your chosen AI tools.
2. Explore "cut-off-date" limitations by finding when the model was trained. Choose a newer feature by referencing language documentation such as JDK Project Docs at `openjdk.org`, and Docs for different Python Versions  at `python.org/doc/versions/` Examine the AI tool's response for these cases.
3. Find cost and capability details of various models from OpenAI, Anthropic or others. Choose a cheap, limited model such as GPT-3.5-turbo. Note that such models can be a good choice for simple tasks as they represent a good cost / performance trade-off.
4. Use the cheap LLM to perform similar actions to those done already and Compare the results. Similarly explore some new actions to create additions to your app. 

### Part 4: (if time permits) Invoking LLM from code

1. Note that some LLM versions and choices might not be available from readily available online apps / pages. In such cases the LLM can be invoked from your code via an API, as detailed in the individual LLM documentation.
2. The best environment for this is Python with Jupyter Notebook, though LangChain4J and SpringAI are possible alternatives. 
3. Explore documentation for setting up your environment (Jupyter Notebook etc) using your simple AI tool such as Perplexity of course!
4. Write some code to choose and invoke the specific LLM.
5. Refer to the API key details provided by your instructor.


## Wrap-up
By completing this lab, you should now be comfortable with:
- Using simple AI tools to complete coding tasks.
- Writing comprehensive, structured propmts.
