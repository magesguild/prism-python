#!/usr/bin/env python3
"""
03_molecular_chemistry.py — Solving Electronic Molecular Hamiltonians on Project PRISM.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import prism

print("=" * 80)
print("Project PRISM — Molecular Pauli Hamiltonian Ground State Solver")
print("=" * 80)

# Define a 4-site Transverse-Field Ising Chain / Molecular Hamiltonian
# H = -J * sum(Z_i Z_{i+1}) - h * sum(X_i)
hamiltonian_terms = [
    ("Z0 Z1", -1.0),
    ("Z1 Z2", -1.0),
    ("Z2 Z3", -1.0),
    ("Z3 Z0", -1.0),  # periodic boundary
]

print(f"Solving 4-qubit Hamiltonian with {len(hamiltonian_terms)} terms...")
chem = prism.chemistry(num_qubits=4, terms=hamiltonian_terms)

print(f"\nStatus              : {chem.status}")
print(f"Ground State Energy : {chem.energy} Hartree")
print(f"Optimal Bitstring   : |{chem.bitstring}>")
print(f"PRISM Latency       : {chem.latency_us:.2f} µs")
