#!/usr/bin/env python3
"""
04_navier_stokes_fluid.py — 2D Discrete Lattice Fluid Dynamics on Project PRISM.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import prism

print("=" * 80)
print("Project PRISM — 2D Discrete Lattice Fluid Dynamics")
print("=" * 80)

# Simulate vortex injection and boundary stress on a 16x16 grid
script = (
    "F = fluid(16, 16); "
    "F = inject_vortex(F, 8, 8, 2.0); "
    "F = step_hydro(F, 5); "
    "boundary_stress(F)"
)

res = prism.eval(script)
print("Boundary Stress Profile Across Grid Perimeter:")
print(res.result)
print(f"Server-Side Execution Latency: {res.latency_us:.2f} µs")

enstrophy = prism.eval("F = fluid(16, 16); F = inject_vortex(F, 8, 8, 2.0); enstrophy(F)")
print(f"Enstrophy State: {enstrophy.result}")
