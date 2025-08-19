import itertools
import time
from collections import defaultdict

from conveyor.conveyor_belt import ConveyorBelt
from conveyor.producer import Producer
from conveyor.consumer import Consumer

# --- Experiment Configuration ---
BELT_CAPACITIES = [10, 20, 50]
PRODUCER_COUNTS = [1, 2, 5]
CONSUMER_COUNTS = [1, 2, 5]
SIMULATION_DURATION = 3  # seconds

def run_single_experiment(belt_capacity, num_producers, num_consumers):
    """Runs a single simulation and returns the results."""
    belt = ConveyorBelt(capacity=belt_capacity)
    producers = [Producer(belt, i) for i in range(num_producers)]
    consumers = [Consumer(belt, i) for i in range(num_consumers)]

    all_threads = producers + consumers
    for t in all_threads:
        t.start()

    time.sleep(SIMULATION_DURATION)

    for t in all_threads:
        t.stop()
    for t in all_threads:
        t.join()

    total_produced = sum(p.items_produced for p in producers)
    total_consumed = sum(c.items_consumed for c in consumers)
    throughput = total_consumed / SIMULATION_DURATION

    return {
        'params': {
            'belt_capacity': belt_capacity,
            'num_producers': num_producers,
            'num_consumers': num_consumers
        },
        'produced': total_produced,
        'consumed': total_consumed,
        'throughput': throughput
    }

def run_all_experiments():
    """Runs all combinations of simulation parameters."""
    results = []
    param_combinations = list(itertools.product(
        BELT_CAPACITIES, PRODUCER_COUNTS, CONSUMER_COUNTS
    ))

    print(f"Running {len(param_combinations)} experiments...")

    for i, (capacity, producers, consumers) in enumerate(param_combinations):
        print(f"  Running experiment {i+1}/{len(param_combinations)}: "
              f"Capacity={capacity}, Producers={producers}, Consumers={consumers}...")
        result = run_single_experiment(capacity, producers, consumers)
        results.append(result)

    print("\nAll experiments complete.")
    return results

def analyze_results(results):
    """Analyzes the results and prints a summary report."""
    if not results:
        print("No results to analyze.")
        return

    # --- Analysis ---
    best_throughput = max(results, key=lambda r: r['throughput'])
    best_efficiency = min(
        results,
        key=lambda r: abs(r['produced'] - r['consumed']) / r['produced'] if r['produced'] > 0 else float('inf')
    )

    # --- Reporting ---
    print("\n--- Performance Analysis Report ---")
    print("\nRecommendations:")
    print(f"""
    - Best for Maximum Throughput:
        Configuration: Capacity={best_throughput['params']['belt_capacity']}, Producers={best_throughput['params']['num_producers']}, Consumers={best_throughput['params']['num_consumers']}
        Throughput: {best_throughput['throughput']:.2f} items/sec
        Details: Produced {best_throughput['produced']}, Consumed {best_throughput['consumed']}
    """)
    print(f"""
    - Best for System Efficiency (Produced vs. Consumed):
        Configuration: Capacity={best_efficiency['params']['belt_capacity']}, Producers={best_efficiency['params']['num_producers']}, Consumers={best_efficiency['params']['num_consumers']}
        Efficiency Score (lower is better): {abs(best_efficiency['produced'] - best_efficiency['consumed']) / best_efficiency['produced']:.2f}
        Details: Produced {best_efficiency['produced']}, Consumed {best_efficiency['consumed']}
    """)

    # Group results by belt capacity for detailed view
    grouped_results = defaultdict(list)
    for r in results:
        grouped_results[r['params']['belt_capacity']].append(r)

    print("\n--- Detailed Results (Grouped by Belt Capacity) ---")
    for capacity, group in sorted(grouped_results.items()):
        print(f"\nBelt Capacity: {capacity}")
        print("-----------------------------------------------------------------")
        print("Producers | Consumers | Produced | Consumed | Throughput (i/s)")
        print("-----------------------------------------------------------------")
        sorted_group = sorted(group, key=lambda r: (r['params']['num_producers'], r['params']['num_consumers']))
        for r in sorted_group:
            p = r['params']
            print(
                f"{p['num_producers']:^9} | "
                f"{p['num_consumers']:^9} | "
                f"{r['produced']:^8} | "
                f"{r['consumed']:^8} | "
                f"{r['throughput']:^16.2f}"
            )
        print("-----------------------------------------------------------------")


if __name__ == "__main__":
    all_results = run_all_experiments()
    analyze_results(all_results)
