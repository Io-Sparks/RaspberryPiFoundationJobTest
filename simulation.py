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
from typing import List, Tuple
from belt import ConveyorBelt
from worker import Worker
from strategies import IndividualStrategy, TeamStrategy, HiveMindStrategy, WorkerStrategy

class Simulation:
    """Manages the setup and execution of the factory simulation."""

    def __init__(self, num_worker_pairs: int, belt_length: int, num_belts: int, strategy_name: str) -> None:
        """
        Initializes the simulation environment.

        Args:
            num_worker_pairs (int): The number of pairs of workers.
            belt_length (int): The length of the conveyor belts.
            num_belts (int): The number of conveyor belts.
            strategy_name (str): The name of the strategy to use ("individual", "team", or "hivemind").

        Raises:
            ValueError: If the configuration is invalid (e.g., too many workers for the belt size).
        """
        # Enforce the physical constraint that the number of workers cannot exceed the belt length.
        if num_worker_pairs * 2 > belt_length:
            raise ValueError(f"Configuration error: The number of workers ({num_worker_pairs * 2}) cannot exceed the belt length ({belt_length}).")

        self.num_worker_pairs: int = num_worker_pairs
        self.belt_length: int = belt_length
        self.num_belts: int = num_belts
        self.strategy_name: str = strategy_name

        self.belts: List[ConveyorBelt] = [ConveyorBelt(belt_length) for _ in range(num_belts)]

        # Select the appropriate worker strategy.
        self.strategy: WorkerStrategy
        if strategy_name == "individual":
            self.strategy = IndividualStrategy()
        elif strategy_name == "team":
            self.strategy = TeamStrategy()
        elif strategy_name == "hivemind":
            self.strategy = HiveMindStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        # Create the pairs of workers.
        self.worker_pairs: List[Tuple[Worker, Worker]] = [(Worker(f"{i+1}A", self.strategy), Worker(f"{i+1}B", self.strategy)) for i in range(self.num_worker_pairs)]
        # Create a flat list of all workers for the hivemind strategy
        self.all_workers: List[Worker] = [worker for pair in self.worker_pairs for worker in pair]

    def run_step(self) -> None:
        """Runs a single step of the simulation."""
        # 1. Advance all assembly timers.
        for worker in self.all_workers:
            worker.step_assembly()

        # 2. Workers act.
        if self.strategy_name == "hivemind":
            # For the hivemind strategy, make a single, globally optimal move.
            self.strategy.hive_act(self.all_workers, self.belts)
        else:
            # For other strategies, each worker acts individually or in pairs.
            for i in range(self.num_worker_pairs):
                worker_a, worker_b = self.worker_pairs[i]
                station_index = i + 1
                worker_a.act(worker_b, self.belts, station_index)
                worker_b.act(worker_a, self.belts, station_index)

        # 3. Advance all belts.
        for belt in self.belts:
            belt.step()

        # 4. Add new components to the start of the belt.
        for belt in self.belts:
            if belt.slots[0] is None:
                item = random.choice(['A', 'B'])
                belt.push_item(item)

    def display(self) -> None:
        """Prints the current state of the simulation to the console."""
        total_finished = self.get_total_finished_products()
        for i, belt in enumerate(self.belts):
            print(f"Belt {i}: {belt}")
        print(f"Finished Products: {total_finished}")
        print("-" * 20)

    def get_total_finished_products(self) -> int:
        """Calculates the total number of products made by all workers."""
        return sum(w.products_made for pair in self.worker_pairs for w in pair)

    def run_simulation(self, steps: int, quiet: bool = False) -> None:
        """
        Runs the full simulation for a given number of steps.

        Args:
            steps (int): The total number of steps to run.
            quiet (bool): If True, suppresses step-by-step output and prints only
                          the final JSON result.
        """
        for step in range(1, steps + 1):
            if not quiet:
                print(f"--- Step {step} ---")
            self.run_step()
            if not quiet:
                self.display()

        total_finished = self.get_total_finished_products()
        missed_a = sum(belt.missed_a for belt in self.belts)
        missed_b = sum(belt.missed_b for belt in self.belts)

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

        output_data = {
            "products_created": {
                "C": total_finished
            },
            "missed_a": missed_a,
            "missed_b": missed_b
        }
        print(json.dumps(output_data))


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from a .env file if it exists.

    belt_length: int = int(os.getenv("BELT_LENGTH", 10))
    num_worker_pairs: int = int(os.getenv("NUM_WORKER_PAIRS", 3))
    num_belts: int = int(os.getenv("NUM_BELTS", 1))
    strategy: str = os.getenv("STRATEGY", "individual")
    steps: int = int(os.getenv("STEPS", 100))
    quiet: bool = os.getenv("QUIET", "false").lower() in ("true", "1", "t")

    try:
        sim = Simulation(
            num_worker_pairs=num_worker_pairs,
            belt_length=belt_length,
            num_belts=num_belts,
            strategy_name=strategy
        )
        sim.run_simulation(steps, quiet)
    except ValueError as e:
        print(f"Error: {e}")
