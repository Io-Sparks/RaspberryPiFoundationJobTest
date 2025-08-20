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
            belts (List[List[ConveyorBelt]]): The list of all conveyor belts.
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

        # Priority 2: If holding a finished product, find an empty spot to place it.
        if worker.is_holding_product():
            # Place on the belt at the current station if possible
            if belts[0].slots[station_index] is None:
                product = worker.place_product()
                belts[0].slots[station_index] = product
                return

        # Priority 3: If able to assemble, start the assembly process.
        if worker.can_assemble():
            worker.start_assembly()
            return

        # Priority 4: If hands are not full, take a needed component from the belt.
        if not worker.is_full():
            needed_components = worker.needs()
            component_on_belt = belts[0].slots[station_index]
            if component_on_belt in needed_components:
                worker.pickup(component_on_belt)
                belts[0].slots[station_index] = None
                return

class TeamStrategy(WorkerStrategy):
    """
    A sophisticated strategy where workers score and choose the best possible action.
    This strategy allows for collaboration with a worker's direct partner.
    """
    def _get_best_action(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> Optional[Tuple[str, Any]]:
        if worker.is_assembling():
            return None

        possible_actions: List[Tuple[int, Tuple[str, Any]]] = []

        # Action: Place a finished product (Score: 100)
        if worker.is_holding_product() and belts[0].slots[station_index] is None:
            possible_actions.append((100, ('place_product', None)))

        # Action: Start assembly (Score: 90)
        if worker.can_assemble():
            possible_actions.append((90, ('start_assembly', None)))

        # Action: Pass a component to a partner who can use it to assemble (Score: 80)
        component_to_pass = None
        if worker.is_holding(A) and not worker.is_holding(B) and partner.is_holding(B) and not partner.is_full():
            component_to_pass = A
        elif worker.is_holding(B) and not worker.is_holding(A) and partner.is_holding(A) and not partner.is_full():
            component_to_pass = B
        
        if component_to_pass:
            possible_actions.append((80, ('give_component', component_to_pass)))

        # Action: Pick up a needed component from the belt (Score: 70)
        if not worker.is_full():
            component_on_belt = belts[0].slots[station_index]
            if component_on_belt in worker.needs():
                possible_actions.append((70, ('pickup', component_on_belt)))

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
            product = worker.place_product()
            belts[0].slots[station_index] = product
        elif action_type == 'start_assembly':
            worker.start_assembly()
        elif action_type == 'give_component':
            component_to_give = params
            # Correctly remove the component from the giving worker's hand
            if worker.hand_left == component_to_give:
                worker.hand_left = None
            elif worker.hand_right == component_to_give:
                worker.hand_right = None
            partner.pickup(component_to_give)
        elif action_type == 'pickup':
            component = params
            worker.pickup(component)
            belts[0].slots[station_index] = None


class HiveMindStrategy(WorkerStrategy):
    """
    A "perfect information" strategy that executes the single most optimal
    move for the entire system at each step.
    """
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> None:
        pass # Hive mind uses the global hive_act method.

    def hive_act(self, all_workers: List[Worker], belts: List[ConveyorBelt]) -> None:
        possible_actions: List[Tuple[int, str, Any]] = []
        belt = belts[0] # Assuming one belt for now

        for i, worker in enumerate(all_workers):
            station_index = i // 2
            if worker.is_assembling():
                continue

            # PRIORITY 1: Place a finished product (Score 100)
            if worker.is_holding_product() and belt.slots[station_index] is None:
                possible_actions.append((100, 'place', (i, station_index)))

            # PRIORITY 2: Start assembling a product (Score 90)
            if worker.can_assemble():
                possible_actions.append((90, 'start_assembly', i))

            # PRIORITY 3: Take a final component to assemble (Score 70)
            if not worker.is_full() and worker.is_holding_one_component():
                component_on_belt = belt.slots[station_index]
                if component_on_belt in worker.needs():
                    possible_actions.append((70, 'pickup', (i, component_on_belt, station_index)))
            
            # PRIORITY 4: Take any component if hands are empty (Score 60)
            if worker.is_empty():
                component_on_belt = belt.slots[station_index]
                if component_on_belt in [A, B]:
                    possible_actions.append((60, 'pickup', (i, component_on_belt, station_index)))

        if not possible_actions:
            return

        possible_actions.sort(key=lambda x: x[0], reverse=True)
        best_action = possible_actions[0]
        _, action_type, params = best_action

        if action_type == 'place':
            worker_index, station_index = params
            worker = all_workers[worker_index]
            product = worker.place_product()
            belt.slots[station_index] = product
        elif action_type == 'start_assembly':
            worker_index = params
            worker = all_workers[worker_index]
            worker.start_assembly()
        elif action_type == 'pickup':
            worker_index, component, station_index = params
            worker = all_workers[worker_index]
            worker.pickup(component)
            belt.slots[station_index] = None
