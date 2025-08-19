
import random

# --- Components ---
A = "A"
B = "B"
C = "C" # Finished product

class ConveyorBelt:
    def __init__(self, length):
        self.length = length
        self.slots = [None] * length
        self.missed_a = 0
        self.missed_b = 0

    def step(self):
        """
        Moves the belt forward one step and adds a new component.
        Returns the item that fell off the end, if any.
        """
        # Item falling off the end
        last_item = self.slots[-1]
        if last_item == A:
            self.missed_a += 1
        elif last_item == B:
            self.missed_b += 1


        # Move all items one step forward
        self.slots[1:] = self.slots[:-1]

        # Add a new item at the start
        rand_val = random.random()
        if rand_val < 1/3:
            self.slots[0] = A
        elif rand_val < 2/3:
            self.slots[0] = B
        else:
            self.slots[0] = None
        
        return last_item

    def __repr__(self):
        return str(self.slots)
