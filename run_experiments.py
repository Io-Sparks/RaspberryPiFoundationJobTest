import itertools
from conveyor_simulation import run_simulation

# --- Experiment Configuration ---
# Define the parameter ranges to test. Feel free to adjust these.
BELT_CAPACITIES = [10, 50, 100]
PRODUCER_COUNTS = [1, 5, 10]
CONSUMER_COUNTS = [1, 5, 10]
SIMULATION_DURATION = 10  # seconds


def run_experiments():
    """
    Runs a series of simulations with different configurations and prints the results
    in a formatted table.
    """
    print("--- Starting Performance Experiments ---")
    print(f"Running each simulation for {SIMULATION_DURATION} seconds.")
    print("-" * 80)
    print(
        f"{'Capacity':<12} | {'Producers':<12} | {'Consumers':<12} | "
        f"{'Produced':<12} | {'Consumed':<12} | {'Throughput (items/s)':<25}"
    )
    print("-" * 80)

    # Create all combinations of parameters to test
    param_combinations = itertools.product(
        BELT_CAPACITIES, PRODUCER_COUNTS, CONSUMER_COUNTS
    )

    for capacity, producers, consumers in param_combinations:
        # Run the simulation with the current set of parameters
        results = run_simulation(
            belt_capacity=capacity,
            num_producers=producers,
            num_consumers=consumers,
            duration=SIMULATION_DURATION,
        )

        produced = results["produced"]
        consumed = results["consumed"]
        # Throughput is a key performance metric
        throughput = consumed / SIMULATION_DURATION

        print(
            f"{capacity:<12} | {producers:<12} | {consumers:<12} | "
            f"{produced:<12} | {consumed:<12} | {throughput:<25.2f}"
        )

    print("-" * 80)
    print("--- Experiments Finished ---")


if __name__ == "__main__":
    run_experiments()
