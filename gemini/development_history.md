# Development History (The Story So Far)

This document records the major bugs and the design decisions made to fix them. It serves as a log of what has gone wrong to avoid repeating mistakes.

1.  **Initial State**: The simulation was not producing any finished products. Workers were not picking up items.
    *   **Bug**: The worker pickup logic in `simulation.py` was inside an `if worker.pickup()` block, which never executed because `pickup()` returns `None`.
    *   **Decision**: Refactored to use `worker.can_pickup()` before calling `worker.pickup()`.

2.  **'C' Appearing at the Start of the Belt**:
    *   **Bug**: A worker was stationed at slot 0 and would place its finished product there, overwriting the component source.
    *   **Decision**: Slot 0 was reserved exclusively for the component source. All worker stations were shifted to start from slot 1.

3.  **Workers Picking Up Finished Products**:
    *   **Bug**: The worker pickup logic did not check *what* it was picking up, allowing workers to grab finished 'C' products from the belt.
    *   **Decision**: Added a check to ensure workers only pick up components 'A' or 'B'.

4.  **Major Refactoring for Flexibility**:
    *   **Problem**: The worker logic was hardcoded in `simulation.py`, making it impossible to experiment with different AI behaviors.
    *   **Decision**: Introduced the **Strategy Pattern**. Created `strategies.py` to hold all worker AI. Modified `worker.py` to use a strategy object. Modified `simulation.py` to select a strategy via the command line.

5.  **Post-Refactoring `AttributeError`s**:
    *   **Bug 1**: The new strategy code in `strategies.py` used a non-existent `belt.get_slot()` method.
    *   **Bug 2**: The strategy code used non-existent `worker.assembly_progress` attributes.
    *   **Decision**: Corrected the code to use the proper attributes and direct list access (`belt.slots[i]`). This highlighted the need for careful consistency checks between files.

6.  **The Great Stagnation (Zero Finished Products)**:
    *   **Bug 1**: The assembly logic was completely missing from the `IndividualStrategy` after the refactoring.
    *   **Bug 2 (The Root Cause)**: The `worker.needs()` method was fundamentally flawed. It assumed `hand_left` was for 'A' and `hand_right` was for 'B', causing workers to get stuck if they picked up 'B' first.
    *   **Decision**: Added the assembly logic to the strategy. Rewrote the `needs()` method to be agnostic about which hand holds which component. This was the final, critical fix.
