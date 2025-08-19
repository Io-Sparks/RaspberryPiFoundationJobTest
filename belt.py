"""
This module defines the core components of the factory simulation.

It includes the definitions for the components (A, B, C) and the ConveyorBelt
class, which manages the state and movement of items in the simulation.
"""

import random

# --- Components ---
A = "A"  # Component A
B = "B"  # Component B
C = "C"  # Finished product

class ConveyorBelt:
    """Represents the conveyor belt that transports components."""

    def __init__(self, length):
        """
        Initializes the ConveyorBelt.

        Args:
            length (int): The number of slots on the conveyor belt.
        """
        self.length = length  # The total number of slots on the belt
        self.slots = [None] * length  # The list of slots, initially empty
        self.missed_a = 0  # Counter for 'A' components that fall off
        self.missed_b = 0  # Counter for 'B' components that fall off

    def step(self):
        """
        Moves all items on the belt forward by one position.

        The item in the last slot falls off the belt. If it's a component
        (A or B), it's counted as missed. The first slot becomes empty.

        Returns:
            str or None: The component that fell off the end of the belt, or None.
        """
        # Get the item from the last slot before it falls off.
        last_item = self.slots[-1]

        # If the item is a component, increment the appropriate missed counter.
        if last_item == A:
            self.missed_a += 1
        elif last_item == B:
            self.missed_b += 1

        # Shift all items on the belt one position to the right.
        # The last item is discarded, and the first item becomes None.
        self.slots[1:] = self.slots[:-1]
        self.slots[0] = None

        return last_item

    def step_with_random_item(self):
        """
        Moves the belt forward one step and adds a new random component (or nothing)
        to the first slot.

        This simulates the arrival of new materials at the start of the belt.

        Returns:
            str or None: The component that fell off the end of the belt, or None.
        """
        # First, advance the belt and get the item that fell off.
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

    def push_item(self, item):
        """
        Places a given item onto the first slot of the belt.

        This is used by workers to place finished products.

        Args:
            item (str): The component to place on the belt (e.g., 'C').
        """
        self.slots[0] = item

    def is_empty(self):
        """
        Checks if the conveyor belt is completely empty.

        Returns:
            bool: True if all slots are None, False otherwise.
        """
        return all(slot is None for slot in self.slots)

    def __repr__(self):
        """
        Provides a string representation of the belt's current state.

        Returns:
            str: A string showing the contents of the belt's slots.
        """
        return str(self.slots)
