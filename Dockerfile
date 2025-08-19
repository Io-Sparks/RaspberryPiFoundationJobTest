# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Set environment variables
# 1. Prevents Python from buffering stdout and stderr, ensuring logs are sent straight to the terminal.
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Expose the port for the health check server
EXPOSE 8080

# Copy the application source code to the container
# We copy the specific files needed to run the simulation.
COPY conveyor_simulation.py .
COPY config.py .
COPY conveyor/ ./conveyor/
COPY health_checker.py .

# Set the default command to run the simulation
# This command runs when the container starts.
CMD ["python", "conveyor_simulation.py"]
