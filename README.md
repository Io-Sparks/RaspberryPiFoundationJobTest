# RaspberryPiFoundationJobTest

This project simulates a conveyor belt system with workers assembling products.

## How to Run the Simulation

To run the simulation, execute the `simulation.py` script from your terminal.

```bash
python simulation.py [OPTIONS]
```

### Options:

*   `--belt-length <length>`: Specifies the length of the conveyor belts.
    *   Type: Integer
    *   Default: `10`
    *   Example: `--belt-length 15`

*   `--num-worker-pairs <number>`: Specifies the number of worker pairs.
    *   Type: Integer
    *   Default: `3`
    *   Example: `--num-worker-pairs 2`

*   `--num-belts <number>`: Specifies the number of conveyor belts.
    *   Type: Integer
    *   Default: `1`
    *   Example: `--num-belts 2`

*   `--strategy <strategy_name>`: Specifies the worker strategy to use.
    *   Options: `individual`, `team`
    *   Type: String
    *   Default: `individual`
    *   Example: `--strategy team`

*   `--steps <number>`: Specifies the number of steps to run the simulation for.
    *   Type: Integer
    *   Default: `100`
    *   Example: `--steps 50`

### Examples:

1.  **Run with default settings:**
    ```bash
    python simulation.py
    ```

2.  **Run with a belt length of 20 and 5 worker pairs:**
    ```bash
    python simulation.py --belt-length 20 --num-worker-pairs 5
    ```

3.  **Run for 200 steps using the 'team' strategy:**
    ```bash
    python simulation.py --steps 200 --strategy team
    ```

4.  **Run with 2 belts and a belt length of 15:**
    ```bash
    python simulation.py --num-belts 2 --belt-length 15
    ```

## Running the Unit Tests

To run the unit tests, use the following command from the root directory of the project:

```bash
python -m unittest discover tests
```
