# Project Overview

## Goal

The primary goal of this project is to simulate a factory production line to identify the most efficient configurations. The simulation consists of one or more conveyor belts that transport components, and pairs of workers who take these components to assemble a finished product.

## Core Components

*   **`simulation.py`**: The main executable for the simulation. It is responsible for:
    *   Reading its configuration from environment variables (e.g., `BELT_LENGTH`, `NUM_WORKER_PAIRS`), with support for `.env` files for local development.
    *   Initializing the simulation environment (belts, workers).
    *   Running the main simulation loop for a specified number of steps. This includes advancing the assembly timers for all workers at each step.
    *   Printing the state of the simulation at each step.
    *   Outputting final statistics in JSON format.
    *   **Self-validating**: The simulation will raise a `ValueError` if initialized with more workers than the belt can physically hold.

*   **`belt.py`**: Defines the `ConveyorBelt` class.
    *   A belt is a fixed-length series of slots.
    *   It has a `source` that generates new components ('A' or 'B') at the beginning of the belt.
    *   The `advance()` method shifts every item on the belt one position down the line, with the last item falling off and being counted as waste.

*   **`worker.py`**: Defines the `Worker` class.
    *   A worker has two hands and can hold components.
    *   **Assembly Process**: A worker must collect both an 'A' and a 'B' component to start assembly. The process takes **4 simulation steps**, during which the worker is busy. After the timer completes, the components are replaced by a finished 'C' product.
    *   It relies on a "Strategy" object to make decisions.

*   **`strategies.py`**: Defines the AI logic for workers using an Abstract Base Class (`WorkerStrategy`).
    *   `IndividualStrategy`: Each worker acts independently, following a simple set of priorities.
    *   `TeamStrategy`: Workers collaborate. They can give surplus components to their partners and will pick up components from the belt that their partner needs. The decision-making is based on a scoring system.
    *   `HiveMindStrategy`: A "perfect information" strategy that executes the single most optimal move for the entire system at each step, coordinating all workers.

*   **`reporting.py`**: A script for running batch simulations and analyzing performance.
    *   It runs the simulation across a wide and dynamic range of configurations, ensuring that all tested scenarios are physically possible (i.e., number of workers does not exceed belt capacity).
    *   It calculates and reports on key metrics: Velocity (products made), Efficiency (products per worker), and Waste % (missed components).
    *   It intelligently sorts the results, prioritizing productive configurations with the lowest waste and highest efficiency.

*   **`Dockerfile`**: Defines a containerized environment for the simulation, ensuring consistency and portability.
