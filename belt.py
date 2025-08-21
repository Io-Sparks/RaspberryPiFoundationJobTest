"""
This module defines the core components of the factory simulation.

It includes the definitions for the components (A, B, C) and the ConveyorBelt
class, which manages the state and movement of items in the simulation.
"""

import random
from typing import List, Optional

# --- Components ---
A = "A"  # Component A
B = "B"  # Component B
C = "C"  # Finished product

class ConveyorBelt:
    """Represents the conveyor belt that transports components."""

    def __init__(self, length: int) -> None:
        """
        Initializes the ConveyorBelt.

        Args:
            length (int): The number of slots on the conveyor belt.
        """
        self.length: int = length  # The total number of slots on the belt
        self.slots: List[Optional[str]] = [None] * length  # The list of slots, initially empty
        self.missed_a: int = 0  # Counter for 'A' components that fall off
        self.missed_b: int = 0  # Counter for 'B' components that fall off

    def step(self) -> Optional[str]:
        """
        Moves the belt forward one step.

        The last item is removed and returned. The first slot becomes empty.
        This method also handles counting missed components ('A' or 'B') and
        removing finished products ('C') for free.

        Returns:
            str or None: The component that fell off the end of the belt, or None.
        """
        # Get the item from the last slot before it falls off.
        last_item = self.slots[-1]

        # If the item is a component, increment the appropriate missed counter.
        # If it's a finished product 'C', it's removed for free and not counted.
        if last_item == A:
            self.missed_a += 1
        elif last_item == B:
            self.missed_b += 1
        elif last_item == C:
            # 'C' is removed for free, so we don't count it as missed.
            pass

        # Shift all items on the belt one position to the right.
        self.slots = [None] + self.slots[:-1]

        return last_item if last_item != C else None

    def step_with_random_item(self) -> Optional[str]:
        """
        Moves the belt forward one step and adds a new random component (or nothing)
        to the first slot.

        This simulates the arrival of new materials at the start of the belt.

        Returns:
            str or None: The component that fell off the end of the belt, or None.
        """
        last_item = self.step()
        
        # Add a new random item to the newly emptied first slot.
        # There is a 1/3 chance for A, 1/3 for B, and 1/3 for an empty slot.
        rand_val = random.random()
        if rand_val < 1/3:
            self.slots[0] = A
        elif rand_val < 2/3:
            self.slots[0] = B
        else:
            self.slots[0] = None

        return last_item

    def push_item(self, item: str) -> None:
        """
        Places a given item onto the first slot of the belt.

        This is used by workers to place finished products.

        Args:
            item (str): The component to place on the belt (e.g., 'C').
        """
        self.slots[0] = item

    def is_empty(self) -> bool:
        """
        Checks if the conveyor belt is completely empty.

        Returns:
            bool: True if all slots are None, False otherwise.
        """
        return all(slot is None for slot in self.slots)

    def __repr__(self) -> str:
        """
        Provides a string representation of the belt's current state.

        Returns:
            str: A string showing the contents of the belt's slots.
        """
        return str(self.slots)
