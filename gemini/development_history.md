# Development History (The Story So Far)

This document records the major bugs and the design decisions made to fix them. It serves as a log of what has gone wrong to avoid repeating mistakes.

1.  **Initial State**: The simulation was not producing any finished products. Workers were not picking up items.
    *   **Decision**: Corrected worker pickup logic in `simulation.py`.

2.  **'C' Appearing at the Start of the Belt**:
    *   **Decision**: Reserved slot 0 for the component source and shifted worker stations to start from slot 1.

3.  **Workers Picking Up Finished Products**:
    *   **Decision**: Added a check to ensure workers only pick up components 'A' or 'B'.

4.  **Major Refactoring for Flexibility**:
    *   **Problem**: The worker logic was hardcoded in `simulation.py`, making it impossible to experiment with different AI behaviors.
    *   **Decision**: Introduced the **Strategy Pattern**. Created `strategies.py` to hold all worker AI. This was a pivotal change for the project's architecture.

5.  **The Great Stagnation (Zero Finished Products)**:
    *   **Bug**: The `worker.needs()` method was fundamentally flawed, causing workers to get stuck if they picked up component 'B' before 'A'.
    *   **Decision**: Rewrote the `needs()` method to be hand-agnostic. This was a critical fix to enable basic production.

6.  **Reporting and Analysis Implementation**:
    *   **Need**: A way to systematically test different configurations and measure performance.
    *   **Decision**: Created `reporting.py`. This script automates running the simulation with various parameters and generates a performance report. Initially, it had bugs where it failed to parse the simulation output.
    *   **Fix**: Modified `simulation.py` to output a clean JSON summary, which the reporting script could reliably parse.

7.  **The Failed `TeamStrategy` (Multiple Attempts)**:
    *   **Bug**: The initial `TeamStrategy` was non-functional, producing zero products. The logic was flawed, causing workers to either do nothing or give away components they needed themselves.
    *   **Decision**: Rewrote the `TeamStrategy` multiple times. The final, successful version uses a scoring system (`_get_best_action`). Workers evaluate all possible moves (pickup, give, assemble, place) and choose the one with the highest score, making their decision-making dynamic and intelligent.

8.  **Defensive Programming Enhancement**:
    *   **Need**: To ensure future strategies would adhere to the required structure.
    *   **Decision**: Implemented an Abstract Base Class (`WorkerStrategy`) in `strategies.py`. This acts as an "interface," forcing any new strategy to implement the `act()` method, preventing incomplete strategies from being used.

9.  **Critical Simulation Logic Flaw**:
    *   **Bug**: With a very short belt (e.g., length 1), no products were ever made. The simulation was adding a new component to the belt *before* letting workers place their finished products, meaning the placement slot was never empty.
    *   **Decision**: Corrected the order of operations in `simulation.py`. Workers now act *before* the new component is added, fixing the bug and making the simulation more realistic.

10. **Refining Performance Metrics**:
    *   **Need**: The initial "efficiency" metric (products per step) wasn't very insightful.
    *   **Decision**: Changed the efficiency calculation to be **products per worker**. Added **waste tracking** (missed components) to the report. This provides a much more comprehensive view for identifying the truly optimal configuration.
