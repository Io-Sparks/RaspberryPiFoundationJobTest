# Assumptions and Constraints

This document outlines the key assumptions and constraints that define the rules of the factory simulation. These rules govern the behavior of the components, the workers, and the environment itself.

## Simulation Environment

*   **Discrete Time**: The simulation proceeds in discrete time steps. All actions and events occur within these steps.
*   **Single Conveyor Belt**: There is only one conveyor belt in the factory.
*   **Worker Placement**: Workers are always placed in pairs. Each pair is assigned to a single station along the conveyor belt, starting from slot 0.
*   **Worker Capacity**: The total number of workers (`num_worker_pairs * 2`) cannot exceed the total number of slots on the conveyor belt.

## Conveyor Belt Mechanics

*   **Constant Speed**: The belt moves forward exactly one position at every time step.
*   **Component Generation**: At every time step, a new component—chosen randomly between 'A' and 'B'—is placed at the beginning of the belt (slot 0).
*   **Component Loss**: Any component that reaches the end of the belt without being picked up falls off and is counted as a "missed" component.

## Worker Behavior

*   **Two Hands**: Each worker has two hands and can hold a maximum of two items (one per hand).
*   **Assembly Process**: 
    *   A worker must be holding one 'A' and one 'B' to begin assembly.
    *   The assembly process takes a fixed duration of **4 time steps**.
    *   A worker cannot perform any other actions (like picking up or passing items) while they are assembling a product.
*   **Product Creation**: Once the 4-step assembly is complete, the 'A' and 'B' components are consumed, and a finished product 'C' is created in the worker's hands.
*   **Strategy-Driven**: A worker's actions are determined entirely by their assigned AI strategy (`IndividualStrategy` or `TeamStrategy`). They have no independent decision-making ability.

## Strategy Constraints

*   **Individual Strategy**: This is a simple, rule-based strategy. Workers act purely on their own, without any awareness or collaboration with their partner.
*   **Team Strategy**: This is a more complex, score-based strategy. It allows a worker to collaborate with their direct partner at the same station by passing components. It does not allow for collaboration with workers at other stations.
