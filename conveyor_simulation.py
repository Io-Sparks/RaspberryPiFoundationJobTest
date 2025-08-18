import threading
import time

from config import (
    BELT_CAPACITY,
    NUM_PRODUCERS,
    NUM_CONSUMERS,
    SIMULATION_DURATION_SECONDS,
)
from conveyor import ConveyorBelt, Producer, Consumer

def main():
    """Sets up and runs the simulation."""
    print("Starting Conveyor Belt Simulation...")
    print(
        f"Configuration: Belt Capacity={BELT_CAPACITY}, Producers={NUM_PRODUCERS}, Consumers={NUM_CONSUMERS}")
    print("---------------------------------------------------------")

    # The shared resource
    belt = ConveyorBelt(BELT_CAPACITY)

    # An event to signal all threads to stop gracefully
    stop_event = threading.Event()

    threads = []
    # Create and start producer threads
    for i in range(NUM_PRODUCERS):
        producer = Producer(belt, stop_event, i + 1)
        threads.append(producer)
        producer.start()

    # Create and start consumer threads
    for i in range(NUM_CONSUMERS):
        consumer = Consumer(belt, stop_event, i + 1)
        threads.append(consumer)
        consumer.start()

    # Let the simulation run for the configured duration
    time.sleep(SIMULATION_DURATION_SECONDS)

    # Shutdown the simulation gracefully
    print("---------------------------------------------------------")
    print("Simulation time elapsed. Shutting down all threads...")
    stop_event.set()

    # The semaphores might be blocking, so we need to unblock them
    # to allow threads to check the stop_event and exit.
    for _ in range(NUM_PRODUCERS):
        belt.filled_slots.release()  # Unblock a waiting consumer
    for _ in range(NUM_CONSUMERS):
        belt.empty_slots.release()  # Unblock a waiting producer

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Simulation finished.")


if __name__ == "__main__":
    main()
