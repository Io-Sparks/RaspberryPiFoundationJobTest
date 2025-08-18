import threading
import time
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
        self.items = deque()

        # A lock to protect the belt from simultaneous access during add/remove
        self.lock = threading.Lock()

        # Semaphore to track the number of items on the belt.
        # Consumers wait on this if it's 0 (empty).
        self.filled_slots = threading.Semaphore(0)

        # Semaphore to track the number of empty slots on the belt.
        # Producers wait on this if it's 0 (full).
        self.empty_slots = threading.Semaphore(capacity)

    def put(self, item: int, timeout: float = None) -> bool:
        """
        Places an item on the conveyor belt.
        If the belt is full, the producer thread will block until a slot is free
        or the timeout is reached.
        Returns True if the item was put, False if it timed out.
        """
        # Acquire a permit for an empty slot. Blocks if belt is full.
        if not self.empty_slots.acquire(timeout=timeout):
            return False

        # Now that we have a permit, acquire the lock to modify the belt
        with self.lock:
            self.items.append(item)

        # Release a permit for a filled slot, signaling to consumers.
        self.filled_slots.release()
        return True

    def take(self, timeout: float = None) -> int | None:
        """
        Takes an item from the conveyor belt.
        If the belt is empty, the consumer thread will block until an item is available
        or the timeout is reached.
        Returns the item, or None if it timed out.
        """
        # Acquire a permit for a filled slot. Blocks if belt is empty.
        if not self.filled_slots.acquire(timeout=timeout):
            return None

        # Now that we have a permit, acquire the lock to modify the belt
        with self.lock:
            item = self.items.popleft()

        # Release a permit for an empty slot, signaling to producers.
        self.empty_slots.release()
        return item

    def is_empty(self) -> bool:
        """Returns True if the belt is empty."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Returns True if the belt is full."""
        return len(self.items) == self.capacity

    def __len__(self) -> int:
        """Returns the number of items currently on the belt."""
        return len(self.items)
