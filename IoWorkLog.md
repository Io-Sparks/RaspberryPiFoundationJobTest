# Io's Work Log

## 15/08/2024: Project Kick-off & Foundation

- Utilized Gemini to understand the project brief and problem space.
- Initialized a new Git repository and connected it to GitHub.
- Created foundational project files: `README.md`, `.gitignore`, and this `IoWorkLog.md`.
- Performed the initial commit of project documents.
  ```bash
  git init
  git remote add origin git@github.com:Io-Sparks/RaspberryPiFoundationJobTest.git
  git pull origin main
  git checkout main
  git add IoWorkLog.md TASK_1_-_Conveyor_Belt_Challenge__2_.pdf
  git commit -m "Initial Commit at project beginning."
  ```
- Added core components of the simulation, including the initial `belt`, `worker`, and `simulation` modules.
- Implemented the first version of unit testing to ensure baseline functionality.
- Added a `Dockerfile` to ensure a consistent and reproducible runtime environment.
- Added optimizations and experiments to explore the effects of different simulation configurations.
  - Example run command: `python simulation.py --belt-length 15 --num-worker-pairs 3 --strategy team`

## 19/08/2024: Major Enhancements & Bug Fixes

- **Implemented Core Assembly Constraint:** Correctly implemented the critical 4-tick assembly delay for creating products, a key requirement from the brief that was previously missing. This makes the simulation far more realistic.
- **Added Comprehensive Testing:** Created a new test suite from scratch (`tests/test_worker.py`) to validate the core logic of the simulation, including the new assembly delay and configuration constraints.
- **Fixed Invalid Configurations:** Corrected a major flaw where the reporting script could test physically impossible scenarios (i.e., more workers than belt space). The simulation will now raise an exception if it receives an invalid configuration, and the test suite verifies this behaviour.
- **Improved Reporting Logic:** Refined the reporting output to be more intelligent. It now prioritizes low-waste configurations first, then high-efficiency, and correctly moves any configuration that produced zero products to the bottom of the report.
- **Modernized Codebase:**
    - Added comprehensive docstrings and inline comments to all Python files (`belt.py`, `worker.py`, `strategies.py`, `simulation.py`, `reporting.py`).
    - Added full type hinting to all functions and methods, improving code clarity and robustness.
- **Enhanced Documentation:**
    - Created a `.env.example` file to make environment variable configuration clear.
    - Updated all documentation (`README.md` and files in `/gemini`) to reflect the new features, fixes, and a more accurate description of the simulation's rules.

## 20/08/2024: Intensive Debugging, Refactoring & Visualization

This session focused on systematically resolving bugs, improving the accuracy of the simulation, and dramatically enhancing the user-facing output.

- **Systematic Bug Squashing:**
    - Resolved a `TypeError` in `strategies.py` caused by incorrect indexing of the `ConveyorBelt` object.
    - Fixed a cascade of unit test failures that arose from the initial fix, including an `AttributeError` in `test_strategies.py` and a `TypeError` in `test_worker.py`.
    - Corrected a `ValueError` that occurred when the number of workers exceeded the belt length and fixed the final failing unit test that was not correctly asserting this constraint.

- **Reporting Accuracy and Logic Fixes:**
    - Identified and fixed a critical bug where the `team` strategy was producing zero products in the final report, making it appear non-functional.
    - Corrected the "Finished Products" calculation in `simulation.py` to accurately reflect the total number of products created throughout the entire simulation, rather than just a snapshot at the end. This ensures the final report is a true reflection of the factory's total output.

- **Enhanced Simulation Output & Visualization:**
    - Added detailed, real-time commentary to the simulation output, logging when workers pick up, place, or pass components, including the specific slot location.
    - Designed and implemented a completely new, multi-line pictorial representation of the factory floor. This detailed view shows the status of each worker (ID, left/right hands, assembly timer) in relation to the conveyor belt, providing an intuitive and easy-to-read display of the simulation at each step.

- **Major Code Refactoring & Modernization:**
    - **Logging Framework:** Replaced all `print()` statements throughout the project with Python's standard `logging` module. This allows for structured logging with different severity levels (e.g., INFO, ERROR) and provides a `--log-level` command-line argument for granular control over the output.
    - **Separation of Concerns:** Created a new `views.py` module to handle all presentation logic. The complex formatting for the factory floor display and the final results summary was moved out of `simulation.py` and into this new module, resulting in cleaner, more maintainable, and more professional code.
