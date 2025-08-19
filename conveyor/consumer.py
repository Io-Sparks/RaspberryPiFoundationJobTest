import threading
import time
import random
import logging

from .conveyor_belt import ConveyorBelt

class Consumer(threading.Thread):
    """
    A thread that takes items from the conveyor belt and "consumes" them.
    """

    def __init__(self, belt: ConveyorBelt, consumer_id: int):
        super().__init__()
        self.belt = belt
        self._stop_event = threading.Event()
        self.name = f"Consumer-{consumer_id}"
        self.items_consumed = 0
        self.log = logging.getLogger(self.name)

    def stop(self):
        """Signals the thread to stop."""
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                # 1. Take an item from the belt with a timeout
                item = self.belt.take(timeout=1.0)
                if item is not None:
                    self.items_consumed += 1
                    # 2. "Consume" the item
                    consumption_time = random.uniform(0.2, 0.8)
                    self.log.info(f"Consumed item {item}.")
                    time.sleep(consumption_time)
                else:
                    # If the belt is empty, we log it and check the stop_event again
                    self.log.info("Belt is empty. Retrying...")

            except Exception as e:
                self.log.error(f"Encountered an unhandled error: {e}", exc_info=True)
                break
        self.log.info("Shutting down.")
