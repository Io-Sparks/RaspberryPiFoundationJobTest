import threading
import time
import random

from .conveyor_belt import ConveyorBelt

class Consumer(threading.Thread):
    """
    A thread that takes items from the conveyor belt and "consumes" them.
    """

    def __init__(self, belt: ConveyorBelt, stop_event: threading.Event, consumer_id: int):
        super().__init__()
        self.belt = belt
        self.stop_event = stop_event
        self.name = f"Consumer-{consumer_id}"
        self.items_consumed = 0

    def run(self):
        while not self.stop_event.is_set():
            try:
                # 1. Take an item from the belt with a timeout
                item = self.belt.take(timeout=1.0)
                if item is not None:
                    self.items_consumed += 1
                    # 2. "Consume" the item
                    consumption_time = random.uniform(0.2, 0.8)
                    print(f"{self.name}: Consumed item {item}.")
                    time.sleep(consumption_time)
                else:
                    # If the belt is empty, we just loop and check the stop_event again
                    print(f"{self.name}: Belt is empty. Retrying...")

            except Exception as e:
                print(f"{self.name} encountered an error: {e}")
                break
        print(f"{self.name} is shutting down.")
