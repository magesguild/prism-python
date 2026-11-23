"""
Data types and result models for Project PRISM Python SDK.
"""

from typing import Optional, Dict, Any


class EvaluationResult:
    """Represents the outcome of an expression evaluated by Project PRISM."""

    def __init__(self, raw: str, latency_us: float, status: str = "ok"):
        self.raw = raw
        self.result = raw
        self.latency_us = latency_us
        self.status = status

    def to_float(self) -> float:
        """Parses the result string as a float."""
        try:
            return float(self.result)
        except ValueError as e:
            raise ValueError(f"Cannot parse PRISM result '{self.result}' as float: {e}")

    def to_int(self) -> int:
        """Parses the result string as an integer."""
        try:
            return int(round(float(self.result)))
        except ValueError as e:
            raise ValueError(f"Cannot parse PRISM result '{self.result}' as int: {e}")

    def __repr__(self) -> str:
        return f"<EvaluationResult status={self.status} latency={self.latency_us:.2f}µs result={self.result!r}>"

    def __str__(self) -> str:
        return self.result


class QasmResult:
    """Represents the execution result of an OpenQASM quantum circuit."""

    def __init__(
        self,
        num_qubits: int,
        gate_count: int,
        mode: str,
        result: Optional[str],
        counts: Optional[Dict[str, int]],
        latency_us: float,
        status: str = "ok",
    ):
        self.num_qubits = num_qubits
        self.gate_count = gate_count
        self.mode = mode
        self.result = result
        self.counts = counts or {}
        self.latency_us = latency_us
        self.status = status

    def statevector_str(self) -> Optional[str]:
        """Returns the Dirac ket representation of the output quantum state."""
        return self.result

    def __repr__(self) -> str:
        return (
            f"<QasmResult qubits={self.num_qubits} gates={self.gate_count} "
            f"latency={self.latency_us:.2f}µs>"
        )

    def __str__(self) -> str:
        if self.result:
            return self.result
        if self.counts:
            return str(self.counts)
        return f"QasmResult(qubits={self.num_qubits}, gates={self.gate_count})"


class ChemistryResult:
    """Represents the ground state solution of an electronic molecular Hamiltonian."""

    def __init__(
        self,
        num_qubits: int,
        terms_count: int,
        ground_state_energy: Optional[float],
        optimal_bitstring: Optional[str],
        latency_us: float,
        status: str = "ok",
    ):
        self.num_qubits = num_qubits
        self.terms_count = terms_count
        self.ground_state_energy = ground_state_energy
        self.energy = ground_state_energy
        self.optimal_bitstring = optimal_bitstring
        self.bitstring = optimal_bitstring
        self.latency_us = latency_us
        self.status = status

    def __repr__(self) -> str:
        return (
            f"<ChemistryResult qubits={self.num_qubits} terms={self.terms_count} "
            f"energy={self.ground_state_energy} latency={self.latency_us:.2f}µs>"
        )

    def __str__(self) -> str:
        return f"Energy: {self.ground_state_energy} (state: |{self.optimal_bitstring}>)"
