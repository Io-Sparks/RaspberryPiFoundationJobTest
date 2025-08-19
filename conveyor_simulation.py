import threading
import time
import logging

from config import (
    BELT_CAPACITY,
    NUM_PRODUCERS,
    NUM_CONSUMERS,
)
from conveyor import ConveyorBelt, Producer, Consumer
from health_checker import HealthState, HealthChecker


def setup_simulation(belt_capacity: int, num_producers: int, num_consumers: int):
    """
    Sets up the simulation components, starts the threads, and returns them.
    """
    belt = ConveyorBelt(belt_capacity)

    producers = [Producer(belt, i) for i in range(num_producers)]
    consumers = [Consumer(belt, i) for i in range(num_consumers)]

    threads = producers + consumers
    for thread in threads:
        thread.start()

    return {
        "belt": belt,
        "producers": producers,
        "consumers": consumers,
        "threads": threads,
    }


def main():
    """Sets up and runs the simulation using settings from config and includes health checks."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting Conveyor Belt Simulation with Health Checks...")

    # 1. Initialize and start the Health Checker
    health_state = HealthState()
    health_checker = HealthChecker(health_state)
    health_checker.start()
    logging.info(f"Health check server running on port {health_checker.port}")

    logging.info(
        f"Configuration: Belt Capacity={BELT_CAPACITY}, "
        f"Producers={NUM_PRODUCERS}, Consumers={NUM_CONSUMERS}"
    )
    logging.info("---------------------------------------------------------")

    # 2. Set up the simulation components and threads
    sim = setup_simulation(
        belt_capacity=BELT_CAPACITY,
        num_producers=NUM_PRODUCERS,
        num_consumers=NUM_CONSUMERS,
    )

    # 3. Signal that the application is ready to serve traffic
    health_state.set_ready()
    logging.info("Application is ready. Readiness probe will now succeed.")

    # 4. Main application loop with heartbeat
    logging.info("Simulation running indefinitely. Press Ctrl+C to exit.")

    try:
        while True:
            health_state.record_heartbeat()
            # The liveness probe will now succeed for the next 30 seconds.
            time.sleep(5)  # Send a heartbeat every 5 seconds
    except KeyboardInterrupt:
        logging.info("Shutdown signal received (Ctrl+C).")
    finally:
        logging.info("Stopping all threads gracefully...")

        # 5. Stop all threads
        for thread in sim["producers"] + sim["consumers"]:
            thread.stop()

        for thread in sim["threads"]:
            thread.join()

        logging.info("All threads have been stopped.")

        # 6. Collect and log final results
        total_produced = sum(p.items_produced for p in sim["producers"])
        total_consumed = sum(c.items_consumed for c in sim["consumers"])
        items_remaining = len(sim["belt"])

        logging.info("---------------------------------------------------------")
        logging.info("Simulation finished.")
        logging.info(f"Total items produced: {total_produced}")
        logging.info(f"Total items consumed: {total_consumed}")
        logging.info(f"Items remaining on belt: {items_remaining}")


if __name__ == "__main__":
    main()
