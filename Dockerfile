# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set default environment variables for the simulation
# These can be overridden at runtime (e.g., docker run -e BELT_LENGTH=20 ...)
ENV BELT_LENGTH=14
ENV NUM_WORKER_PAIRS=7
ENV STRATEGY=team
ENV STEPS=100
ENV QUIET=false

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY *.py ./

# Define the command to run the application
CMD ["python", "simulation.py"]
