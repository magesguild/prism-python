"""
Project PRISM — Official Python SDK
Mage's Guild Psychonautics LLC (https://www.magesguild.io)

Ultra-lightweight, zero-dependency client for the Project PRISM Mathematical Engine
and Quantum Qudit Runtime.
"""

from .client import PrismClient
from .exceptions import APIConnectionError, EvaluationError, PrismError, QasmParseError
from .types import ChemistryResult, EvaluationResult, QasmResult

__version__ = "0.1.0"
__all__ = [
    "PrismClient",
    "Client",
    "eval",
    "eval_float",
    "qasm",
    "chemistry",
    "PrismError",
    "EvaluationError",
    "QasmParseError",
    "APIConnectionError",
    "EvaluationResult",
    "QasmResult",
    "ChemistryResult",
]

Client = PrismClient

# Module-level default client for zero-boilerplate usage
_default_client = PrismClient()


def eval(expr: str, session_id: str = "default") -> EvaluationResult:
    """Evaluate an expression using the default Project PRISM client."""
    return _default_client.eval(expr, session_id)


def eval_float(expr: str, session_id: str = "default") -> float:
    """Evaluate an expression and return a float using the default Project PRISM client."""
    return _default_client.eval_float(expr, session_id)


def qasm(
    qasm_code: str,
    mode: str = "probabilities",
    shots: int = 1024,
    max_qudits: int = 75,
) -> QasmResult:
    """Execute an OpenQASM circuit using the default Project PRISM client."""
    return _default_client.qasm(qasm_code, mode=mode, shots=shots, max_qudits=max_qudits)


def chemistry(
    num_qubits: int,
    terms: list,
    mode: str = "ground_state",
) -> ChemistryResult:
    """Evaluate a molecular Pauli Hamiltonian using the default Project PRISM client."""
    return _default_client.chemistry(num_qubits, terms, mode=mode)
