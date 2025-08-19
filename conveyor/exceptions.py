"""
Custom exceptions for the conveyor belt simulation.
"""

class ProducerError(Exception):
    """Custom exception for errors raised by a Producer."""
    pass

class ConsumerError(Exception):
    """Custom exception for errors raised by a Consumer."""
    pass
