import threading
import time
import random
import itertools

from .conveyor_belt import ConveyorBelt

# Using a simple counter for unique item serial numbers
item_serial_counter = itertools.count(1)

class Producer(threading.Thread):
    """
    A thread that produces items and puts them on the conveyor belt.
    """

    def __init__(self, belt: ConveyorBelt, stop_event: threading.Event, producer_id: int):
        super().__init__()
        self.belt = belt
        self.stop_event = stop_event
        self.name = f"Producer-{producer_id}"

    def run(self):
        while not self.stop_event.is_set():
            try:
                # 1. Produce a new item
                item = next(item_serial_counter)

                # Simulate time taken to produce the item
                production_time = random.uniform(0.1, 0.5)
                time.sleep(production_time)
                print(
                    f"{self.name}: Produced item {item} in {production_time:.2f}s.")

                # 2. Place the item on the belt
                self.belt.put_item(item, self.name)

            except Exception as e:
                print(f"{self.name} encountered an error: {e}")
                break
        print(f"{self.name} is shutting down.")
