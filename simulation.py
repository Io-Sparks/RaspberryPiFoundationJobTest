
import argparse
import os
import json
from collections import Counter

from belt import ConveyorBelt
from strategies import IndividualStrategy, TeamStrategy
from worker import Worker


class Simulation:
    def __init__(self, num_worker_pairs, belt_length, strategy_name):
        if num_worker_pairs * 2 > belt_length:
            raise ValueError("Number of workers cannot exceed the belt length.")

        self.num_worker_pairs = num_worker_pairs
        self.belt_length = belt_length
        self.strategy_name = strategy_name
        self.quiet_mode = os.environ.get("QUIET") == "true"

        self.belt = ConveyorBelt(belt_length)

        if strategy_name == 'individual':
            self.strategy = IndividualStrategy()
        elif strategy_name == 'team':
            self.strategy = TeamStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        self.workers = []
        for i in range(num_worker_pairs * 2):
            self.workers.append(Worker(i, self.strategy))

    def run(self, steps):
        for step in range(steps):
            if not self.quiet_mode:
                print(f"Step {step + 1}")
            self.run_step()

        self.print_results()

    def run_step(self):
        for worker in self.workers:
            if worker.is_assembling():
                worker.step_assembly()

        self.belt.step_with_random_item()

        if self.strategy_name == 'individual':
            for i in range(self.num_worker_pairs * 2):
                station_index = i % self.belt_length
                self.strategy.act(self.workers[i], None, self.belt, station_index)

        elif self.strategy_name == 'team':
            for i in range(self.num_worker_pairs):
                worker1_idx = 2 * i
                worker2_idx = 2 * i + 1
                worker1 = self.workers[worker1_idx]
                worker2 = self.workers[worker2_idx]
                station_index = i % self.belt_length

                self.strategy.act(worker1, worker2, self.belt, station_index)
                self.strategy.act(worker2, worker1, self.belt, station_index)

        if not self.quiet_mode:
            print(f"  Belt: {self.belt.slots}")

    def print_results(self):
        finished_products = sum(1 for worker in self.workers if worker.is_holding_product()) + self.belt.slots.count('C')
        held_components = Counter()
        for worker in self.workers:
            if worker.hand_left in ['A', 'B']:
                held_components[worker.hand_left] += 1
            if worker.hand_right in ['A', 'B']:
                held_components[worker.hand_right] += 1

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
            print("\n--- Simulation Results ---")
            print(f"  - Finished Products: {finished_products}")
            print(f"  - Missed A: {self.belt.missed_a}")
            print(f"  - Missed B: {self.belt.missed_b}")
            print(f"  - Held A: {held_components['A']}")
            print(f"  - Held B: {held_components['B']}")
            print("------------------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a factory simulation.")
    parser.add_argument("--belt-length", type=int, default=10, help="Length of the conveyor belt.")
    parser.add_argument("--num-pairs", type=int, default=3, help="Number of worker pairs.")
    parser.add_argument("--strategy", type=str, default='team', choices=['individual', 'team'], help="Strategy for the workers.")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps to run the simulation for.")
    args = parser.parse_args()

    belt_length = int(os.environ.get('BELT_LENGTH', args.belt_length))
    num_pairs = int(os.environ.get('NUM_WORKER_PAIRS', args.num_pairs))
    strategy = os.environ.get('STRATEGY', args.strategy)
    steps = int(os.environ.get('STEPS', args.steps))

    simulation = Simulation(num_pairs, belt_length, strategy)
    simulation.run(steps)
