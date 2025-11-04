# Lab Exercise 7a: Debugging Satpy image display Using AI Assistance 

## Overview:

The code provided for this exercise uses sample data representing a mid-latitude cyclone over the United States.

It should use Satpy sample data from ABI (Advanced Baseline Imager) - the primary instrument on NOAA's GOES-R series satellites.

The code has bugs. Your task is to use an AI development tool to debug it.
Record your findings in an organised fashion as you progress, so that you can structure and document the process. Keep a Troubleshooting Log to record each:
- Error description / title
- Error message
- AI suggestion
- Action taken (what you did)
- Result (if / how well it worked)

## Prerequisites:

Knowledge of Python, Jupyter Notebook, configuration of its libraries and virtual environments. Ask your instructor for help if needed.

## Tasks
  1. Run the starter code and observe the error
  2. Use AI assistant to diagnose the problem
  3. Install necessary dependencies with AI guidance
  4. Iterate through errors until image displays
  5. Document your troubleshooting process

## Success Criteria
  - [ ] Python code produces .png file of satellite image
  - [ ] Add a synthetic cloud or storm feature
  - [ ] Create requirements.txt with all dependencies
  - [ ] Display satellite image(s) in Jupyter notebook
  - [ ] Document 3+ error types you encountered

## Reflection Questions
  - What debugging strategies did the AI suggest?
  - Which errors required multiple iterations?
  - How did you verify the AI's suggestions were correct?

## Getting started

1. Copy the initial code from `lab-07a-starter.py` in the `labs` directory of this repository into a new folder, and start debugging!

2. For the "Kaggle data not found" error, instead use Satpy's built-in Americas/NOAA ABI demo data by:
- Add an import: `from satpy.demo import get_us_midlatitude_cyclone_abi`
- Call it by changing the `fnames = glob.glob(...)` call to: `fnames = get_us_midlatitude_cyclone_abi()`

3. When the code is working you should see an image similar to `cloud_cover.png` in the `codeSamples/SatPy` directory of this repository.

4. Once the code is working, extend it to also load and display Air Mass details. Add any other details that you can find.
<details>
<summary>Reveal Solution</summary>
See `codeSample/ex7_solution01.py`
</details>

5. Try a different AI Dev tool, and compare differences in performance.

6. Subject to data availability, extend the app to use Europe/EUMETSAT data. See `data.eumetsat.int` and create a login account as necessary

## Further ideas:  
- Determine what is the data telling us.
  - Ask another AI such as ChatGPT, showing it the image. 
  - Ask the AI Dev tool that you used to debug this code, this will have more insight / context.
<details>
<summary>Reveal Solution</summary>
See `codeSample/ex7_solution02.txt`
</details>

- Generate a description of the ABI data format and content
<details>
<summary>Reveal Solution</summary>
See `codeSample/ex7_solution03.txt`
</details>

- Determine other attributes to display
<details>
<summary>Reveal Solution</summary>
See `codeSample/ex7_solution04.py`
</details>

- Use you AI Dev tool to help you design a web app to productionise the image cration and display
  - Consider what features would you add, and what other data it should display
  - Design UI features to enable this
  - Consider components and platforms (backend, frontend, database etc)



