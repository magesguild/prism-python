# Project PRISM Python SDK (`prism-calc`)

```text
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                 PROJECT PRISM MATHEMATICAL ENGINE (prism-calc)                        ║
║            Official Python SDK & Quantum Runtime Client (Python 3.8+)                 ║
║                        Mage's Guild Psychonautics LLC                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/prism-calc/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation](https://img.shields.io/badge/docs-magesguild.io%2Fdev-gold.svg)](https://www.magesguild.io/dev)
[![Showroom](https://img.shields.io/badge/calculator-live_eval-green.svg)](https://www.magesguild.io/calculator)

The official Python client library for the **Project PRISM Mathematical Engine (`prism-calc`)**, developed by **Mage's Guild Psychonautics LLC**.

Provides zero-dependency access to microsecond scientific arithmetic, complex linear algebra, multi-level qudits ($d \ge 2$), OpenQASM 2.0/3.0 circuit execution (up to 75 qudits during public trial), and molecular electronic Hamiltonian ground-state solvers.

---

## ⚡ Public Trial Access Notice

> **Public Trial Mode Active:** Until **Friday, November 27, 2026 at 23:59:59 UTC**, Project PRISM's cloud evaluation endpoints are accessible **without authentication** for circuits up to **75 qudits**.
> 
> * No API key required for public trial evaluation.
> * Zero installation prerequisites (uses Python standard library).

---

## 🚀 Quickstart

### 1. Installation (Virtual Environment Quickstart)

You do **not** need to wait for a PyPI release. You can install and run the official client directly from this GitHub repository inside a clean Python virtual environment right now:

```bash
# 1. Create and activate a clean virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install directly from this GitHub repository
pip install git+https://github.com/magesguild/prism-python.git

# --- OR: Clone and install in editable development mode ---
git clone https://github.com/magesguild/prism-python.git
cd prism-python
pip install -e .
```

*(Note: Once published to PyPI, standard `pip install prism-calc` will also be available.)*

### 2. Zero-Install / Copy-Paste Mode (No `pip install` Required)

Because the client uses **only standard library Python (`urllib` and `json`)**, you can even skip `pip` entirely: simply copy `src/prism/client.py` directly into your research project or Jupyter notebook!

### 2. Basic Arithmetic & Complex Matrices

```python
import prism

# 1. Scientific Arithmetic & Transcendental Calculus
euler = prism.eval("exp(i * pi) + 1")
print(euler)  # 0  (25.67 µs)

# 2. High-Precision Physical Constants (e.g. Fine-Structure Constant)
alpha_inv = prism.eval_float("4 * pi^3 + pi^2 + pi")
print(alpha_inv)  # 137.03630377587845

# 3. Complex Matrix Inversion
mat = prism.eval("inv([[4, 7], [2, 6]])")
print(mat)
# [2x2 Matrix]:
#   [0.6, -0.7]
#   [-0.2, 0.4]  (30.30 µs)
```

---

## 🌌 Quantum Circuit Simulation (OpenQASM)

Run large-scale quantum circuits up to **75 qudits** with microsecond execution:

```python
import prism

# 75-Qubit Entangled GHZ State
qasm_circuit = """
OPENQASM 2.0;
qreg q[75];
h q[0];
cx q[0], q[1];
cx q[1], q[2];
"""

res = prism.qasm(qasm_circuit, max_qudits=75)
print(f"Total Qubits: {res.num_qubits}")
print(f"Gate Count  : {res.gate_count}")
print(f"Latency     : {res.latency_us:.2f} µs")
print(f"Statevector : {res.result}")
```

**Output:**
```text
Total Qubits: 75
Gate Count  : 3
Latency     : 22.28 µs
Statevector : (0.7071)|000...000> + (0.7071)|111...000>
```

### Measurement Sampling (Shots Mode)

```python
# Sample 1024 shots on a Bell state
bell_qasm = """
OPENQASM 2.0;
qreg q[2];
creg c[2];
h q[0];
cx q[0], q[1];
measure q -> c;
"""

shots_res = prism.qasm(bell_qasm, mode="shots", shots=1024)
print(shots_res.counts)  # {'00': 512, '11': 512}
```

---

## 🧪 Molecular Electronic Chemistry

Solve molecular Pauli Hamiltonians and Ising spin glasses to global ground state eigenvalues:

```python
import prism

# 4-site Transverse-Field Ising Chain: H = -sum(Z_i Z_{i+1})
terms = [
    ("Z0 Z1", -1.0),
    ("Z1 Z2", -1.0),
    ("Z2 Z3", -1.0),
    ("Z3 Z0", -1.0),
]

chem = prism.chemistry(num_qubits=4, terms=terms)
print(f"Ground State Energy: {chem.energy} Hartree")
print(f"Optimal Bitstring  : |{chem.bitstring}>")
print(f"Execution Latency  : {chem.latency_us:.2f} µs")
```

---

## 💻 Interactive Terminal REPL

Launch an interactive calculation shell directly in your console:

```bash
# Start interactive terminal
prism

# Or evaluate an expression directly
prism "inv([[4, 7], [2, 6]])"
```

```text
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                 PROJECT PRISM MATHEMATICAL ENGINE (prism-calc)                        ║
║            Mage's Guild Psychonautics LLC — Official Python SDK REPL                  ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
Connected to https://www.magesguild.io (Unauthenticated Trial Mode). Type 'exit' to quit.

prism>> q = bell(); probabilities(q)
[0.5, 0, 0, 0.5]  (18.42 µs)

prism>> entropy(bell(), 0)
0.693147180559945  (14.12 µs)
```

---

## 🛠️ Advanced Client Configuration

For custom configurations, proxy routing, or enterprise API keys:

```python
from prism import PrismClient

client = PrismClient(
    base_url="https://www.magesguild.io", # Default
    api_key=None,                         # Unauthenticated during trial
    timeout=30.0                          # Seconds
)

res = client.eval("det([[1, 2], [3, 4]])")
print(res.to_int())  # -2
```

---

## 📖 Links & Resources

* **Interactive Web Showroom:** [https://www.magesguild.io/calculator](https://www.magesguild.io/calculator)
* **Canonical DevPortal (`/dev`):** [https://www.magesguild.io/dev](https://www.magesguild.io/dev)
* **Company Inquiries:** [mailto:licensing@magesguild.io](mailto:licensing@magesguild.io)

---

## License

Apache License 2.0. Copyright © 2026 Mage's Guild Psychonautics LLC. All rights reserved.
