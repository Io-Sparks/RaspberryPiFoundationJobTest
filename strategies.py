
from typing import List
from belt import ConveyorBelt
from worker import Worker, A, B, C

class WorkerStrategy:
    """Base class for worker AI strategies."""
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
    """A placeholder for a strategy where workers coordinate their actions."""
    def act(self, worker: Worker, partner: Worker, belts: List[ConveyorBelt], station_index: int):
        # This is where the new team logic will go.
        # For now, we will just print a message and do nothing.
        print(f"TeamStrategy for {worker.worker_id} at station {station_index} - (Not implemented)")
        pass
