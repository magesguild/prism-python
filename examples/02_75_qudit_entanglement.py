#!/usr/bin/env python3
"""
02_75_qudit_entanglement.py — Running large OpenQASM circuits on Project PRISM.
Demonstrates microsecond execution of a 75-qubit GHZ entangled state.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import prism

print("=" * 80)
print("Project PRISM — 75-Qubit OpenQASM Entanglement Demo")
print("=" * 80)

qasm_75 = """
OPENQASM 2.0;
qreg q[75];
h q[0];
cx q[0], q[1];
cx q[1], q[2];
"""

print("Submitting 75-qubit circuit to PRISM unauthenticated trial endpoint...")
res = prism.qasm(qasm_75, max_qudits=75)

print(f"\nExecution Status : {res.status}")
print(f"Total Qubits     : {res.num_qubits}")
print(f"Gate Count       : {res.gate_count}")
print(f"PRISM Latency    : {res.latency_us:.2f} µs")
print(f"\nOutput Statevector (Sparse Superposition):\n{res.result}")
