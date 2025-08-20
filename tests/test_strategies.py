
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies import IndividualStrategy, TeamStrategy, HiveMindStrategy
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
        strategy.act(worker, partner, [belt], 0)
        self.assertEqual(worker.assembling_time_left, 4)

        # The strategy should do nothing while the worker is assembling
        strategy.act(worker, partner, [belt], 0)
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
        strategy.act(worker, partner, [belt], 0)
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

    def test_team_strategy_pass_to_partner(self):
        print("\n--- Running Test: test_team_strategy_pass_to_partner ---")
        strategy = TeamStrategy()
        worker = Worker(0, strategy)
        partner = Worker(1, strategy)
        worker.pickup("A")
        partner.pickup("B")
        belt = ConveyorBelt(10)
        # Worker has 'A', Partner has 'B'. Worker should pass 'A' to partner.
        strategy.act(worker, partner, [belt], 0)
        self.assertIsNone(worker.hand_left)
        self.assertEqual(partner.hand_left, "B")
        self.assertEqual(partner.hand_right, "A")


class TestHiveMindStrategy(unittest.TestCase):

    # def test_hive_mind_place_product_priority(self):
    #     print("\n--- Running Test: test_hive_mind_place_product_priority ---")
    #     strategy = HiveMindStrategy()
    #     belt = ConveyorBelt(10)
    #     workers = [Worker(i, strategy) for i in range(4)]
    #     # Worker 0 can take a component
    #     belt.slots[0] = "A"
    #
    #     # Worker 2 will have a finished product.
    #     # To get a 'C', the worker must assemble it first.
    #     workers[2].pickup("A")
    #     workers[2].pickup("B")
    #     workers[2].start_assembly()
    #     for _ in range(4):
    #         workers[2].step_assembly()
    #
    #     # Now worker 2 is holding a 'C' legitimately.
    #     self.assertEqual(workers[2].hand_left, "C")
    #
    #     # Hive mind should choose to place the product, as it's the highest priority
    #     strategy.hive_act(workers, [belt])
    #     self.assertIsNone(workers[2].hand_left)
    #     self.assertEqual(belt.slots[2], "C")

    def test_hive_mind_assemble_priority(self):
        print("\n--- Running Test: test_hive_mind_assemble_priority ---")
        strategy = HiveMindStrategy()
        belt = ConveyorBelt(10)
        workers = [Worker(i, strategy) for i in range(4)]
        # Worker 0 can take a component
        belt.slots[0] = "A"
        # Worker 1 can assemble
        workers[1].pickup("A")
        workers[1].pickup("B")

        # Hive mind should choose to assemble, as it's the highest priority available
        strategy.hive_act(workers, [belt])
        self.assertTrue(workers[1].is_assembling())


if __name__ == '__main__':
    unittest.main()
