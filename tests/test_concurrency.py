import unittest
import time
from conveyor import ConveyorBelt, Producer, Consumer


class TestConcurrency(unittest.TestCase):

    def test_item_integrity_under_load(self):
        """
        Runs a full simulation with multiple producers and consumers
        and verifies that no items are lost or duplicated.
        """
        belt_capacity = 20
        num_producers = 5
        num_consumers = 5
        simulation_duration = 2  # seconds

        belt = ConveyorBelt(capacity=belt_capacity)

        # Create producers and consumers using the current constructor
        producers = [
            Producer(belt, i) for i in range(num_producers)
        ]
        consumers = [
            Consumer(belt, i) for i in range(num_consumers)
        ]

        # Start all threads
        for p in producers:
            p.start()
        for c in consumers:
            c.start()

        # Let the simulation run for a while
        time.sleep(simulation_duration)

        # Stop the simulation by calling the stop() method on each thread
        for p in producers:
            p.stop()
        for c in consumers:
            c.stop()

        # Wait for all threads to finish
        for p in producers:
            p.join()
        for c in consumers:
            c.join()

        # Tally the results
        total_produced = sum(p.items_produced for p in producers)
        total_consumed = sum(c.items_consumed for c in consumers)
        items_left_on_belt = len(belt)

        print(f"\n--- Concurrency Test Results ---")
        print(f"Total items produced: {total_produced}")
        print(f"Total items consumed: {total_consumed}")
        print(f"Items left on belt: {items_left_on_belt}")

        # The crucial check
        self.assertEqual(
            total_produced,
            total_consumed + items_left_on_belt,
            "Mismatch between produced and consumed items!"
        )


if __name__ == '__main__':
    unittest.main()
