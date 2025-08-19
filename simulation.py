import json
import random
import os
from dotenv import load_dotenv
from belt import ConveyorBelt
from worker import Worker
from strategies import IndividualStrategy, TeamStrategy

class Simulation:
    def __init__(self, num_worker_pairs, belt_length, num_belts, strategy_name):
        # Per our design constraints, worker stations start at slot 1.
        # This means the number of workers cannot exceed the belt length minus one.
        if num_worker_pairs > belt_length -1:
            raise ValueError("Number of worker pairs cannot exceed belt length - 1.")
        
        self.num_worker_pairs = num_worker_pairs
        self.belt_length = belt_length
        self.num_belts = num_belts
        self.strategy_name = strategy_name

        self.belts = [ConveyorBelt(belt_length) for _ in range(num_belts)]

        if strategy_name == "individual":
            self.strategy = IndividualStrategy()
        elif strategy_name == "team":
            self.strategy = TeamStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        # Worker stations are indexed from 1 to num_worker_pairs
        self.workers = [(Worker(f"{i+1}A", self.strategy), Worker(f"{i+1}B", self.strategy)) for i in range(self.num_worker_pairs)]

    def run_step(self):
        # 1. Workers act on the current state of the belt.
        # This allows them to place finished products on empty slots before
        # new components are added.
        for i in range(self.num_worker_pairs):
            worker_a, worker_b = self.workers[i]
            station_index = i + 1
            worker_a.act(worker_b, self.belts, station_index)
            worker_b.act(worker_a, self.belts, station_index)

        # 2. Advance the belts. This moves everything down.
        # The last item is discarded, and slot 0 becomes empty.
        for belt in self.belts:
            belt.step()

        # 3. Add new components to the start of the belt for the next step,
        # but only if a worker hasn't already placed a finished product there.
        for belt in self.belts:
            if belt.slots[0] is None:
                item = random.choice(['A', 'B'])
                belt.push_item(item)

    def display(self):
        total_finished = self.get_total_finished_products()
        for i, belt in enumerate(self.belts):
            print(f"Belt {i}: {belt}")
        print(f"Finished Products: {total_finished}")
        print("-" * 20)

    def get_total_finished_products(self):
        return sum(w.products_made for pair in self.workers for w in pair)

    def run_simulation(self, steps, quiet=False):
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


        # Output JSON for reporting
        output_data = {
            "products_created": {
                "C": total_finished
            },
            "missed_a": missed_a,
            "missed_b": missed_b
        }
        print(json.dumps(output_data))


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    # Get configuration from environment variables with defaults
    belt_length = int(os.getenv("BELT_LENGTH", 10))
    num_worker_pairs = int(os.getenv("NUM_WORKER_PAIRS", 3))
    num_belts = int(os.getenv("NUM_BELTS", 1))
    strategy = os.getenv("STRATEGY", "individual")
    steps = int(os.getenv("STEPS", 100))
    quiet = os.getenv("QUIET", "false").lower() in ("true", "1", "t")

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
