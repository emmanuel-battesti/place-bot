"""
Custom exceptions for the robot simulation.
"""


class RobotException(Exception):
    """Base exception for robot-related errors."""
    pass


class DisabledFunctionError(RobotException):
    """
    Exception raised when attempting to use a disabled function.
    
    This is typically used for deprecated methods that should not be called
    directly by the user.
    """
    pass

