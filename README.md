# Factory Simulation

This project is a Python-based simulation of a factory floor designed to assemble a product 'C' from two components, 'A' and 'B'. It's a tool for exploring the efficiency of different worker strategies and factory layouts.

## Core Concepts

- **Conveyor Belt**: A central belt that carries components 'A' and 'B'. New components are added at the start, and any that aren't picked up fall off the end.
- **Workers**: Workers are stationed in pairs along the belt. Their goal is to pick up one 'A' and one 'B', assemble them into a 'C' (which takes 4 time steps), and then place the 'C' back on the belt.
- **Strategies**: Workers use an AI strategy to decide their actions at each step. The simulation supports different strategies to compare their effectiveness.

## Features

- **Two Worker Strategies**:
    - `individual`: A simple, rule-based strategy where workers act independently.
    - `team`: A more advanced, score-based strategy where workers can collaborate by passing components to each other.
- **Configurable Simulation**: Easily change the belt length, number of workers, and strategy via command-line arguments or environment variables.
- **Detailed Visual Output**: A rich, step-by-step visual representation of the factory floor, showing the belt, worker inventories, and assembly timers.
- **Comprehensive Reporting**: A `reporting.py` script that runs hundreds of simulations with different configurations to find the most efficient and least wasteful setups.
- **Structured Logging**: The simulation uses Python's `logging` module, allowing for clean, filterable output (e.g., INFO, DEBUG, ERROR).

## How to Run

### Running a Single Simulation

You can run a single simulation with custom parameters using `simulation.py`.

```bash
# Example: Run with a belt of length 10, 3 pairs of workers, and the 'team' strategy
python simulation.py --belt-length 10 --num-pairs 3 --strategy team
```

**Command-Line Arguments:**

- `--belt-length`: The number of slots on the conveyor belt.
- `--num-pairs`: The number of worker pairs. The total number of workers will be this value times two.
- `--strategy`: The AI strategy to use (`individual` or `team`).
- `--steps`: The number of time steps to run the simulation for.
- `--log-level`: The level of detail for the output (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

### Generating a Performance Report

To find the best factory configuration, run the `reporting.py` script. This will test many different combinations of belt length, worker numbers, and strategies and print a sorted report of the most effective setups.

```bash
python reporting.py
```

The script will also recommend the best configuration to use as environment variables for future runs.
