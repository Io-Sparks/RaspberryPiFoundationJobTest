"""
This module runs a series of simulations with various configurations
and generates a comprehensive report.

The report helps identify the most efficient and least wasteful configurations
for the factory simulation.
"""

import subprocess
import json
import os
import logging
from typing import List, Tuple, Dict, Any, Optional

# Configure logging for the reporting script
logging.basicConfig(level=logging.INFO, format='%(message)s')

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
    env = os.environ.copy()
    env["BELT_LENGTH"] = str(belt_length)
    env["NUM_WORKER_PAIRS"] = str(num_worker_pairs)
    env["STRATEGY"] = strategy
    env["QUIET"] = "true"
    env["STEPS"] = str(1000)

    command: List[str] = ["python", "simulation.py"]
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    return result.stdout

def parse_output(output: str) -> Tuple[int, int, int, int, int]:
    """
    Parses the JSON output string from the simulation.

    The simulation script prints a JSON object as its last line of output.
    This function extracts and decodes that JSON.

    Args:
        output (str): The complete standard output string from the simulation.

    Returns:
        tuple[int, int, int, int, int]: A tuple containing:
                               - products_created (int): Total 'C' products made.
                               - missed_a (int): Total 'A' components missed.
                               - missed_b (int): Total 'B' components missed.
                               - held_a (int): Total 'A' components held by workers.
                               - held_b (int): Total 'B' components held by workers.
        Returns (0, 0, 0, 0, 0) if parsing fails.
    """
    try:
        json_output: str = output.strip().split('\n')[-1]
        data: Dict[str, Any] = json.loads(json_output)
        products: int = data.get("products_created", {}).get("C", 0)
        missed_a: int = data.get("missed_a", 0)
        missed_b: int = data.get("missed_b", 0)
        held_a: int = data.get("held_a", 0)
        held_b: int = data.get("held_b", 0)
        return products, missed_a, missed_b, held_a, held_b
    except (json.JSONDecodeError, IndexError):
        logging.error("\n--- Error parsing simulation output ---")
        logging.error(output)
        logging.error("-----------------------------------------")
        return 0, 0, 0, 0, 0

def main() -> None:
    """
    Main function to orchestrate the report generation process.

    It defines the range of parameters to test, runs simulations for each
    combination, collects results, calculates metrics, and prints a sorted report.
    """
    # Define the strategies to be tested.
    strategies: List[str] = ["individual", "team"]
    simulation_steps: int = 1000

    results: List[Dict[str, Any]] = []

    logging.info("Generating simulation configurations...")

    param_combinations: List[Tuple[int, int, str]] = []
    for belt_length in range(1, 21):
        # Ensure the number of worker pairs does not exceed the belt's capacity.
        # Each pair needs 2 slots, so the max pairs is belt_length // 2.
        for num_worker_pairs in range(1, (belt_length // 2) + 1):
            for strategy in strategies:
                param_combinations.append((belt_length, num_worker_pairs, strategy))

    logging.info(f"Running {len(param_combinations)} simulations...")

    for i, (belt_length, num_worker_pairs, strategy) in enumerate(param_combinations):
        logging.info(f"Running configuration {i+1}/{len(param_combinations)}: "
                     f"Belt Length={belt_length}, Workers={num_worker_pairs*2}, Strategy='{strategy}'")

        output: str = run_simulation(belt_length, num_worker_pairs, strategy)
        products_created, missed_a, missed_b, held_a, held_b = parse_output(output)

        velocity: int = products_created
        num_workers: int = num_worker_pairs * 2
        efficiency: float = velocity / num_workers if num_workers > 0 else 0
        total_missed: int = missed_a + missed_b
        total_components_introduced: int = simulation_steps
        waste_percentage: float = (total_missed / total_components_introduced) * 100 if total_components_introduced > 0 else 0

        results.append({
            "belt_length": belt_length,
            "num_workers": num_workers,
            "strategy": strategy,
            "velocity": velocity,
            "efficiency": efficiency,
            "missed_a": missed_a,
            "missed_b": missed_b,
            "held_a": held_a,
            "held_b": held_b,
            "waste_percentage": waste_percentage,
        })

    results.sort(key=lambda x: (
        1 if x['velocity'] == 0 else 0,  # Primary sort: 0-velocity runs go last
        x['waste_percentage'],          # Secondary sort: lowest waste first
        -x['efficiency']                 # Tertiary sort: highest efficiency first (negative for descending)
    ))

    logging.info("\n--- Simulation Report ---")
    header: str = f"{'Belt Length':<15} {'Num Workers':<15} {'Strategy':<15} {'Velocity (Products)':<25} {'Efficiency (Products/Worker)':<30} {'Missed A':<10} {'Missed B':<10} {'Held A':<10} {'Held B':<10} {'Waste %':<10}"
    logging.info(header)
    logging.info("-" * len(header))

    for res in results:
        waste_str: str = f"{res['waste_percentage']:.1f}%"
        logging.info(f"{res['belt_length']:<15} {res['num_workers']:<15} {res['strategy']:<15} {res['velocity']:<25} {res['efficiency']:<30.4f} {res['missed_a']:<10} {res['missed_b']:<10} {res['held_a']:<10} {res['held_b']:<10} {waste_str:<10}")

    best_config: Optional[Dict[str, Any]] = next((r for r in results if r['velocity'] > 0), None)

    if best_config:
        belt_length = best_config['belt_length']
        num_worker_pairs = best_config['num_workers'] // 2
        strategy = best_config['strategy']

        logging.info("\n--- Recommended Configuration (Lowest Waste, Highest Efficiency) ---")
        logging.info("To run the simulation with the least wasteful and most efficient configuration, set these environment variables:")
        logging.info(f"export BELT_LENGTH={belt_length}")
        logging.info(f"export NUM_WORKER_PAIRS={num_worker_pairs}")
        logging.info(f"export STRATEGY={strategy}")
        logging.info("\nThen run: python simulation.py")
    else:
        logging.info("\nNo productive configurations found in the simulation runs.")


if __name__ == "__main__":
    main()
