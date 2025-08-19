"""
This module runs a series of simulations with various configurations
and generates a comprehensive report.

The report helps identify the most efficient and least wasteful configurations
for the factory simulation.
"""

import subprocess
import itertools
import json
import os

def run_simulation(belt_length: int, num_worker_pairs: int, strategy: str) -> str:
    """
    Executes the simulation.py script with specified parameters as environment variables.

    The simulation is run in quiet mode with a fixed number of steps to ensure
    comparable results. The JSON output from the simulation is captured.

    Args:
        belt_length (int): The length of the conveyor belt for this simulation run.
        num_worker_pairs (int): The number of worker pairs for this simulation run.
        strategy (str): The strategy to use ("individual" or "team").

    Returns:
        str: The standard output from the simulation script, which includes the
             final JSON result.
    """
    # Create a copy of the current environment variables to modify.
    env = os.environ.copy()
    # Set the configuration parameters as environment variables.
    env["BELT_LENGTH"] = str(belt_length)
    env["NUM_WORKER_PAIRS"] = str(num_worker_pairs)
    env["STRATEGY"] = strategy
    # Run in quiet mode to suppress step-by-step output.
    env["QUIET"] = "true"
    # Ensure a consistent number of steps for fair comparison.
    env["STEPS"] = str(1000)

    # Define the command to run the simulation script.
    command = ["python", "simulation.py"]
    # Execute the command and capture its output.
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    return result.stdout

def parse_output(output: str) -> tuple[int, int, int]:
    """
    Parses the JSON output string from the simulation.

    The simulation script prints a JSON object as its last line of output.
    This function extracts and decodes that JSON.

    Args:
        output (str): The complete standard output string from the simulation.

    Returns:
        tuple[int, int, int]: A tuple containing:
                               - products_created (int): Total 'C' products made.
                               - missed_a (int): Total 'A' components missed.
                               - missed_b (int): Total 'B' components missed.
        Returns (0, 0, 0) if parsing fails.
    """
    try:
        # The JSON output is expected to be the last line.
        json_output = output.strip().split('\n')[-1]
        data = json.loads(json_output)
        # Extract relevant metrics, defaulting to 0 if not found.
        products = data.get("products_created", {}).get("C", 0)
        missed_a = data.get("missed_a", 0)
        missed_b = data.get("missed_b", 0)
        return products, missed_a, missed_b
    except (json.JSONDecodeError, IndexError):
        # Handle cases where the output is not valid JSON or is empty.
        return 0, 0, 0

def main():
    """
    Main function to orchestrate the report generation process.

    It defines the range of parameters to test, runs simulations for each
    combination, collects results, calculates metrics, and prints a sorted report.
    """
    # Define the strategies to be tested.
    strategies = ["individual", "team"]
    # Define the fixed number of simulation steps for each run.
    simulation_steps = 1000

    # List to store the results of each simulation run.
    results = []

    print("Generating simulation configurations...")

    # Generate all valid parameter combinations.
    param_combinations = []
    # Iterate through belt lengths from 1 to 20.
    for belt_length in range(1, 21):
        # The number of worker pairs can range from 1 up to the belt length.
        # This ensures workers always have a valid station index (1 to belt_length).
        for num_worker_pairs in range(1, belt_length + 1):
            # Test each defined strategy for the current belt length and worker count.
            for strategy in strategies:
                param_combinations.append((belt_length, num_worker_pairs, strategy))

    print(f"Running {len(param_combinations)} simulations...")

    # Run each simulation and collect its metrics.
    for i, (belt_length, num_worker_pairs, strategy) in enumerate(param_combinations):
        # Print progress to the console.
        print(f"Running configuration {i+1}/{len(param_combinations)}: "
              f"Belt Length={belt_length}, Workers={num_worker_pairs*2}, Strategy='{strategy}'")

        # Execute the simulation and parse its output.
        output = run_simulation(belt_length, num_worker_pairs, strategy)
        products_created, missed_a, missed_b = parse_output(output)

        # Calculate derived metrics.
        velocity = products_created
        num_workers = num_worker_pairs * 2
        # Efficiency is products per worker; avoid division by zero.
        efficiency = velocity / num_workers if num_workers > 0 else 0
        total_missed = missed_a + missed_b
        # Total components introduced to the belt is equal to the simulation steps.
        total_components_introduced = simulation_steps
        # Waste percentage is the proportion of missed components out of total introduced.
        waste_percentage = (total_missed / total_components_introduced) * 100 if total_components_introduced > 0 else 0

        # Store all results in a dictionary.
        results.append({
            "belt_length": belt_length,
            "num_workers": num_workers,
            "strategy": strategy,
            "velocity": velocity,
            "efficiency": efficiency,
            "missed_a": missed_a,
            "missed_b": missed_b,
            "waste_percentage": waste_percentage,
        })

    # Sort the results based on the defined criteria:
    # 1. Configurations with 0 velocity (no products made) are pushed to the very bottom.
    # 2. For productive configurations, sort by waste percentage (lowest first).
    # 3. Then, sort by efficiency (highest first).
    results.sort(key=lambda x: (
        1 if x['velocity'] == 0 else 0,  # Primary sort: 0-velocity runs go last
        x['waste_percentage'],          # Secondary sort: lowest waste first
        -x['efficiency']                 # Tertiary sort: highest efficiency first (negative for descending)
    ))

    # Print the formatted report header.
    print("\n--- Simulation Report ---")
    header = f"{'Belt Length':<15} {'Num Workers':<15} {'Strategy':<15} {'Velocity (Products)':<25} {'Efficiency (Products/Worker)':<30} {'Missed A':<10} {'Missed B':<10} {'Waste %':<10}"
    print(header)
    print("-" * len(header))

    # Print each row of the report.
    for res in results:
        waste_str = f"{res['waste_percentage']:.1f}%"
        print(f"{res['belt_length']:<15} {res['num_workers']:<15} {res['strategy']:<15} {res['velocity']:<25} {res['efficiency']:<30.4f} {res['missed_a']:<10} {res['missed_b']:<10} {waste_str:<10}")

    # Find and print the command for the best configuration.
    # The best configuration is the first one in the sorted list that produced products.
    best_config = next((r for r in results if r['velocity'] > 0), None)

    if best_config:
        # Extract parameters for the best configuration.
        belt_length = best_config['belt_length']
        # Convert total workers back to worker pairs.
        num_worker_pairs = best_config['num_workers'] // 2
        strategy = best_config['strategy']

        # Print the recommended configuration as environment variables.
        print("\n--- Recommended Configuration (Lowest Waste, Highest Efficiency) ---")
        print("To run the simulation with the least wasteful and most efficient configuration, set these environment variables:")
        print(f"export BELT_LENGTH={belt_length}")
        print(f"export NUM_WORKER_PAIRS={num_worker_pairs}")
        print(f"export STRATEGY={strategy}")
        print("\nThen run: python simulation.py")
    else:
        print("\nNo productive configurations found in the simulation runs.")


if __name__ == "__main__":
    # Execute the main function when the script is run directly.
    main()
