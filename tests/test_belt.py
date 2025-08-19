
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from belt import ConveyorBelt

class TestConveyorBelt(unittest.TestCase):

    def test_belt_initialization(self):
        print("\n--- Running Test: test_belt_initialization ---")
        belt = ConveyorBelt(10)
        self.assertEqual(len(belt.slots), 10)
        self.assertIsNone(belt.slots[0])

    def test_belt_step(self):
        print("\n--- Running Test: test_belt_step ---")
        belt = ConveyorBelt(10)
        belt.push_item("A")
        belt.step()
        self.assertIsNone(belt.slots[0])
        self.assertEqual(belt.slots[1], "A")

    def test_belt_step_with_full_belt(self):
        print("\n--- Running Test: test_belt_step_with_full_belt ---")
        belt = ConveyorBelt(10)
        for i in range(10):
            belt.push_item(i)
            belt.step()
        self.assertEqual(belt.slots[9], 1)

    def test_belt_is_empty(self):
        print("\n--- Running Test: test_belt_is_empty ---")
        belt = ConveyorBelt(10)
        self.assertTrue(belt.is_empty())
        belt.push_item("A")
        self.assertFalse(belt.is_empty())

    def test_belt_push_item(self):
        print("\n--- Running Test: test_belt_push_item ---")
        belt = ConveyorBelt(10)
        belt.push_item("A")
        self.assertEqual(belt.slots[0], "A")

if __name__ == '__main__':
    unittest.main()
