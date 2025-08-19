import argparse
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
        # 1. Workers perform actions based on the current state of the belts.
        # Worker pair `i` is stationed at belt slot `i+1`.
        for i in range(self.num_worker_pairs):
            worker_a, worker_b = self.workers[i]
            station_index = i + 1
            worker_a.act(worker_b, self.belts, station_index)
            worker_b.act(worker_a, self.belts, station_index)

        # 2. After all workers have acted, advance all belts.
        for belt in self.belts:
            belt.step_with_random_item()

    def display(self):
        total_finished = self.get_total_finished_products()
        for i, belt in enumerate(self.belts):
            print(f"Belt {i}: {belt}")
        print(f"Finished Products: {total_finished}")
        print("-" * 20)

    def get_total_finished_products(self):
        return sum(w.products_made for pair in self.workers for w in pair)

    def run_simulation(self, steps):
        for step in range(1, steps + 1):
            print(f"--- Step {step} ---")
            self.run_step()
            self.display()
        
        total_finished = self.get_total_finished_products()
        missed_a = sum(belt.missed_a for belt in self.belts)
        missed_b = sum(belt.missed_b for belt in self.belts)
        print("\n--- Simulation Finished ---")
        print(f"Total steps: {steps}")
        print(f"Total finished products: {total_finished}")
        print(f"Total missed A components: {missed_a}")
        print(f"Total missed B components: {missed_b}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a conveyor belt simulation.")
    parser.add_argument("--belt-length", type=int, default=10, help="Length of the conveyor belts.")
    parser.add_argument("--num-worker-pairs", type=int, default=3, help="Number of worker pairs.")
    parser.add_argument("--num-belts", type=int, default=1, help="Number of conveyor belts.")
    parser.add_argument("--strategy", type=str, default="individual", help="Worker strategy (individual or team).")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps to run the simulation for.")
    args = parser.parse_args()

    try:
        sim = Simulation(
            num_worker_pairs=args.num_worker_pairs,
            belt_length=args.belt_length,
            num_belts=args.num_belts,
            strategy_name=args.strategy
        )
        sim.run_simulation(args.steps)
    except ValueError as e:
        print(f"Error: {e}")
