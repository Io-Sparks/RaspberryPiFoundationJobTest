from typing import List
from belt import ConveyorBelt
from worker import Worker

def format_belt_and_workers(belt: ConveyorBelt, workers: List[Worker], num_worker_pairs: int, belt_length: int) -> List[str]:
    """
    Formats the current state of the belt and workers into a list of strings for display.
    """
    output_lines = []
    output_lines.append("") # Add a newline for spacing from the action commentary

    top_lines = [""] * 4
    belt_line = "Belt:  "
    bottom_lines = [""] * 4
    blank_line = ""

    station_width = 28  # Width for each station's visual block

    for i in range(belt_length):
        # --- Top Worker ---
        if i < num_worker_pairs:
            worker = workers[2 * i]
            w_id = f"Worker: {worker.worker_id + 1}"
            w_lh = f"LeftHand: {worker.hand_left or '_'}"
            w_rh = f"RightHand: {worker.hand_right or '_'}"
            w_at = f"AssemblyTimer: ({worker.assembling_time_left})"
            
            top_lines[0] += f"| {w_id:<{station_width-2}} "
            top_lines[1] += f"| {w_lh:<{station_width-2}} "
            top_lines[2] += f"| {w_rh:<{station_width-2}} "
            top_lines[3] += f"| {w_at:<{station_width-2}} "
            blank_line += f"| {' ':<{station_width-2}} "
        else:
            # Add empty space for stations without workers
            for j in range(4):
                top_lines[j] += " " * (station_width + 1)
            blank_line += " " * (station_width + 1)

        # --- Belt ---
        item = belt.slots[i]
        belt_item_str = f"[{str(item or ' '):^5}]" # e.g., "[  A  ]"
        belt_line += f"| {belt_item_str:^{station_width-2}} "

        # --- Bottom Worker ---
        if i < num_worker_pairs:
            worker = workers[2 * i + 1]
            w_id = f"Worker: {worker.worker_id + 1}"
            w_lh = f"LeftHand: {worker.hand_left or '_'}"
            w_rh = f"RightHand: {worker.hand_right or '_'}"
            w_at = f"AssemblyTimer: ({worker.assembling_time_left})"

            bottom_lines[0] += f"| {w_id:<{station_width-2}} "
            bottom_lines[1] += f"| {w_lh:<{station_width-2}} "
            bottom_lines[2] += f"| {w_rh:<{station_width-2}} "
            bottom_lines[3] += f"| {w_at:<{station_width-2}} "
        else:
            # Add empty space for stations without workers
            for j in range(4):
                bottom_lines[j] += " " * (station_width + 1)

    # Add all constructed lines to the output
    for line in top_lines:
        output_lines.append(f"       {line}")
    
    output_lines.append(f"       {blank_line}")
    output_lines.append(belt_line)
    output_lines.append(f"       {blank_line}")

    for line in bottom_lines:
        output_lines.append(f"       {line}")
    
    output_lines.append("") # Extra newline at the end for clarity

    return output_lines

def format_simulation_results(finished_products: int, missed_a: int, missed_b: int, held_a: int, held_b: int) -> List[str]:
    """
    Formats the final simulation results into a list of strings for display.
    """
    output_lines = []
    output_lines.append("\n--- Simulation Results ---")
    output_lines.append(f"  - Finished Products: {finished_products}")
    output_lines.append(f"  - Missed A: {missed_a}")
    output_lines.append(f"  - Missed B: {missed_b}")
    output_lines.append(f"  - Held A: {held_a}")
    output_lines.append(f"  - Held B: {held_b}")
    output_lines.append("------------------------\n")
    return output_lines
