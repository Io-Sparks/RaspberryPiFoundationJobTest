"""
This module defines the AI strategies that workers use to make decisions.

It includes a base abstract class, WorkerStrategy, and two concrete implementations:
- IndividualStrategy: A simple, rule-based strategy where workers act independently.
- TeamStrategy: A more advanced, score-based strategy where workers can
  collaborate by passing components to each other.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from belt import ConveyorBelt
from worker import Worker, A, B, C

class WorkerStrategy(ABC):
    """
    Abstract base class for all worker AI strategies.

    A strategy defines the logic that a worker uses to decide which action
    to take during their turn in the simulation.
    """
    @abstractmethod
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        """
        Executes a single action for a worker based on the strategy.

        Args:
            worker (Worker): The worker instance that is acting.
            partner (Worker): The worker's partner at the same station.
            belts (List[ConveyorBelt]): The list of conveyor belts in the simulation.
            station_index (int): The index of the worker's station on the belt.
        """
        raise NotImplementedError

class IndividualStrategy(WorkerStrategy):
    """
    A simple, rule-based strategy where workers act independently.

    The worker follows a strict priority list for actions:
    1. Place a finished product.
    2. Continue assembling a product.
    3. Start assembling if holding both components.
    4. Pick up a needed component from their station.
    """
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        """
        Executes a single action for a worker based on a fixed priority list.

        Args:
            worker (Worker): The worker instance that is acting.
            partner (Worker): The worker's partner (unused in this strategy).
            belts (List[ConveyorBelt]): The list of conveyor belts.
            station_index (int): The index of the worker's station.
        """

        # Priority 1: If holding a finished product, place it on any empty belt slot.
        if worker.is_holding_product():
            # Scan all belts and all slots for an empty space.
            for i, belt in enumerate(belts):
                for slot_idx, slot in enumerate(belt.slots):
                    if slot is None:
                        # Place the product and end the turn.
                        product = worker.place_product()
                        belt.slots[slot_idx] = product
                        print(f"{worker.worker_id} placed {product} on belt {i} slot {slot_idx}. Total finished: {worker.products_made + partner.products_made}")
                        return

        # Priority 2: If currently assembling a product, continue the process.
        if worker.is_assembling():
            worker.step_assembly()
            if worker.is_holding_product():
                # Assembly is now complete.
                print(f"{worker.worker_id} finished assembling. Now holding: {worker.hand_left}, {worker.hand_right}.")
            else:
                # Assembly is still in progress.
                total_assembly_time = 4
                progress = total_assembly_time - worker.assembling_time_left
                print(f"{worker.worker_id} is assembling. Progress: {progress}/{total_assembly_time}")
            return

        # Priority 3: If holding both necessary components, start the assembly process.
        if worker.can_assemble():
            worker.start_assembly()
            print(f"{worker.worker_id} started assembling.")
            return

        # Priority 4: If hands are not full, try to pick up a needed component.
        if not worker.is_full():
            # Determine which components the worker still needs.
            needed_components = worker.needs()
            for component in needed_components:
                # Check the worker's station on each belt for the needed component.
                for i, belt in enumerate(belts):
                    if belt.slots[station_index] == component:
                        # Pick up the component and end the turn.
                        worker.pickup(component)
                        belts[i].slots[station_index] = None
                        print(f"{worker.worker_id} picked up {component} from belt {i} slot {station_index}. Holding: {worker.hand_left}, {worker.hand_right}")
                        return

class TeamStrategy(WorkerStrategy):
    """
    A sophisticated strategy where workers score and choose the best possible action.

    This strategy allows for collaboration, such as one worker giving a surplus
    component to their partner if the partner needs it. Actions are scored based
    on their immediate value, and the highest-scoring action is chosen.
    """

    def _get_best_action(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> Tuple[str, Any] | None:
        """
        Analyzes the game state and determines the best action to take.

        This method evaluates all possible actions (placing, assembling, picking up,
        giving to partner) and assigns them a score. The action with the highest
        score is returned.

        Args:
            worker (Worker): The worker considering the action.
            partner (Worker): The worker's partner.
            belts (List[ConveyorBelt]): The list of conveyor belts.
            station_index (int): The index of the worker's station.

        Returns:
            A tuple containing the action type (str) and its parameters, or None.
        """
        possible_actions = []

        # Action 1: Place a finished product (highest priority).
        if worker.is_holding_product():
            for i, belt in enumerate(belts):
                for slot_idx, slot in enumerate(belt.slots):
                    if slot is None:
                        # Score is 100, the highest possible, to ensure this is always chosen.
                        possible_actions.append((100, ('place_product', (i, belt, slot_idx))))

        # Action 2: Continue assembling a product.
        if worker.is_assembling():
            # High priority to finish what's already started.
            possible_actions.append((90, ('step_assembly', None)))

        # Action 3: Start assembling a product.
        if worker.can_assemble():
            # High priority to start combining components.
            possible_actions.append((80, ('start_assembly', None)))

        # Action 4: Give a surplus component to the partner (collaboration).
        # Check if the worker has two of the same component.
        if not partner.is_full() and worker.hand_left is not None and worker.hand_left == worker.hand_right:
            component_to_give = worker.hand_right
            # Check if the partner actually needs this component.
            if partner.needs_component(component_to_give):
                # This is a valuable team play.
                possible_actions.append((70, ('give_component', component_to_give)))

        # Action 5: Pick up components from any belt slot.
        if not worker.is_full():
            for belt_idx, belt in enumerate(belts):
                for slot_idx, component in enumerate(belt.slots):
                    if component in [A, B]:
                        # Base score is higher for items closer to the worker's station.
                        distance = abs(station_index - slot_idx)
                        base_score = 60 - distance * 5

                        # Add a bonus if the worker needs this component for themselves.
                        if worker.needs_component(component):
                            possible_actions.append((base_score + 5, ('pickup', (component, belt_idx, slot_idx))))
                        # Add a smaller bonus if it helps the partner (still a good team play).
                        elif partner.needs_component(component):
                            possible_actions.append((base_score, ('pickup', (component, belt_idx, slot_idx))))

        # If no actions are possible, return None.
        if not possible_actions:
            return None

        # Sort actions by score in descending order to find the best one.
        possible_actions.sort(key=lambda x: x[0], reverse=True)
        
        # Return the details of the highest-scoring action.
        if possible_actions:
            return possible_actions[0][1]
        return None


    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        """
        Determines the best action using a scoring system and executes it.

        Args:
            worker (Worker): The worker instance that is acting.
            partner (Worker): The worker's partner at the same station.
            belts (List[ConveyorBelt]): The list of conveyor belts.
            station_index (int): The index of the worker's station.
        """
        # First, determine the best action based on the current state.
        action_details = self._get_best_action(worker, partner, belts, station_index)

        # If no valid action was found, the worker does nothing this turn.
        if action_details is None:
            return

        # Unpack the action type and its parameters.
        action_type, params = action_details

        # Execute the chosen action.
        if action_type == 'place_product':
            belt_idx, belt, slot_idx = params
            product = worker.place_product()
            belt.slots[slot_idx] = product
            print(f"{worker.worker_id} (team) placed {product} on belt {belt_idx} slot {slot_idx}. Total finished: {worker.products_made + partner.products_made}")

        elif action_type == 'step_assembly':
            worker.step_assembly()
            if worker.is_holding_product():
                print(f"{worker.worker_id} (team) finished assembling. Now holding: {worker.hand_left}, {worker.hand_right}.")
            else:
                total_assembly_time = 4
                progress = total_assembly_time - worker.assembling_time_left
                print(f"{worker.worker_id} (team) is assembling. Progress: {progress}/{total_assembly_time}")

        elif action_type == 'start_assembly':
            worker.start_assembly()
            print(f"{worker.worker_id} (team) started assembling.")

        elif action_type == 'give_component':
            component_to_give = params
            # Give the component from the surplus hand (right hand).
            worker.hand_right = None
            partner.pickup(component_to_give)
            print(f"{worker.worker_id} (team) gave surplus {component_to_give} to {partner.worker_id}.")

        elif action_type == 'pickup':
            component, belt_idx, slot_idx = params
            worker.pickup(component)
            # Remove the component from the belt.
            belts[belt_idx].slots[slot_idx] = None
            print(f"{worker.worker_id} (team) picked up {component} from belt {belt_idx} slot {slot_idx}. Holding: {worker.hand_left}, {worker.hand_right}")
