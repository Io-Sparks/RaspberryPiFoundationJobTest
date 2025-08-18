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
    *   **Single Responsibility Principle:** This module's only job is to handle configuration, providing a clean interface to the rest of the application.
    *   **Defaults:** It provides sensible default values, making the application easier to run in local development environments where not all variables might be set.

**Decision:** Use the `python-dotenv` library to load a `.env` file for local development convenience.

*   **Reasoning:**
    *   **Developer Experience:** Automates the loading of local configuration, removing the need for developers to manually `export` environment variables in their shell.
    *   **Environment Parity:** Allows local development to mimic the use of environment variables in production without requiring complex setup.
    *   **Safe for Production:** The `load_dotenv()` function fails silently if no `.env` file is found, making it safe to keep in the code for production/CI/CD environments where the file will not and should not exist.