
import unittest
from worker import Worker, A, B, C
from belt import ConveyorBelt
from strategies import IndividualStrategy
from simulation import Simulation

class TestAssemblyProcess(unittest.TestCase):
    """
    Tests the worker's assembly process to ensure it follows the 4-tick delay rule.
    """

    def test_assembly_timer_starts(self):
        """
        Verify that a worker with components 'A' and 'B' starts the assembly timer.
        """
        worker = Worker("w1", IndividualStrategy())
        worker.hand_left = A
        worker.hand_right = B
        
        # The strategy should decide to start the assembly
        worker.act(partner=None, belts=[ConveyorBelt(1)], station_index=0)

        self.assertTrue(worker.is_assembling())
        self.assertEqual(worker.assembling_time_left, Worker.ASSEMBLY_TIME)
        self.assertEqual(worker.hand_left, A) # Hands should be unchanged
        self.assertEqual(worker.hand_right, B)

    def test_worker_is_locked_during_assembly(self):
        """
        Verify that a worker cannot interact with the belt while assembling.
        """
        worker = Worker("w1", IndividualStrategy())
        worker.hand_left = A
        worker.hand_right = B
        worker.start_assembly() # Manually start
        worker.assembling_time_left = 3 # Set timer to be in-progress

        belt = ConveyorBelt(5)
        belt.push_item(A) # Add a component the worker might otherwise take

        # The strategy should do nothing because the worker is busy
        worker.act(partner=None, belts=[belt], station_index=0)

        # No action should have been taken
        self.assertEqual(worker.assembling_time_left, 3) # Timer is not stepped by act()
        self.assertEqual(belt.slots, [A, None, None, None, None])
        self.assertEqual(worker.hand_left, A)

    def test_assembly_finishes_correctly_after_stepping(self):
        """
        Verify that the product 'C' appears after the timer is stepped down.
        """
        worker = Worker("w1", IndividualStrategy())
        worker.hand_left = A
        worker.hand_right = B
        worker.start_assembly()

        # Simulate the passing of time by stepping the assembly process
        for _ in range(Worker.ASSEMBLY_TIME - 1):
            worker.step_assembly()
        
        self.assertTrue(worker.is_assembling())
        self.assertEqual(worker.assembling_time_left, 1)

        # The final step that finishes the assembly
        worker.step_assembly()

        self.assertFalse(worker.is_assembling())
        self.assertEqual(worker.assembling_time_left, 0)
        self.assertEqual(worker.hand_left, C) # Hands now have the finished product
        self.assertIsNone(worker.hand_right)
        self.assertEqual(worker.products_made, 1)

class TestSimulationConstraints(unittest.TestCase):
    """
    Tests the physical constraints of the simulation setup.
    """

    def test_raises_error_for_too_many_workers(self):
        """
        Verify that the Simulation raises a ValueError if there are more workers than belt spaces.
        """
        with self.assertRaises(ValueError):
            Simulation(
                num_worker_pairs=6, # 12 workers
                belt_length=10,     # Only 10 spaces
                num_belts=1,
                strategy_name="individual"
            )

    def test_allows_valid_number_of_workers(self):
        """
        Verify that the Simulation initializes successfully with a valid number of workers.
        """
        try:
            Simulation(
                num_worker_pairs=5, # 10 workers
                belt_length=10,     # 10 spaces
                num_belts=1,
                strategy_name="individual"
            )
        except ValueError:
            self.fail("Simulation raised ValueError unexpectedly for a valid configuration.")

if __name__ == '__main__':
    unittest.main()
