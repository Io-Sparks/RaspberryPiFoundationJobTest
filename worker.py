from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from strategies import WorkerStrategy
    from belt import ConveyorBelt

A = "A"
B = "B"
C = "C"  # Finished Product

class Worker:
    ASSEMBLY_TIME = 4

    def __init__(self, worker_id: str, strategy: WorkerStrategy):
        self.worker_id = worker_id
        self.strategy = strategy
        self.hand_left = None
        self.hand_right = None
        self.assembling_time_left = 0
        self.products_made = 0

    def act(self, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        """Delegates the action choice entirely to the strategy."""
        self.strategy.act(self, partner, belts, station_index)

    def needs(self) -> List[str]:
        """Returns a list of components the worker needs to start assembly."""
        if self.is_full() or self.is_assembling():
            return []
        
        held_components = {self.hand_left, self.hand_right} - {None}
        all_components = {A, B}
        needed = list(all_components - held_components)
        return needed

    def is_full(self) -> bool:
        """Checks if both hands are holding components."""
        return self.hand_left is not None and self.hand_right is not None

    def can_assemble(self) -> bool:
        """Checks if the worker has both components and is not already assembling."""
        return self.is_full() and not self.is_assembling()

    def start_assembly(self):
        """Begins the assembly process."""
        if self.can_assemble():
            self.assembling_time_left = self.ASSEMBLY_TIME

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
