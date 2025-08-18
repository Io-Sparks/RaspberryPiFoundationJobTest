import unittest
from conveyor import ConveyorBelt


class TestConveyorBelt(unittest.TestCase):

    def test_initialization(self):
        """Test that the belt is initialized correctly."""
        belt = ConveyorBelt(capacity=10)
        self.assertEqual(belt.capacity, 10)
        self.assertTrue(belt.is_empty())
        self.assertFalse(belt.is_full())

    def test_put_and_take_item(self):
        """Test basic put and take operations."""
        belt = ConveyorBelt(capacity=5)
        item = 123 # Items are integers

        belt.put(item)
        self.assertFalse(belt.is_empty())

        taken_item = belt.take()
        self.assertEqual(taken_item, item)
        self.assertTrue(belt.is_empty())

    def test_is_full(self):
        """Test the is_full method."""
        belt = ConveyorBelt(capacity=2)
        belt.put(1)
        self.assertFalse(belt.is_full())

        belt.put(2)
        self.assertTrue(belt.is_full())

    def test_is_empty(self):
        """Test the is_empty method."""
        belt = ConveyorBelt(capacity=2)
        self.assertTrue(belt.is_empty())

        belt.put(1)
        self.assertFalse(belt.is_empty())

    def test_len(self):
        """Test the __len__ method."""
        belt = ConveyorBelt(capacity=3)
        self.assertEqual(len(belt), 0)
        belt.put(1)
        self.assertEqual(len(belt), 1)
        belt.put(2)
        self.assertEqual(len(belt), 2)
        belt.take()
        self.assertEqual(len(belt), 1)


if __name__ == '__main__':
    unittest.main()
