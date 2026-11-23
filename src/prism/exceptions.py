"""
Exceptions for Project PRISM Python SDK.
"""

class PrismError(Exception):
    """Base exception for all Project PRISM errors."""
    pass

class APIConnectionError(PrismError):
    """Raised when communication with the PRISM API fails."""
    pass

class EvaluationError(PrismError):
    """Raised when an expression or quantum circuit evaluation fails."""
    def __init__(self, message: str, raw_response: dict = None):
        super().__init__(message)
        self.raw_response = raw_response or {}

class QasmParseError(EvaluationError):
    """Raised when an OpenQASM circuit fails parsing."""
    pass
