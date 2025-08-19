
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from belt import ConveyorBelt
from worker import Worker, A, B, C

class WorkerStrategy(ABC):
    """Base class for worker AI strategies."""
    @abstractmethod
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        raise NotImplementedError

class IndividualStrategy(WorkerStrategy):
    """A simple strategy where workers act independently."""
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):

        # Priority 1: Place a finished product on an empty slot.
        if worker.is_holding_product():
            for i, belt in enumerate(belts):
                if belt.slots[station_index] is None:
                    product = worker.place_product()
                    belt.slots[station_index] = product
                    print(f"{worker.worker_id} placed {product} on belt {i} slot {station_index}. Total finished: {worker.products_made + partner.products_made}")
                    return

        # Priority 2: Continue assembling if already started.
        if worker.is_assembling():
            worker.step_assembly()
            if worker.is_holding_product():
                print(f"{worker.worker_id} finished assembling. Now holding: {worker.hand_left}, {worker.hand_right}.")
            else:
                total_assembly_time = 4
                progress = total_assembly_time - worker.assembling_time_left
                print(f"{worker.worker_id} is assembling. Progress: {progress}/{total_assembly_time}")
            return

        # Priority 3: If holding both components, start assembling.
        if worker.can_assemble():
            worker.start_assembly()
            print(f"{worker.worker_id} started assembling.")
            return

        # Priority 4: Pick up needed components from any belt.
        if not worker.is_full():
            needed_components = worker.needs()
            for component in needed_components:
                for i, belt in enumerate(belts):
                    if belt.slots[station_index] == component:
                        worker.pickup(component)
                        belts[i].slots[station_index] = None
                        print(f"{worker.worker_id} picked up {component} from belt {i} slot {station_index}. Holding: {worker.hand_left}, {worker.hand_right}")
                        # Action taken, end turn.
                        return

class TeamStrategy(WorkerStrategy):
    """A strategy where workers score and choose the best possible action."""

    def _get_best_action(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int) -> Tuple[str, Any] | None:
        possible_actions = []

        # 1. Score placing a finished product (highest priority)
        if worker.is_holding_product():
            for i, belt in enumerate(belts):
                if belt.slots[station_index] is None:
                    possible_actions.append((100, ('place_product', (i, belt))))

        # 2. Score continuing assembly
        if worker.is_assembling():
            possible_actions.append((90, ('step_assembly', None)))

        # 3. Score starting assembly
        if worker.can_assemble():
            possible_actions.append((80, ('start_assembly', None)))

        # 4. Score giving a surplus component to the partner
        if not partner.is_full() and worker.hand_left is not None and worker.hand_left == worker.hand_right:
            component_to_give = worker.hand_right
            if partner.needs_component(component_to_give):
                possible_actions.append((70, ('give_component', component_to_give)))

        # 5. Score picking up components from belts
        if not worker.is_full():
            for belt_idx, belt in enumerate(belts):
                for slot_idx, component in enumerate(belt.slots):
                    if component in [A, B]:
                        # Score is higher for closer items
                        distance = abs(station_index - slot_idx)
                        base_score = 60 - distance * 5

                        # Add bonus if the worker needs it for themselves
                        if worker.needs_component(component):
                            possible_actions.append((base_score + 5, ('pickup', (component, belt_idx, slot_idx))))
                        # Add smaller bonus if the partner needs it
                        elif partner.needs_component(component):
                            possible_actions.append((base_score, ('pickup', (component, belt_idx, slot_idx))))

        if not possible_actions:
            return None

        # Return the action with the highest score
        possible_actions.sort(key=lambda x: x[0], reverse=True)
        return possible_actions[0][1]

    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        action_details = self._get_best_action(worker, partner, belts, station_index)

        if action_details is None:
            # No action to perform
            return

        action_type, params = action_details

        if action_type == 'place_product':
            belt_idx, belt = params
            product = worker.place_product()
            belt.slots[station_index] = product
            print(f"{worker.worker_id} (team) placed {product} on belt {belt_idx} slot {station_index}. Total finished: {worker.products_made + partner.products_made}")

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
            worker.hand_right = None  # Give from the surplus hand
            partner.pickup(component_to_give)
            print(f"{worker.worker_id} (team) gave surplus {component_to_give} to {partner.worker_id}.")

        elif action_type == 'pickup':
            component, belt_idx, slot_idx = params
            worker.pickup(component)
            belts[belt_idx].slots[slot_idx] = None
            print(f"{worker.worker_id} (team) picked up {component} from belt {belt_idx} slot {slot_idx}. Holding: {worker.hand_left}, {worker.hand_right}")
