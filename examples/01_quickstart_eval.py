#!/usr/bin/env python3
"""
01_quickstart_eval.py — Basic evaluation examples using Project PRISM.
"""

import sys
import os

# Add local src to path for direct running without pip install
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import prism

print("=" * 70)
print("Project PRISM — Quickstart Arithmetic & Matrix Evaluation")
print("=" * 70)

# 1. Euler's Identity
euler = prism.eval("exp(i * pi) + 1")
print(f"e^(i*pi) + 1 = {euler.result}  (Latency: {euler.latency_us:.2f} µs)")

# 2. Transcendental Calculus (Fine-Structure Constant Formula)
alpha = prism.eval_float("4 * pi^3 + pi^2 + pi")
print(f"Alpha^-1 formula = {alpha:.10f}")

# 3. Complex 2x2 Matrix Inversion
mat = prism.eval("inv([[4, 7], [2, 6]])")
print(f"\nMatrix Inverse of [[4, 7], [2, 6]]:\n{mat.result}\n(Latency: {mat.latency_us:.2f} µs)")

# 4. Multi-Level Qudit States (Bell State & Entanglement Entropy)
bell = prism.eval("q = bell(); probabilities(q)")
print(f"\nBell State |Φ+> Amplitudes:\n{bell.result}")

entropy = prism.eval("entropy(bell(), 0)")
print(f"Entanglement Entropy: {entropy.result} ebits  (ln(2) ≈ 0.6931)")
