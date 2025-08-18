import threading
import time
import random
from collections import deque
import itertools

# --- Configuration ---
BELT_CAPACITY = 10
NUM_PRODUCERS = 2
NUM_CONSUMERS = 3
SIMULATION_DURATION_SECONDS = 15
# ---------------------

# Using a simple counter for unique item serial numbers
item_serial_counter = itertools.count(1)


class ConveyorBelt:
    """
    Represents the shared conveyor belt.

    This class is thread-safe and uses Semaphores to coordinate producers
    and consumers, preventing them from adding to a full belt or taking
    from an empty one.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Belt capacity must be positive.")

        self.capacity = capacity
        # The belt itself, using a deque for efficient appends and pops
        self.belt = deque()

        # A lock to protect the belt from simultaneous access during add/remove
        self.lock = threading.Lock()

        # Semaphore to track the number of items on the belt.
        # Consumers wait on this if it's 0 (empty).
        self.filled_slots = threading.Semaphore(0)

        # Semaphore to track the number of empty slots on the belt.
        # Producers wait on this if it's 0 (full).
        self.empty_slots = threading.Semaphore(capacity)

    def put_item(self, item: int, producer_name: str):
        """
        Places an item on the conveyor belt.
        If the belt is full, the producer thread will block until a slot is free.
        """
        # Acquire a permit for an empty slot. Blocks if belt is full.
        self.empty_slots.acquire()

        # Now that we have a permit, acquire the lock to modify the belt
        with self.lock:
            self.belt.append(item)
            print(
                f"{producer_name}: Placed item {item} on the belt. (Belt size: {len(self.belt)})")

        # Release a permit for a filled slot, signaling to consumers.
        self.filled_slots.release()

    def take_item(self, consumer_name: str) -> int:
        """
        Takes an item from the conveyor belt.
        If the belt is empty, the consumer thread will block until an item is available.
        """
        # Acquire a permit for a filled slot. Blocks if belt is empty.
        self.filled_slots.acquire()

        # Now that we have a permit, acquire the lock to modify the belt
        with self.lock:
            item = self.belt.popleft()
            print(
                f"{consumer_name}: Took item {item} from the belt. (Belt size: {len(self.belt)})")

        # Release a permit for an empty slot, signaling to producers.
        self.empty_slots.release()
        return item


class Producer(threading.Thread):
    """
    A thread that produces items and puts them on the conveyor belt.
    """

    def __init__(self, belt: ConveyorBelt, stop_event: threading.Event):
        super().__init__()
        self.belt = belt
        self.stop_event = stop_event
        self.name = f"Producer-{self.ident % 100}"

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


class Consumer(threading.Thread):
    """
    A thread that takes items from the conveyor belt and "consumes" them.
    """

    def __init__(self, belt: ConveyorBelt, stop_event: threading.Event):
        super().__init__()
        self.belt = belt
        self.stop_event = stop_event
        self.name = f"Consumer-{self.ident % 100}"

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


def main():
    """Sets up and runs the simulation."""
    print("Starting Conveyor Belt Simulation...")
    print(
        f"Configuration: Belt Capacity={BELT_CAPACITY}, Producers={NUM_PRODUCERS}, Consumers={NUM_CONSUMERS}")
    print("---------------------------------------------------------")

    # The shared resource
    belt = ConveyorBelt(BELT_CAPACITY)

    # An event to signal all threads to stop gracefully
    stop_event = threading.Event()

    threads = []
    # Create and start producer threads
    for _ in range(NUM_PRODUCERS):
        producer = Producer(belt, stop_event)
        threads.append(producer)
        producer.start()

    # Create and start consumer threads
    for _ in range(NUM_CONSUMERS):
        consumer = Consumer(belt, stop_event)
        threads.append(consumer)
        consumer.start()

    # Let the simulation run for the configured duration
    time.sleep(SIMULATION_DURATION_SECONDS)

    # Shutdown the simulation gracefully
    print("---------------------------------------------------------")
    print("Simulation time elapsed. Shutting down all threads...")
    stop_event.set()

    # The semaphores might be blocking, so we need to unblock them
    # to allow threads to check the stop_event and exit.
    for _ in range(NUM_PRODUCERS):
        belt.filled_slots.release()  # Unblock a waiting consumer
    for _ in range(NUM_CONSUMERS):
        belt.empty_slots.release()  # Unblock a waiting producer

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Simulation finished.")


if __name__ == "__main__":
    main()
