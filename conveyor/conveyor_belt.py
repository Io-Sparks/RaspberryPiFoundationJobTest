import threading
from collections import deque

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
