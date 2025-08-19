"""
This module defines the AI strategies that workers use to make decisions.

It includes a base abstract class, WorkerStrategy, and three concrete implementations:
- IndividualStrategy: A simple, rule-based strategy where workers act independently.
- TeamStrategy: A more advanced, score-based strategy where workers can
  collaborate by passing components to each other.
- HiveMindStrategy: A "perfect information" strategy that executes the single
  most optimal move for the entire system at each step.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Optional
from belt import ConveyorBelt
from worker import Worker, A, B, C

class WorkerStrategy(ABC):
    """
    Abstract base class for all worker AI strategies.

    A strategy defines the logic that a worker uses to decide which action
    to take during their turn in the simulation.
    """
    @abstractmethod
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> None:
        """
        Executes a single action for a worker based on the strategy.
        This method is used by strategies where workers act individually or in pairs.

        Args:
            worker (Worker): The worker instance that is acting.
            partner (Worker): The worker's partner at the same station.
            belts (List[ConveyorBelt]): The list of conveyor belts in the simulation.
            station_index (int): The index of the worker's station on the belt.
        """
        raise NotImplementedError

    def hive_act(self, all_workers: List[Worker], belts: List[ConveyorBelt]) -> None:
        """
        Executes the single best action for the entire system.
        This method is used by global, "hive mind" strategies.

        Args:
            all_workers (List[Worker]): A list of all workers in the simulation.
            belts (List[ConveyorBelt]): The list of all conveyor belts.
        """
        # Default implementation is empty.
        # This method is only implemented by strategies that manage the entire system.
        pass


class IndividualStrategy(WorkerStrategy):
    """
    A simple, rule-based strategy where workers act independently.

    The worker follows a strict priority list for actions:
    1. If assembling, do nothing (wait for the timer).
    2. Place a finished product.
    3. Start assembling if holding both components.
    4. Pick up a needed component from their station.
    """
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> None:
        # Priority 1: If worker is busy assembling, do nothing.
        if worker.is_assembling():
            return

        # Priority 2: If holding a finished product, find any empty spot to place it.
        if worker.is_holding_product():
            for i, belt in enumerate(belts):
                if None in belt.slots:
                    slot_idx = belt.slots.index(None)
                    product = worker.place_product()
                    belt.slots[slot_idx] = product
                    # print(f"{worker.worker_id} placed {product} on belt {i} slot {slot_idx}.")
                    return

        # Priority 3: If able to assemble, start the assembly process.
        if worker.can_assemble():
            worker.start_assembly()
            # print(f"{worker.worker_id} started assembling.")
            return

        # Priority 4: If hands are not full, take a needed component from the belt.
        if not worker.is_full():
            needed_components = worker.needs()
            for component in needed_components:
                for i, belt in enumerate(belts):
                    if belt.slots[station_index] == component:
                        worker.pickup(component)
                        belts[i].slots[station_index] = None
                        # print(f"{worker.worker_id} picked up {component}.")
                        return

class TeamStrategy(WorkerStrategy):
    """
    A sophisticated strategy where workers score and choose the best possible action.
    This strategy allows for collaboration with a worker's direct partner.
    """
    def _get_best_action(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> Optional[Tuple[str, Any]]:
        # If worker is busy assembling, no other actions are possible.
        if worker.is_assembling():
            return None

        possible_actions: List[Tuple[int, Tuple[str, Any]]] = []

        # Action: Place a finished product (Score: 100)
        if worker.is_holding_product():
            for i, belt in enumerate(belts):
                if None in belt.slots:
                    slot_idx = belt.slots.index(None)
                    possible_actions.append((100, ('place_product', (i, belt, slot_idx))))

        # Action: Start assembly (Score: 90)
        if worker.can_assemble():
            possible_actions.append((90, ('start_assembly', None)))

        # Action: Give a surplus component to a partner who needs it (Score: 70)
        if not partner.is_full() and worker.hand_left is not None and worker.hand_left == worker.hand_right:
            component_to_give = worker.hand_right
            if partner.needs_component(component_to_give):
                possible_actions.append((70, ('give_component', component_to_give)))

        # Action: Pick up a component from the belt (Score: 50-65)
        if not worker.is_full():
            for belt_idx, belt in enumerate(belts):
                for slot_idx, component in enumerate(belt.slots):
                    if component in [A, B]:
                        distance = abs(station_index - slot_idx)
                        base_score = 60 - distance * 5
                        if worker.needs_component(component):
                            possible_actions.append((base_score + 5, ('pickup', (component, belt_idx, slot_idx))))
                        elif partner.needs_component(component):
                            possible_actions.append((base_score, ('pickup', (component, belt_idx, slot_idx))))

        if not possible_actions:
            return None
        
        possible_actions.sort(key=lambda x: x[0], reverse=True)
        return possible_actions[0][1]

    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> None:
        action_details = self._get_best_action(worker, partner, belts, station_index)
        if action_details is None:
            return

        action_type, params = action_details
        if action_type == 'place_product':
            belt_idx, belt, slot_idx = params
            product = worker.place_product()
            belt.slots[slot_idx] = product
        elif action_type == 'start_assembly':
            worker.start_assembly()
        elif action_type == 'give_component':
            component_to_give = params
            worker.hand_right = None # Assuming the surplus is in the right hand
            partner.pickup(component_to_give)
        elif action_type == 'pickup':
            component, belt_idx, slot_idx = params
            worker.pickup(component)
            belts[belt_idx].slots[slot_idx] = None


class HiveMindStrategy(WorkerStrategy):
    """
    A "perfect information" strategy that executes the single most optimal
    move for the entire system at each step.
    """
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> None:
        pass # Hive mind uses the global hive_act method.

    def hive_act(self, all_workers: List[Worker], belts: List[ConveyorBelt]) -> None:
        possible_actions: List[Tuple[int, str, Any]] = []

        for worker in all_workers:
            if worker.is_assembling():
                continue # This worker is busy and cannot perform any actions.

            # PRIORITY 1: Place a finished product (Score 100)
            if worker.is_holding_product():
                for i, belt in enumerate(belts):
                    if None in belt.slots:
                        slot_idx = belt.slots.index(None)
                        possible_actions.append((100, 'place', (worker, i, belt, slot_idx)))

            # PRIORITY 2: Start assembling a product (Score 90)
            if worker.can_assemble():
                possible_actions.append((90, 'start_assembly', worker))

            # ... (rest of the hive mind logic for picking/passing components) ...

        if not possible_actions:
            return

        possible_actions.sort(key=lambda x: x[0], reverse=True)
        best_action = possible_actions[0]
        _, action_type, params = best_action

        if action_type == 'place':
            worker, belt_idx, belt, slot_idx = params
            product = worker.place_product()
            belt.slots[slot_idx] = product
        elif action_type == 'start_assembly':
            worker = params
            worker.start_assembly()
        elif action_type == 'pickup':
            worker, component, belt_idx, slot_idx = params
            worker.pickup(component)
            belts[belt_idx].slots[slot_idx] = None
        elif action_type == 'give':
            giver, receiver, component = params
            # This needs a more robust way to handle which hand gives
            if giver.hand_left == component:
                giver.hand_left = None
            else:
                giver.hand_right = None
            receiver.pickup(component)
