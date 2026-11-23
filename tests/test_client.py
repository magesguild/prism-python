"""
Automated unit tests for Project PRISM Python SDK.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import prism


class TestPrismClient(unittest.TestCase):
    def setUp(self):
        self.client = prism.Client()

    def test_arithmetic_eval(self):
        res = self.client.eval("2 + 2")
        self.assertEqual(res.to_int(), 4)
        self.assertGreater(res.latency_us, 0.0)

    def test_alpha_formula(self):
        val = self.client.eval_float("4 * pi^3 + pi^2 + pi")
        self.assertAlmostEqual(val, 137.03630377587845, places=5)

    def test_qasm_75_qubits(self):
        circuit = "OPENQASM 2.0; qreg q[75]; h q[0]; cx q[0], q[1]; cx q[1], q[2];"
        res = self.client.qasm(circuit, max_qudits=75)
        self.assertEqual(res.status, "ok")
        self.assertEqual(res.num_qubits, 75)
        self.assertIn("0.707106", res.result)

    def test_chemistry_ising(self):
        terms = [("Z0 Z1", -1.0), ("Z1 Z2", -1.0)]
        res = self.client.chemistry(num_qubits=3, terms=terms)
        self.assertEqual(res.status, "ok")
        self.assertIsNotNone(res.ground_state_energy)


if __name__ == "__main__":
    unittest.main()
