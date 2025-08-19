# Assumptions and Constraints

This document outlines the key assumptions and design constraints that have been established through trial and error during the development of the simulation.

## Simulation Logic

1.  **Workers Act Before Source**: In a single simulation step, all workers complete their actions *before* a new component is generated at the source. This is critical for allowing workers to place finished products onto the belt.
2.  **Slot 0 is the Source**: The first slot (index 0) of any conveyor belt is exclusively for generating new components. Workers **must not** place any items in this slot.
3.  **Worker Stations Start at Slot 1**: To enforce the "Slot 0 is the Source" rule, worker stations are assigned starting from slot 1.
4.  **Workers Only Pick Up Raw Materials**: Workers should only pick up components 'A' and 'B'. They must never pick up a finished product ('C').
5.  **Assembly Requires 'A' and 'B'**: A finished product 'C' can only be created by assembling one 'A' and one 'B' component.
6.  **One Action Per Step**: A worker can only perform one significant action per simulation step (e.g., pickup, place, or advance assembly).
7.  **Flexible Product Placement**: A worker holding a finished product can place it in **any available empty slot** on the conveyor belt. This is a critical rule to prevent deadlocks in high-density configurations.

## Code and Design

1.  **Strategy Pattern with Interface**: The worker's decision-making logic is decoupled from its state. All AI/logic must be implemented within a class in `strategies.py` that inherits from the `WorkerStrategy` Abstract Base Class. This enforces a contract for all strategies.
2.  **Teamwork via Scoring**: The `TeamStrategy` is implemented using a scoring system. It evaluates all possible actions a worker can take and executes the highest-scoring one. This allows for dynamic and context-aware decision-making.
3.  **Configuration via Environment Variables**: The application is configured using environment variables (e.g., `BELT_LENGTH`, `STRATEGY`), not command-line arguments. This is a core design principle for portability and alignment with containerization best practices.
4.  **Clean JSON Output**: The `simulation.py` script must produce a clean, single-line JSON object as its final output to be compatible with the `reporting.py` script.
5.  **Intelligent Reporting**: The `reporting.py` script is the primary tool for analysis. It must:
    *   Calculate and display metrics for velocity, efficiency (per worker), and waste.
    *   Filter out and demote any configuration that produces zero products.
    *   Sort viable configurations to find the optimal balance of low waste and high efficiency.
