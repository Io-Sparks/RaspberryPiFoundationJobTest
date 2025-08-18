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

    def run(self):
        while not self.stop_event.is_set():
            try:
                # 1. Take an item from the belt
                item = self.belt.take_item(self.name)

                # 2. "Consume" the item
                consumption_time = random.uniform(0.2, 0.8)
                print(
                    f"{self.name}: Consuming item {item} (will take {consumption_time:.2f}s)...")
                time.sleep(consumption_time)
                print(f"{self.name}: Finished consuming item {item}.")

            except Exception as e:
                # This can happen if the main thread shuts down while a consumer
                # is waiting on a semaphore.
                if not self.stop_event.is_set():
                    print(f"{self.name} encountered an error: {e}")
                break
        print(f"{self.name} is shutting down.")
