
from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from strategies import WorkerStrategy
    from belt import ConveyorBelt

A = "A"
B = "B"
C = "C"  # Finished Product

class Worker:
    def __init__(self, worker_id: str, strategy: WorkerStrategy, assembly_time: int = 4):
        self.worker_id = worker_id
        self.strategy = strategy
        self.assembly_time = assembly_time
        self.hand_left = None
        self.hand_right = None
        self.assembling_time_left = 0
        self.products_made = 0

    def act(self, partner: Worker, belt: ConveyorBelt, station_index: int):
        """Delegates the action choice entirely to the strategy."""
        self.strategy.act(self, partner, belt, station_index)

    def needs_component(self, component: str) -> bool:
        """
        Checks if the worker needs a specific component to start or continue assembly.
        A worker needs a component if they have an empty hand, or if they have
        one component and the specified one is the missing counterpart.
        """
        if self.is_full() or self.is_assembling():
            return False

        # If both hands are empty, they need either A or B.
        if self.hand_left is None and self.hand_right is None:
            return component in [A, B]

        # If one hand is empty, they need the other component.
        held_component = self.hand_left or self.hand_right
        if held_component == A and component == B:
            return True
        if held_component == B and component == A:
            return True
            
        return False

    def needs(self) -> List[str]:
        """Returns a list of components the worker needs to start assembly."""
        if self.is_full() or self.is_assembling():
            return []
        
        held_components = {self.hand_left, self.hand_right} - {None}
        all_components = {A, B}
        needed = list(all_components - held_components)
        return needed

    def is_empty(self) -> bool:
        """Checks if both hands are empty."""
        return self.hand_left is None and self.hand_right is None

    def is_full(self) -> bool:
        """Checks if both hands are holding components."""
        return self.hand_left is not None and self.hand_right is not None

    def is_holding(self, component: str) -> bool:
        """Checks if the worker is holding a specific component."""
        return self.hand_left == component or self.hand_right == component

    def is_holding_one_component(self) -> bool:
        """Checks if the worker is holding exactly one component."""
        return (self.hand_left is not None) != (self.hand_right is not None)

    def can_assemble(self) -> bool:
        """Checks if the worker has both components and is not already assembling."""
        return {self.hand_left, self.hand_right} == {A, B} and not self.is_assembling()

    def start_assembly(self):
        """Begins the assembly process."""
        if self.can_assemble():
            self.assembling_time_left = self.assembly_time

    def is_assembling(self) -> bool:
        """Checks if the worker is currently assembling a product."""
        return self.assembling_time_left > 0

    def step_assembly(self):
        """Advances the assembly process by one step."""
        if self.is_assembling():
            self.assembling_time_left -= 1
            if self.assembling_time_left == 0:
                # Assembly finished, product appears, components are consumed.
                self.hand_left = C
                self.hand_right = None
                self.products_made += 1

    def pickup(self, item: str):
        """Picks up an item, placing it in an empty hand."""
        if self.hand_left is None:
            self.hand_left = item
        elif self.hand_right is None:
            self.hand_right = item
        else:
            raise Exception("Both hands are full")

    def receive_item(self, item: str):
        """Receives an item from a partner, placing it in an empty hand."""
        self.pickup(item) # Same logic as pickup

    def is_holding_product(self) -> bool:
        """Checks if the worker is holding a finished product."""
        return self.hand_left == C or self.hand_right == C

    def place_product(self) -> str | None:
        """Places the finished product, clearing the hand that held it."""
        if self.is_holding_product():
            if self.hand_left == C:
                self.hand_left = None
            else:
                self.hand_right = None
            return C
        return None

    def __repr__(self):
        return f"Worker {self.worker_id} (L: {self.hand_left}, R: {self.hand_right}, T: {self.assembling_time_left})"
