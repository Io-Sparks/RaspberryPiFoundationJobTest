# Project Overview

## Goal

The primary goal of this project is to simulate a factory production line. The simulation consists of one or more conveyor belts that transport components, and pairs of workers who take these components to assemble a finished product.

## Core Components

*   **`simulation.py`**: The main executable for the simulation. It is responsible for:
    *   Parsing command-line arguments (e.g., `--strategy`).
    *   Initializing the simulation environment (belts, workers).
    *   Running the main simulation loop for a specified number of steps.
    *   Printing the state of the simulation at each step.
    *   Reporting final statistics.

*   **`belt.py`**: Defines the `ConveyorBelt` class.
    *   A belt is a fixed-length series of slots.
    *   It has a `source` that generates new components ('A', 'B', or `None`) at the beginning of the belt (slot 0).
    *   The `advance()` method shifts every item on the belt one position down the line, with the last item falling off.

*   **`worker.py`**: Defines the `Worker` class.
    *   A worker has two hands (`hand_left`, `hand_right`) and can hold components.
    *   It tracks assembly progress (`assembling_time_left`).
    *   It relies on a "Strategy" object to make decisions.

*   **`strategies.py`**: Defines the AI logic for workers.
    *   This file was created to decouple the decision-making logic from the worker's state.
    *   It contains a base `WorkerStrategy` class and concrete implementations.
    *   `IndividualStrategy` is the current implementation, where each worker acts alone.
    *   A `TeamStrategy` is planned for future development where workers can coordinate.
