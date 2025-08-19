
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker import Worker
from strategies import IndividualStrategy

class TestWorker(unittest.TestCase):

    def test_worker_initialization(self):
        print("\n--- Running Test: test_worker_initialization ---")
        worker = Worker(0, IndividualStrategy())
        self.assertEqual(worker.worker_id, 0)
        self.assertEqual(worker.hand_left, None)
        self.assertEqual(worker.hand_right, None)
        self.assertEqual(worker.assembling_time_left, 0)

    def test_worker_pickup(self):
        print("\n--- Running Test: test_worker_pickup ---")
        worker = Worker(0, IndividualStrategy())
        worker.pickup("A")
        self.assertEqual(worker.hand_left, "A")
        worker.pickup("B")
        self.assertEqual(worker.hand_right, "B")

    def test_worker_pickup_full_hands(self):
        print("\n--- Running Test: test_worker_pickup_full_hands ---")
        worker = Worker(0, IndividualStrategy())
        worker.pickup("A")
        worker.pickup("B")
        with self.assertRaises(Exception):
            worker.pickup("C")

    def test_worker_start_assembly(self):
        print("\n--- Running Test: test_worker_start_assembly ---")
        worker = Worker(0, IndividualStrategy())
        worker.pickup("A")
        worker.pickup("B")
        worker.start_assembly()
        self.assertEqual(worker.assembling_time_left, 4)

    def test_worker_step_assembly(self):
        print("\n--- Running Test: test_worker_step_assembly ---")
        worker = Worker(0, IndividualStrategy())
        worker.pickup("A")
        worker.pickup("B")
        worker.start_assembly()
        worker.step_assembly()
        self.assertEqual(worker.assembling_time_left, 3)

    def test_worker_finish_assembly(self):
        print("\n--- Running Test: test_worker_finish_assembly ---")
        worker = Worker(0, IndividualStrategy())
        worker.pickup("A")
        worker.pickup("B")
        worker.start_assembly()
        for _ in range(4):
            worker.step_assembly()
        self.assertEqual(worker.hand_left, "C")
        self.assertEqual(worker.hand_right, None)
        self.assertEqual(worker.assembling_time_left, 0)

if __name__ == '__main__':
    unittest.main()
