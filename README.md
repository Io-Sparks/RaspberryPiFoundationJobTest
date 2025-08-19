# Factory Simulation

This project simulates a factory floor with conveyor belts and workers who assemble products from components.

## Core Simulation Rules

- **Components**: The simulation uses two primary components, 'A' and 'B'.
- **Assembly**: A worker must collect one of each component to begin assembly.
- **Assembly Time**: The assembly process is not instantaneous. Once a worker has both components, they enter an "assembling" state for **4 simulation steps**. During this time, they cannot interact with the belt or other workers.
- **Finished Product**: After the 4-step assembly period, the 'A' and 'B' components are consumed and replaced with a finished product, 'C'. The worker is then free to place the 'C' on the belt.

## Configuration

The simulation is configured using environment variables. For local development, you can create a `.env` file in the project root to manage these settings.

**`.env.example`:**
```
# The length of the conveyor belt.
BELT_LENGTH=15

# The number of pairs of workers.
NUM_WORKER_PAIRS=3

# The strategy for the workers (individual, team, or hivemind).
STRATEGY=team

# The number of steps to run the simulation for.
STEPS=100

# Set to "true" to suppress step-by-step output.
QUIET=false
```

### Environment Variables:

*   `BELT_LENGTH`: The number of slots on the conveyor belt. (Default: `10`)
*   `NUM_WORKER_PAIRS`: The number of worker pairs. (Default: `3`)
*   `STRATEGY`: The behavior of the workers. Can be `individual`, `team`, or `hivemind`. (Default: `individual`)
*   `STEPS`: The total number of steps the simulation will run. (Default: `100`)
*   `QUIET`: If set to `true`, the detailed step-by-step log will be hidden. (Default: `false`)

## How to Run

### 1. Local Execution

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file (you can copy `.env.example`) and modify the values as needed. Then, run the simulation:

```bash
python simulation.py
```

### 2. Docker

The project includes a `Dockerfile` for building a containerized version of the simulation.

**Build the image:**
```bash
docker build -t factory-simulation .
```

**Run the container with default settings:**
```bash
docker run factory-simulation
```

**Override configuration at runtime:**
You can override the default environment variables set in the Dockerfile.
```bash
docker run -e STRATEGY=individual -e BELT_LENGTH=20 factory-simulation
```

## Reporting

To analyze the performance of different configurations, run the `reporting.py` script:

```bash
python reporting.py
```

This will test various combinations of settings and print a summary report, including a recommendation for the most efficient configuration found.

## Recommended Configuration

Based on the latest performance analysis, the recommended configuration is:

*   **BELT_LENGTH**: `15`
*   **NUM_WORKER_PAIRS**: `3`
*   **STRATEGY**: `hivemind`
