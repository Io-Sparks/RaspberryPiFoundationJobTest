
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies import IndividualStrategy, TeamStrategy
from worker import Worker
from belt import ConveyorBelt

class TestIndividualStrategy(unittest.TestCase):

    def test_individual_strategy_pickup(self):
        print("\n--- Running Test: test_individual_strategy_pickup ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        belt = ConveyorBelt(10)
        belt.slots[0] = "A"
        strategy.act(worker, partner, belt, 0)
        self.assertEqual(worker.hand_left, "A")

    def test_individual_strategy_start_assembly(self):
        print("\n--- Running Test: test_individual_strategy_start_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        strategy.act(worker, partner, belt, 0)
        self.assertEqual(worker.assembling_time_left, 4)
        self.assertTrue(worker.is_assembling())

    def test_individual_strategy_step_assembly(self):
        print("\n--- Running Test: test_individual_strategy_step_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        # Start assembly
        strategy.act(worker, partner, belt, 0)
        self.assertEqual(worker.assembling_time_left, 4)

        # The strategy should do nothing while the worker is assembling
        strategy.act(worker, partner, belt, 0)
        self.assertEqual(worker.assembling_time_left, 4)

        # The simulation loop is responsible for stepping the assembly
        worker.step_assembly()
        self.assertEqual(worker.assembling_time_left, 3)

    def test_individual_strategy_finish_assembly(self):
        print("\n--- Running Test: test_individual_strategy_finish_assembly ---")
        strategy = IndividualStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        worker.pickup("B")
        belt = ConveyorBelt(10)
        # Start assembly
        strategy.act(worker, partner, belt, 0)
        self.assertEqual(worker.assembling_time_left, 4)

        # Simulate the simulation loop advancing time
        for _ in range(4):
            worker.step_assembly()

        # After 4 steps, the assembly should be finished
        self.assertEqual(worker.assembling_time_left, 0)
        self.assertFalse(worker.is_assembling())
        self.assertEqual(worker.hand_left, "C")
        self.assertIsNone(worker.hand_right)


class TestTeamStrategy(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
