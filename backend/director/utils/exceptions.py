"""This module contains the exceptions used in the director package."""


class DirectorException(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, message: str = "An error occurred.", **kwargs) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)


class AgentException(DirectorException):
    """Exception raised for errors in the agent."""

    def __init__(self, message: str = "An error occurred in the agent", **kwargs) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)


class ToolException(DirectorException):
    """Exception raised for errors in the tool."""

    def __init__(self, message: str = "An error occurred in the tool", **kwargs) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)
