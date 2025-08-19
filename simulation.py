"""
This module runs the main factory simulation.

It orchestrates the entire process, including creating the belts and workers,
running the simulation step-by-step, and printing the final results.
Configuration is loaded from environment variables.
"""

import json
import random
import os
from dotenv import load_dotenv
from belt import ConveyorBelt
from worker import Worker
from strategies import IndividualStrategy, TeamStrategy

class Simulation:
    """Manages the setup and execution of the factory simulation."""

    def __init__(self, num_worker_pairs, belt_length, num_belts, strategy_name):
        """
        Initializes the simulation environment.

        Args:
            num_worker_pairs (int): The number of pairs of workers.
            belt_length (int): The length of the conveyor belts.
            num_belts (int): The number of conveyor belts.
            strategy_name (str): The name of the strategy to use ("individual" or "team").

        Raises:
            ValueError: If the configuration is invalid (e.g., too many workers).
        """
        # Design constraint: Worker stations start at slot 1, so the number of
        # worker pairs cannot exceed the belt length minus one.
        if num_worker_pairs > belt_length - 1:
            raise ValueError("Number of worker pairs cannot exceed belt length - 1.")

        self.num_worker_pairs = num_worker_pairs
        self.belt_length = belt_length
        self.num_belts = num_belts
        self.strategy_name = strategy_name

        # Create the conveyor belts.
        self.belts = [ConveyorBelt(belt_length) for _ in range(num_belts)]

        # Select the appropriate worker strategy.
        if strategy_name == "individual":
            self.strategy = IndividualStrategy()
        elif strategy_name == "team":
            self.strategy = TeamStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        # Create the pairs of workers.
        # Worker stations are indexed from 1 to num_worker_pairs.
        self.workers = [(Worker(f"{i+1}A", self.strategy), Worker(f"{i+1}B", self.strategy)) for i in range(self.num_worker_pairs)]

    def run_step(self):
        """Runs a single step of the simulation."""
        # 1. Workers act first. This allows them to pick up components from the
        #    current state of the belt and place finished products on empty slots
        #    before the belt moves.
        for i in range(self.num_worker_pairs):
            worker_a, worker_b = self.workers[i]
            # The station index corresponds to the belt slot number.
            station_index = i + 1
            # Worker A acts, with Worker B as its partner.
            worker_a.act(worker_b, self.belts, station_index)
            # Worker B acts, with Worker A as its partner.
            worker_b.act(worker_a, self.belts, station_index)

        # 2. Advance all belts. This moves all items one step down the line.
        #    The last item falls off, and slot 0 becomes empty.
        for belt in self.belts:
            belt.step()

        # 3. Add new components to the start of the belt.
        #    This happens only if a worker hasn't already placed a finished
        #    product in the first slot during their turn.
        for belt in self.belts:
            if belt.slots[0] is None:
                # A new component ('A' or 'B') is added randomly.
                item = random.choice(['A', 'B'])
                belt.push_item(item)

    def display(self):
        """Prints the current state of the simulation to the console."""
        total_finished = self.get_total_finished_products()
        for i, belt in enumerate(self.belts):
            print(f"Belt {i}: {belt}")
        print(f"Finished Products: {total_finished}")
        print("-" * 20)

    def get_total_finished_products(self):
        """Calculates the total number of products made by all workers."""
        return sum(w.products_made for pair in self.workers for w in pair)

    def run_simulation(self, steps, quiet=False):
        """
        Runs the full simulation for a given number of steps.

        Args:
            steps (int): The total number of steps to run.
            quiet (bool): If True, suppresses step-by-step output and prints only
                          the final JSON result.
        """
        # Main simulation loop.
        for step in range(1, steps + 1):
            if not quiet:
                print(f"--- Step {step} ---")
            self.run_step()
            if not quiet:
                self.display()

        # After the loop, gather all the final statistics.
        total_finished = self.get_total_finished_products()
        missed_a = sum(belt.missed_a for belt in self.belts)
        missed_b = sum(belt.missed_b for belt in self.belts)

        # If not in quiet mode, print a detailed summary.
        if not quiet:
            print("\n--- Simulation Finished ---")
            print(f"Total steps: {steps}")
            print(f"Total finished products: {total_finished}")
            print(f"Total missed A components: {missed_a}")
            print(f"Total missed B components: {missed_b}")

            print("\n--- Configuration Used ---")
            print("To run this configuration again:")
            print(f"BELT_LENGTH={self.belt_length} NUM_WORKER_PAIRS={self.num_worker_pairs} STRATEGY={self.strategy_name} python simulation.py")

            print("\n--- Recommended Configuration ---")
            print("export BELT_LENGTH=15")
            print("export NUM_WORKER_PAIRS=3")
            print("export STRATEGY=team")
            print("# Then run: python simulation.py")

        # Always print the final JSON data for reporting purposes.
        output_data = {
            "products_created": {
                "C": total_finished
            },
            "missed_a": missed_a,
            "missed_b": missed_b
        }
        print(json.dumps(output_data))


if __name__ == "__main__":
    # This block runs when the script is executed directly.
    load_dotenv()  # Load environment variables from a .env file if it exists.

    # Get configuration from environment variables, using sensible defaults.
    belt_length = int(os.getenv("BELT_LENGTH", 10))
    num_worker_pairs = int(os.getenv("NUM_WORKER_PAIRS", 3))
    num_belts = int(os.getenv("NUM_BELTS", 1))
    strategy = os.getenv("STRATEGY", "individual")
    steps = int(os.getenv("STEPS", 100))
    # Check for a QUIET flag to suppress detailed output.
    quiet = os.getenv("QUIET", "false").lower() in ("true", "1", "t")

    try:
        # Create and run the simulation with the specified configuration.
        sim = Simulation(
            num_worker_pairs=num_worker_pairs,
            belt_length=belt_length,
            num_belts=num_belts,
            strategy_name=strategy
        )
        sim.run_simulation(steps, quiet)
    except ValueError as e:
        # Catch and report any configuration errors.
        print(f"Error: {e}")
