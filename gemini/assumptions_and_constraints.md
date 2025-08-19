# Assumptions and Constraints

This document outlines the key assumptions and design constraints that have been established through trial and error during the development of the simulation.

## Simulation Logic

1.  **Slot 0 is the Source**: The first slot (index 0) of any conveyor belt is exclusively for generating new components. Workers **must not** place any items in this slot.
2.  **Worker Stations Start at Slot 1**: To enforce the "Slot 0 is the Source" rule, worker stations are assigned starting from slot 1.
3.  **Workers Only Pick Up Raw Materials**: Workers should only pick up components 'A' and 'B'. They must never pick up a finished product ('C').
4.  **Assembly Requires 'A' and 'B'**: A finished product 'C' can only be created by assembling one 'A' and one 'B' component.
5.  **One Action Per Step**: A worker can only perform one significant action per simulation step (e.g., pickup, place, or step assembly).

## Code and Design

1.  **Strategy Pattern**: The worker's decision-making logic is decoupled from its state. All AI/logic must be implemented within a class in `strategies.py`. The `Worker` class itself should remain a simple state machine.
2.  **Teamwork is a Goal**: The current `IndividualStrategy` is a baseline. A `TeamStrategy` where workers can coordinate (e.g., pass items) is a desired future enhancement.
3.  **Correct `needs()` Logic**: The `worker.needs()` method must correctly identify required components regardless of which hand holds what. A worker holding {'A', `None`} needs a 'B'. A worker holding {'B', `None`} needs an 'A'. A worker holding {'A', 'B'} needs nothing.
