# Project Overview

This project is a Python-based simulation of a factory floor. The goal is to assemble a finished product, 'C', from two components, 'A' and 'B'. The simulation is designed to be a tool for analyzing the efficiency of different worker strategies and factory configurations.

## Core Components

*   **`simulation.py`**: The main executable for running a single simulation instance. It handles the simulation loop, manages the state of the world, and prints the output.
*   **`belt.py`**: Defines the `ConveyorBelt` class, which is responsible for moving components through the factory.
*   **`worker.py`**: Defines the `Worker` class, which represents an individual worker who can pick up components, assemble them, and place finished products.
*   **`strategies.py`**: Contains the AI logic for the workers. It defines a base `WorkerStrategy` class and two concrete implementations:
    *   `IndividualStrategy`: A simple, rule-based approach where workers act independently.
    *   `TeamStrategy`: A more sophisticated, score-based approach that allows a pair of workers to collaborate by passing components to each other.
*   **`reporting.py`**: A script to run a large batch of simulations with varying parameters. It analyzes the results to find the most efficient and least wasteful factory configurations.
*   **`views.py`**: Contains the presentation logic, responsible for formatting the simulation state into the detailed, human-readable visual output that is logged to the console.

## Key Features

*   **Configurable Factory**: The simulation can be configured with different belt lengths, numbers of worker pairs, and worker strategies through command-line arguments.
*   **Visual Simulation**: The simulation provides a detailed, step-by-step textual visualization of the factory floor, including the contents of the belt and the state of each worker.
*   **Performance Reporting**: The `reporting.py` script automates the process of testing hundreds of configurations and generates a sorted report to identify the optimal setup.
*   **Structured Logging**: All output is handled through Python's `logging` module, allowing for clear separation of informational messages, warnings, and errors.
*   **Separation of Concerns**: The project is structured to separate the core simulation logic from the presentation (view) logic, making the codebase modular and maintainable.
