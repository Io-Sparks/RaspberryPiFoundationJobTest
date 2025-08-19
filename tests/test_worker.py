
import unittest
from worker import Worker, A, B, C
from belt import Belt
from strategies import IndividualStrategy

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
        worker.act(partner=None, belts=[Belt(1)], station_index=0)

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

        belt = Belt(5)
        belt.push(A) # Add a component the worker might otherwise take

        # The strategy should do nothing because the worker is busy
        worker.act(partner=None, belts=[belt], station_index=0)

        # No action should have been taken
        self.assertEqual(worker.assembling_time_left, 3) # Timer is not stepped by act()
        self.assertEqual(belt.items, [A, None, None, None, None])
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

if __name__ == '__main__':
    unittest.main()
