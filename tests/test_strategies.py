
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies import IndividualStrategy
from worker import Worker
from belt import ConveyorBelt

class TestIndividualStrategy(unittest.TestCase):

    def test_individual_strategy_pickup(self):
        print("\n--- Running Test: test_individual_strategy_pickup ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        belt = ConveyorBelt(10)
        belt.push_item("A")
        strategy.act(worker, partner, [belt], 0)
        self.assertEqual(worker.hand_left, "A")

    def test_individual_strategy_start_assembly(self):
        print("\n--- Running Test: test_individual_strategy_start_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        strategy.act(worker, partner, [belt], 0)
        self.assertEqual(worker.assembling_time_left, 4)

    def test_individual_strategy_step_assembly(self):
        print("\n--- Running Test: test_individual_strategy_step_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        strategy.act(worker, partner, [belt], 0) # start assembly
        strategy.act(worker, partner, [belt], 0) # step assembly
        self.assertEqual(worker.assembling_time_left, 3)

    def test_individual_strategy_finish_assembly(self):
        print("\n--- Running Test: test_individual_strategy_finish_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        for _ in range(5):
            strategy.act(worker, partner, [belt], 0)
        self.assertEqual(worker.hand_left, "C")

if __name__ == '__main__':
    unittest.main()
