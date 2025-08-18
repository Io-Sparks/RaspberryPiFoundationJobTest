# Conveyor Belt Simulation

This project simulates a factory conveyor belt system with multiple producer and consumer threads. It is designed to be a scalable and robust demonstration of concurrent programming principles in Python.

## Project Structure

- `conveyor/`: The core Python package containing the logic for the belt, producers, and consumers.
- `tests/`: Contains unit and integration tests for the project.
- `conveyor_simulation.py`: The main script to run the simulation.
- `run_experiments.py`: A script to run a battery of performance tests with different configurations.
- `config.py`: Handles configuration management via environment variables.
- `docs/`: Contains project documentation for architectural decisions and assumptions.

## Getting Started

### Prerequisites

- Python 3.7+

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd RaspberryPiFoundationJobTest
    ```

2.  **Create a local configuration file:**
    The simulation is configured using environment variables. For local development, you can create a `.env` file in the project root.

    ```bash
    cp .env.example .env
    ```

    Now you can edit the `.env` file to change simulation parameters:
    - `BELT_CAPACITY`: The maximum number of items the belt can hold.
    - `NUM_PRODUCERS`: The number of producer threads.
    - `NUM_CONSUMERS`: The number of consumer threads.

### Running the Simulation

To run the main simulation, execute the following command from the project root:

```bash
python conveyor_simulation.py
```

The script will load the configuration from your `.env` file and start the simulation, printing live updates to the console.

### Running the Tests

The project includes a suite of unit and integration tests to ensure correctness and thread-safety. To run all tests, use Python's built-in `unittest` discover feature:

```bash
python -m unittest discover tests
```

This will find and run all files named `test_*.py` inside the `tests/` directory.

### Running Performance Experiments

To analyze the performance characteristics of the system under different configurations, you can run the experiment script:

```bash
python run_experiments.py
```

This script will run a series of simulations with varying belt capacities, producer counts, and consumer counts. It will print a summary table of the results, allowing you to observe how each parameter affects the overall throughput of the system. You can modify the parameter ranges at the top of the `run_experiments.py` file to conduct different tests.
