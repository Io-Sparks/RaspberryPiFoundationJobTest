import threading
import time

from config import (
    BELT_CAPACITY,
    NUM_PRODUCERS,
    NUM_CONSUMERS,
    SIMULATION_DURATION_SECONDS,
)
from conveyor import ConveyorBelt, Producer, Consumer


def run_simulation(belt_capacity: int, num_producers: int, num_consumers: int, duration: int):
    """
    Runs a single conveyor belt simulation with a given configuration.

    Args:
        belt_capacity: The maximum number of items the belt can hold.
        num_producers: The number of producer threads.
        num_consumers: The number of consumer threads.
        duration: The number of seconds to run the simulation for.

    Returns:
        A dictionary containing the total items produced and consumed.
    """
    belt = ConveyorBelt(belt_capacity)
    stop_event = threading.Event()

    producers = [Producer(belt, stop_event, i) for i in range(num_producers)]
    consumers = [Consumer(belt, stop_event, i) for i in range(num_consumers)]

    threads = producers + consumers

    for thread in threads:
        thread.start()

    time.sleep(duration)

    stop_event.set()

    for thread in threads:
        thread.join()

    total_produced = sum(p.items_produced for p in producers)
    total_consumed = sum(c.items_consumed for c in consumers)

    return {
        "produced": total_produced,
        "consumed": total_consumed,
        "remaining": len(belt),
    }


def main():
    """Sets up and runs the simulation using settings from config."""
    print("Starting Conveyor Belt Simulation...")
    print(
        f"Configuration: Belt Capacity={BELT_CAPACITY}, "
        f"Producers={NUM_PRODUCERS}, Consumers={NUM_CONSUMERS}"
    )
    print("---------------------------------------------------------")

    results = run_simulation(
        belt_capacity=BELT_CAPACITY,
        num_producers=NUM_PRODUCERS,
        num_consumers=NUM_CONSUMERS,
        duration=SIMULATION_DURATION_SECONDS,
    )

    print("---------------------------------------------------------")
    print("Simulation finished.")
    print(f"Total items produced: {results['produced']}")
    print(f"Total items consumed: {results['consumed']}")
    print(f"Items remaining on belt: {results['remaining']}")


if __name__ == "__main__":
    main()
