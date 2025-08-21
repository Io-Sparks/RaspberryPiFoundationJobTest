
import argparse
import os
import json
import logging
from collections import Counter

from belt import ConveyorBelt
from strategies import IndividualStrategy, TeamStrategy
from worker import Worker
from views import format_belt_and_workers, format_simulation_results


class Simulation:
    """
    Orchestrates the factory simulation, managing the conveyor belt, workers,
    and the overall simulation flow.

    This class initializes the simulation environment based on provided
    parameters, runs the simulation for a specified number of steps, and
    reports the final results.
    """
    def __init__(self, num_worker_pairs: int, belt_length: int, strategy_name: str, assembly_time: int):
        """
        Initializes the simulation with specified parameters.

        Args:
            num_worker_pairs (int): The number of pairs of workers.
            belt_length (int): The length of the conveyor belt.
            strategy_name (str): The name of the strategy to be used ('individual' or 'team').
            assembly_time (int): The number of time steps required to assemble a product.

        Raises:
            ValueError: If the number of workers exceeds the belt length or if the
                        strategy name is unknown.
        """
        # A station holds a pair of workers, so the number of workers cannot exceed the belt length.
        if num_worker_pairs > belt_length:
            raise ValueError("Number of workers cannot exceed the belt length.")

        self.num_worker_pairs = num_worker_pairs
        self.belt_length = belt_length
        self.strategy_name = strategy_name
        self.assembly_time = assembly_time
        # Quiet mode suppresses the step-by-step visual output for faster execution.
        self.quiet_mode = os.environ.get("QUIET") == "true"

        # Initialize the conveyor belt.
        self.belt = ConveyorBelt(belt_length)

        # Select the strategy for the workers.
        if strategy_name == 'individual':
            self.strategy = IndividualStrategy()
        elif strategy_name == 'team':
            self.strategy = TeamStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        # Create the workers.
        self.workers = []
        for i in range(num_worker_pairs * 2):
            self.workers.append(Worker(i, self.strategy, self.assembly_time))

    def run(self, steps: int):
        """
        Runs the simulation for a given number of time steps.

        Args:
            steps (int): The total number of steps to simulate.
        """
        # Loop through each time step of the simulation.
        for step in range(steps):
            if not self.quiet_mode:
                logging.info(f"Step {step + 1}")
            self.run_step()

        # After the simulation is complete, print the final results.
        self._print_final_results()

    def run_step(self):
        """
        Executes a single time step of the simulation.

        This involves moving the belt, updating worker assembly progress,
        and allowing workers to act based on their strategy.
        """
        # The belt moves forward, potentially adding a new random item.
        self.belt.step_with_random_item()

        # Workers who are currently assembling continue their work.
        for worker in self.workers:
            if worker.is_assembling():
                worker.step_assembly()

        # Workers decide and act based on the new state of the belt.
        if self.strategy_name == 'individual':
            # In the 'individual' strategy, each worker acts independently.
            for i in range(self.num_worker_pairs * 2):
                station_index = i // 2
                # Find the worker's partner (for potential future strategies, though not used in 'individual').
                partner_idx = i + 1 if i % 2 == 0 else i - 1
                partner = self.workers[partner_idx]
                self.strategy.act(self.workers[i], partner, self.belt, station_index)

        elif self.strategy_name == 'team':
            # In the 'team' strategy, pairs of workers collaborate.
            for i in range(self.num_worker_pairs):
                worker1_idx = 2 * i
                worker2_idx = 2 * i + 1
                worker1 = self.workers[worker1_idx]
                worker2 = self.workers[worker2_idx]
                station_index = i

                # Both workers in the pair get a chance to act.
                self.strategy.act(worker1, worker2, self.belt, station_index)
                self.strategy.act(worker2, worker1, self.belt, station_index)

        # If not in quiet mode, print the visual state of the factory.
        if not self.quiet_mode:
            formatted_output = format_belt_and_workers(self.belt, self.workers, self.num_worker_pairs, self.belt_length)
            for line in formatted_output:
                logging.info(line)

    def _print_final_results(self):
        """
        Calculates and prints the final results of the simulation.

        This includes total products made, components missed, and components
        still held by workers. The output format is either JSON (in quiet mode)
        or a formatted string.
        """
        # Calculate the total number of finished products.
        finished_products = sum(worker.products_made for worker in self.workers)
        
        # Count the number of components ('A' and 'B') still held by workers.
        held_components = Counter()
        for worker in self.workers:
            if worker.hand_left in ['A', 'B']:
                held_components[worker.hand_left] += 1
            if worker.hand_right in ['A', 'B']:
                held_components[worker.hand_right] += 1

        # In quiet mode, output results as a single line of JSON.
        if self.quiet_mode:
            results_json = {
                "products_created": {"C": finished_products},
                "missed_a": self.belt.missed_a,
                "missed_b": self.belt.missed_b,
                "held_a": held_components['A'],
                "held_b": held_components['B']
            }
            print(json.dumps(results_json))
        else:
            # In normal mode, print a formatted, human-readable summary.
            formatted_results = format_simulation_results(
                finished_products, self.belt.missed_a, self.belt.missed_b,
                held_components['A'], held_components['B']
            )
            for line in formatted_results:
                logging.info(line)


if __name__ == "__main__":
    # --- Argument Parsing ---
    # Set up the command-line argument parser.
    parser = argparse.ArgumentParser(description="Run a factory simulation.")
    parser.add_argument("--belt-length", type=int, default=3, help="Length of the conveyor belt.")
    parser.add_argument("--num-pairs", type=int, default=3, help="Number of worker pairs.")
    parser.add_argument("--strategy", type=str, default='team', choices=['individual', 'team'], help="Strategy for the workers.")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps to run the simulation for.")
    parser.add_argument("--assembly-time", type=int, default=4, help="Number of steps required for a worker to assemble a product.")
    parser.add_argument("--log-level", type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level.")
    args = parser.parse_args()

    # --- Logging Configuration ---
    # Configure the logging system based on the specified log level.
    logging.basicConfig(level=getattr(logging, args.log_level), format='%(message)s')

    # --- Parameter Loading ---
    # Load simulation parameters, prioritizing environment variables over command-line arguments.
    belt_length = int(os.environ.get('BELT_LENGTH', args.belt_length))
    num_pairs = int(os.environ.get('NUM_WORKER_PAIRS', args.num_pairs))
    strategy = os.environ.get('STRATEGY', args.strategy)
    steps = int(os.environ.get('STEPS', args.steps))
    assembly_time = int(os.environ.get('ASSEMBLY_TIME', args.assembly_time))

    # --- Simulation Execution ---
    # Use a try-except block to gracefully handle initialization errors.
    try:
        # Create a Simulation instance with the determined parameters.
        simulation = Simulation(num_pairs, belt_length, strategy, assembly_time)
        # Run the simulation.
        simulation.run(steps)
    except ValueError as e:
        # If initialization fails (e.g., invalid parameters), log the error.
        logging.error(f"Failed to initialize simulation: {e}")
