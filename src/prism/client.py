"""
Project PRISM Client — Official REST API Client
Mage's Guild Psychonautics LLC (https://www.magesguild.io)

Zero external dependencies: uses standard library urllib and json.
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple, Union

from .exceptions import APIConnectionError, EvaluationError, QasmParseError
from .types import ChemistryResult, EvaluationResult, QasmResult

DEFAULT_BASE_URL = os.environ.get("PRISM_BASE_URL", "https://www.magesguild.io")


class PrismClient:
    """
    Client for interacting with the Project PRISM Mathematical Engine REST API.
    
    Example:
        >>> import prism
        >>> client = prism.Client()
        >>> res = client.eval("4 * pi^3 + pi^2 + pi")
        >>> print(res.to_float())
        137.03630377587845
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("PRISM_API_KEY")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "prism-python/0.1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=self._headers())

        t_start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw_body = resp.read().decode("utf-8")
                elapsed_us = (time.perf_counter() - t_start) * 1_000_000.0
                data = json.loads(raw_body)
                if "latency_us" not in data or data["latency_us"] == 0:
                    data["latency_us"] = elapsed_us
                return data
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
                msg = err_json.get("error", err_body)
            except Exception:
                msg = f"HTTP {e.code}: {err_body}"
            raise EvaluationError(msg) from e
        except urllib.error.URLError as e:
            raise APIConnectionError(f"Could not connect to PRISM API at {url}: {e.reason}") from e
        except Exception as e:
            raise APIConnectionError(f"Request failed: {e}") from e

    def eval(self, expr: str, session_id: str = "default") -> EvaluationResult:
        """
        Evaluates a mathematical, matrix, or quantum expression on Project PRISM.

        Args:
            expr: Mathematical expression string, e.g. 'inv([[4, 7], [2, 6]])'
            session_id: Optional session identifier for maintaining state.

        Returns:
            EvaluationResult: Contains the result string and execution latency.
        """
        trimmed = expr.strip()
        if not trimmed:
            raise ValueError("Expression cannot be empty")

        data = self._post("/api/prism/eval", {"expr": trimmed, "session_id": session_id})
        status = data.get("status", "ok")
        if status != "ok" or data.get("error") is not None:
            raise EvaluationError(data.get("error", "Evaluation failed"), raw_response=data)

        return EvaluationResult(
            raw=data.get("result", ""),
            latency_us=float(data.get("latency_us", 0.0)),
            status=status,
        )

    def eval_float(self, expr: str, session_id: str = "default") -> float:
        """Convenience method that evaluates an expression and returns a float."""
        return self.eval(expr, session_id).to_float()

    def qasm(
        self,
        qasm_code: str,
        mode: str = "probabilities",
        shots: int = 1024,
        max_qudits: int = 75,
    ) -> QasmResult:
        """
        Executes an OpenQASM 2.0 or 3.0 circuit string on Project PRISM.

        Args:
            qasm_code: Valid OpenQASM string (e.g. 'OPENQASM 2.0; qreg q[50]; h q[0]; cx q[0], q[1];')
            mode: 'probabilities' (returns state amplitudes) or 'shots' (returns bitstring counts).
            shots: Number of measurement shots to sample when mode='shots'.
            max_qudits: Maximum qudits permitted (trial bound: 75).

        Returns:
            QasmResult: Execution details, Dirac ket notation or measurement dictionary.
        """
        trimmed = qasm_code.strip()
        if not trimmed:
            raise ValueError("QASM code cannot be empty")

        payload = {
            "qasm": trimmed,
            "mode": mode,
            "shots": shots,
            "max_qudits": max_qudits,
        }
        data = self._post("/api/prism/qasm", payload)

        status = data.get("status", "ok")
        if status != "ok" or data.get("error") is not None:
            err_msg = data.get("error", "QASM execution failed")
            raise QasmParseError(err_msg, raw_response=data)

        return QasmResult(
            num_qubits=data.get("num_qubits", 0),
            gate_count=data.get("gate_count", 0),
            mode=data.get("mode", mode),
            result=data.get("result"),
            counts=data.get("counts"),
            latency_us=float(data.get("latency_us", 0.0)),
            status=status,
        )

    def chemistry(
        self,
        num_qubits: int,
        terms: List[Tuple[str, float]],
        mode: str = "ground_state",
    ) -> ChemistryResult:
        """
        Evaluates a molecular Pauli Hamiltonian to find its global ground state energy.

        Args:
            num_qubits: Number of qubits / spin sites.
            terms: List of (pauli_string, coefficient), e.g. [("Z0 Z1", -1.0), ("X0", 0.5)].
            mode: Evaluation mode (default: 'ground_state').

        Returns:
            ChemistryResult: Ground state energy eigenvalue and optimal bitstring.
        """
        payload = {
            "num_qubits": num_qubits,
            "terms": terms,
            "mode": mode,
        }
        data = self._post("/api/prism/chemistry/eval", payload)

        status = data.get("status", "ok")
        if status != "ok" or data.get("error") is not None:
            raise EvaluationError(data.get("error", "Chemistry evaluation failed"), raw_response=data)

        return ChemistryResult(
            num_qubits=data.get("num_qubits", num_qubits),
            terms_count=data.get("terms_count", len(terms)),
            ground_state_energy=data.get("ground_state_energy"),
            optimal_bitstring=data.get("optimal_bitstring"),
            latency_us=float(data.get("latency_us", 0.0)),
            status=status,
        )
