import threading
import time
import random
import itertools
import logging

from .conveyor_belt import ConveyorBelt

# Using a simple counter for unique item serial numbers
item_serial_counter = itertools.count(1)

class Producer(threading.Thread):
    """
    A thread that produces items and puts them on the conveyor belt.
    """

    def __init__(self, belt: ConveyorBelt, producer_id: int):
        super().__init__()
        self.belt = belt
        self._stop_event = threading.Event()
        self.name = f"Producer-{producer_id}"
        self.items_produced = 0
        self.log = logging.getLogger(self.name)

    def stop(self):
        """Signals the thread to stop."""
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                # 1. Produce a new item
                item = next(item_serial_counter)

                # Simulate time taken to produce the item
                production_time = random.uniform(0.1, 0.5)
                time.sleep(production_time)

                # 2. Place the item on the belt with a timeout
                if self.belt.put(item, timeout=1.0):
                    self.log.info(f"Placed item {item} on the belt.")
                    self.items_produced += 1
                else:
                    # If the belt is full, we log a warning and check the stop_event again
                    self.log.warning("Belt is full. Retrying...")

            except Exception as e:
                self.log.error(f"Encountered an unhandled error: {e}", exc_info=True)
                break
        self.log.info("Shutting down.")
