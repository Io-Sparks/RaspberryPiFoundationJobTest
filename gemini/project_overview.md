# Project Overview

## Goal

The primary goal of this project is to simulate a factory production line to identify the most efficient configurations. The simulation consists of one or more conveyor belts that transport components, and pairs of workers who take these components to assemble a finished product.

## Core Components

*   **`simulation.py`**: The main executable for the simulation. It is responsible for:
    *   Parsing command-line arguments (e.g., `--strategy`, `--belt-length`).
    *   Initializing the simulation environment (belts, workers).
    *   Running the main simulation loop for a specified number of steps.
    *   Printing the state of the simulation at each step.
    *   Outputting final statistics in JSON format.

*   **`belt.py`**: Defines the `ConveyorBelt` class.
    *   A belt is a fixed-length series of slots.
    *   It has a `source` that generates new components ('A' or 'B') at the beginning of the belt.
    *   The `advance()` method shifts every item on the belt one position down the line, with the last item falling off and being counted as waste.

*   **`worker.py`**: Defines the `Worker` class.
    *   A worker has two hands and can hold components.
    *   It tracks assembly progress.
    *   It relies on a "Strategy" object to make decisions.

*   **`strategies.py`**: Defines the AI logic for workers using an Abstract Base Class (`WorkerStrategy`) to ensure a consistent interface.
    *   `IndividualStrategy`: Each worker acts independently, following a simple set of priorities.
    *   `TeamStrategy`: Workers collaborate. They can give surplus components to their partners and will pick up components from the belt that their partner needs. The decision-making is based on a scoring system to choose the most optimal action at any given time.

*   **`reporting.py`**: A script for running batch simulations and analyzing performance.
    *   It runs the simulation across a range of different configurations (belt lengths, worker numbers, strategies).
    *   It calculates and reports on key metrics: Velocity (products made), Efficiency (products per worker), and Waste % (missed components).
    *   It identifies the best-performing configuration and provides the command to run it.
