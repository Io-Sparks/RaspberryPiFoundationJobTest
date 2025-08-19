import subprocess
import itertools
import json
import os

def run_simulation(belt_length, num_worker_pairs, strategy):
    """Runs the simulation with the given parameters and returns the output."""
    env = os.environ.copy()
    env["BELT_LENGTH"] = str(belt_length)
    env["NUM_WORKER_PAIRS"] = str(num_worker_pairs)
    env["STRATEGY"] = strategy
    env["QUIET"] = "true"
    env["STEPS"] = str(100) # Keep steps constant for comparable results

    command = ["python", "simulation.py"]
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    return result.stdout

def parse_output(output):
    """Parses the JSON output from the simulation."""
    try:
        # The actual JSON output is the last line of the simulation output
        json_output = output.strip().split('\n')[-1]
        data = json.loads(json_output)
        products = data.get("products_created", {}).get("C", 0)
        missed_a = data.get("missed_a", 0)
        missed_b = data.get("missed_b", 0)
        return products, missed_a, missed_b
    except (json.JSONDecodeError, IndexError):
        return 0, 0, 0

def main():
    """
    Runs the simulation with various configurations and generates a report.
    """
    # Sensible ranges for the parameters
    belt_lengths = [1, 5, 10, 15]
    num_worker_pairs_options = [1, 2, 3] # Worker pairs (2, 4, 6 workers)
    strategies = ["individual", "team"]
    simulation_steps = 100 # Keep this constant for comparable results

    results = []

    print("Running simulations...")

    # Generate all combinations of parameters
    param_combinations = list(itertools.product(belt_lengths, num_worker_pairs_options, strategies))

    for i, (belt_length, num_worker_pairs, strategy) in enumerate(param_combinations):
        # Skip impossible configurations where workers wouldn't fit
        if num_worker_pairs > belt_length -1:
            continue

        print(f"Running configuration {i+1}/{len(param_combinations)}: "
              f"Belt Length={belt_length}, Workers={num_worker_pairs*2}, Strategy='{strategy}'")

        output = run_simulation(belt_length, num_worker_pairs, strategy)
        products_created, missed_a, missed_b = parse_output(output)

        velocity = products_created
        num_workers = num_worker_pairs * 2
        efficiency = velocity / num_workers if num_workers > 0 else 0
        total_missed = missed_a + missed_b
        waste_percentage = (total_missed / simulation_steps) * 100 if simulation_steps > 0 else 0

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

    # Sort results by efficiency for the report
    results.sort(key=lambda x: x["efficiency"], reverse=True)

    # Print the report
    print("\n--- Simulation Report ---")
    header = f"{'Belt Length':<15} {'Num Workers':<15} {'Strategy':<15} {'Velocity (Products)':<25} {'Efficiency (Products/Worker)':<30} {'Missed A':<10} {'Missed B':<10} {'Waste %':<10}"
    print(header)
    print("-" * len(header))

    for res in results:
        waste_str = f"{res['waste_percentage']:.1f}%"
        print(f"{res['belt_length']:<15} {res['num_workers']:<15} {res['strategy']:<15} {res['velocity']:<25} {res['efficiency']:<30.4f} {res['missed_a']:<10} {res['missed_b']:<10} {waste_str:<10}")

    # Find and print the command for the most efficient configuration
    if results:
        # Find best config based on efficiency, then velocity as a tie-breaker
        best_config = sorted(results, key=lambda x: (x['efficiency'], x['velocity']), reverse=True)[0]
        belt_length = best_config['belt_length']
        num_worker_pairs = best_config['num_workers'] // 2
        strategy = best_config['strategy']

        print("\n--- Recommended Configuration (Highest Efficiency) ---")
        print("To run the simulation with the most efficient configuration, set these environment variables:")
        print(f"export BELT_LENGTH={belt_length}")
        print(f"export NUM_WORKER_PAIRS={num_worker_pairs}")
        print(f"export STRATEGY={strategy}")
        print("\nThen run: python simulation.py")


if __name__ == "__main__":
    main()
