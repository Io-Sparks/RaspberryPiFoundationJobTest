15/08
Loaded up my IDE - got Gemini to tell me about 
the brief as I was going to have to learn the problem space.

I created a repo in github and sorted readme, license 
and the initial .gitignore to get things started so I could
share.

added a blank git repo
`git init`

pulled in the main branch from github
`git remote add origin git@github.com:Io-Sparks/RaspberryPiFoundationJobTest.git`
`git pull origin main`
`git checkout main`
added this work log and the gitignore
`git add IoWorkLog.md TASK_1_-_Conveyor_Belt_Challenge__2_.pdf`
`git commit -m "Initial Commit at project beginning."`

Added in core components of the simulation

Added unit testing 

Added optimisations and experiments to see what effects
changing different parts of the configuration would have
please run with 
`python simulation.py --belt-length 15 --num-worker-pairs 3 --strategy team`

Added Dockerfile to bring consistency between environments.
Didnt add kubernetes and associated checks that would manage a lot of 
scalability aspects as it adds a lot of complexity that is 
unneccesary at this stage 

16/08
Major project enhancements and bug fixes.

- **Implemented Core Assembly Constraint:** Correctly implemented the critical 4-tick assembly delay for creating products, a key requirement from the brief that was previously missing. This makes the simulation far more realistic.

- **Added Comprehensive Testing:** Created a new test suite from scratch (`tests/test_worker.py`) to validate the core logic of the simulation, including the new assembly delay and configuration constraints.

- **Fixed Invalid Configurations:** Corrected a major flaw where the reporting script could test physically impossible scenarios (i.e., more workers than belt space). The simulation will now raise an exception if it receives an invalid configuration, and the test suite verifies this behaviour.

- **New "HiveMind" Strategy:** Introduced a new "perfect information" strategy (`hivemind`) that acts as a single, coordinated entity. This strategy calculates the most optimal move available across the entire factory at each step, providing a theoretical maximum efficiency benchmark.

- **Improved Reporting Logic:** Refined the reporting output to be more intelligent. It now prioritizes low-waste configurations first, then high-efficiency, and correctly moves any configuration that produced zero products to the bottom of the report.

- **Modernized Codebase:**
    - Added comprehensive docstrings and inline comments to all Python files (`belt.py`, `worker.py`, `strategies.py`, `simulation.py`, `reporting.py`).
    - Added full type hinting to all functions and methods, improving code clarity and robustness.

- **Enhanced Documentation:**
    - Created a `.env.example` file to make environment variable configuration clear.
    - Updated all documentation (`README.md` and files in `/gemini`) to reflect the new features, fixes, and a more accurate description of the simulation's rules.
