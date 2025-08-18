# Assumption Log

This document records the assumptions made during the development process. These are important for understanding the context and constraints of the design decisions.

## 2025-08-18: Deployment and Configuration

*   **Assumption:** The target deployment environment is or will 
                    be a Kubernetes cluster.
    *   **Justification:** The request to use environment variables for 
                           CI/CD and the discussion of scalability patterns (sidecars, sharding) strongly point towards a container orchestration system like Kubernetes. Choosing Helm is a direct consequence of this assumption.

*   **Assumption:** The organisation has a CI/CD pipeline capable of 
                    executing Helm commands.

    *   **Justification:** The goal of automated, secure deployments 
                           requires a CI/CD system that can build 
                           container images and run deployment commands 
                           (`helm upgrade --install`).

*   **Assumption:** A container registry is available to store the 
                    application's Docker image.
    *   **Justification:** The Helm chart references a container 
                           image (`image.repository`). This image must 
                           be built and pushed to a registry where the 
                           Kubernetes cluster can pull it from.

  *   **Assumption:** For local development, developers are capable of 
                      managing `.env` files or setting environment 
                      variables manually.
      *   **Justification:** While I was unable to create a `.env` file, 
                             this is a standard developer practice. 
                             We assume developers have the basic knowledge 
                             to set up their local environment based on 
                             our `config.py` implementation.