# Decision Log

This document records the key architectural and design decisions made during the development of the conveyor simulation project.

## 2025-08-18: Helm for Configuration and Deployment

**Decision:** Adopt Helm as the primary tool for packaging, configuring, and deploying the application to Kubernetes.

*   **Reasoning:**
    *   **Standardization:** Helm is the de-facto standard for managing Kubernetes applications.
    *   **Automation:** Enables fully automated and repeatable deployments via CI/CD pipelines.
    *   **Configuration Management:** Allows for templating of Kubernetes manifests and managing environment-specific configurations (e.g., dev, staging, production) from a single, version-controlled source (`values.yaml`).
    *   **Extensibility:** Simplifies the addition of future components like sidecar containers for logging and monitoring, or scaling configurations.

**Decision:** Externalize all application configuration from the Python code into environment variables.

*   **Reasoning:**
    *   **12-Factor App:** Adheres to the principle of separating configuration from code, which is a best practice for building scalable and maintainable applications.
    *   **Portability:** Allows the same application container image to be used across all environments without modification.
    *   **Security:** Prevents hardcoding of sensitive information and allows for secure injection of secrets using Kubernetes-native mechanisms.

**Decision:** Use a `config.py` module to centralize access to environment variables within the application.

*   **Reasoning:**
    *   **Single Responsibility Principle:** This module'''s only job is to handle configuration, providing a clean interface to the rest of the application.
    *   **Defaults:** It provides sensible default values, making the application easier to run in local development environments where not all variables might be set.

**Decision:** Use the `python-dotenv` library to load a `.env` file for local development convenience.

*   **Reasoning:**
    *   **Developer Experience:** Automates the loading of local configuration, removing the need for developers to manually `export` environment variables in their shell.
    *   **Environment Parity:** Allows local development to mimic the use of environment variables in production without requiring complex setup.
    *   **Safe for Production:** The `load_dotenv()` function fails silently if no `.env` file is found, making it safe to keep in the code for production/CI/CD environments where the file will not and should not exist.

## 2025-08-19: Code Structure and Testing

**Decision:** Refactor the core simulation classes (`ConveyorBelt`, `Producer`, `Consumer`) into a dedicated Python package named `conveyor`.

*   **Reasoning:**
    *   **Maintainability:** Follows the Single Responsibility Principle, making the code easier to understand, modify, and debug.
    *   **Testability:** Enables the creation of focused unit tests for each component in isolation.
    *   **Scalability:** Provides the necessary modular foundation for potentially evolving these components into separate, independently scalable services in the future.
    *   **Clarity:** Adopts standard Python project structure and naming conventions (e.g., lowercase module names, CapWords class names).

**Decision:** Implement a comprehensive test suite using the `unittest` framework.

*   **Reasoning:**
    *   **Correctness:** Verifies that each unit of code (e.g., `ConveyorBelt`) behaves as expected in isolation.
    *   **Confidence:** The integration test (`test_concurrency.py`) provides strong assurance that the concurrency model is working correctly under load, preventing race conditions and data loss.
    *   **Regression Prevention:** Protects against future changes accidentally breaking existing functionality.

**Decision:** Implement a thread-safe conveyor belt using a `deque` protected by a `threading.Lock` and coordinated by two `threading.Semaphore` objects.

*   **Reasoning:**
    *   **Thread Safety:** The `Lock` guarantees that only one thread can modify the internal `deque` at a time, preventing data corruption.
    *   **Bounded Buffer:** The `empty_slots` and `filled_slots` semaphores correctly implement the bounded buffer pattern, ensuring producers wait when the belt is full and consumers wait when it is empty. This is a robust and well-understood concurrency pattern.
    *   **Clarity:** While `queue.Queue` provides this out-of-the-box, the explicit use of Locks and Semaphores makes the concurrency control mechanism transparent and easy to understand for developers familiar with threading primitives.

## 2025-08-20: Concurrency Robustness

**Decision:** Modified `ConveyorBelt` methods (`put`, `take`) to use non-blocking, timed waits instead of indefinite blocking.

*   **Reasoning:**
    *   **Deadlock Prevention:** The previous implementation caused threads to hang indefinitely if they tried to access a full or empty belt when the simulation was stopping. This created a deadlock where threads could not check the `stop_event`.
    *   **Graceful Shutdown:** Using a short timeout allows threads to wake up periodically, check the `stop_event`, and terminate gracefully, ensuring that tests and the application can shut down reliably. This makes the entire system more robust and predictable.
