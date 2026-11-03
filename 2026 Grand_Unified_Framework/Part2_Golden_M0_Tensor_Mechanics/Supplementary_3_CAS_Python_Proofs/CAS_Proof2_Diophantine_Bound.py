#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 Jung Soo Kim (Arkhenomia Institute) <https://orcid.org/0009-0006-5140-0604>
# SPDX-License-Identifier: CC-BY-NC-4.0 AND LicenseRef-Arkhenomia-Governance-v2.2.0
# ==============================================================================
# Author & Institute: Jung Soo Kim (ORCID: 0009-0006-5140-0604) / Arkhenomia Institute
# License           : CC BY-NC 4.0 (Commercial licensing administered by Arkhenetics; see LICENSE.txt)
# Canonical Repo    : https://github.com/arkhenomia/arkheion
# Dataset Archive   : https://huggingface.co/datasets/arkhenomia/arkheion
# Official Websites : https://arkhenomia.org | https://arkhenetics.com
# ------------------------------------------------------------------------------
# Commercial use, corporate R&D, in-house enterprise deployment, AI knowledge
# distillation, surrogate model training, automated scraping/corpus ingestion,
# OS kernel/hardware/firmware porting (ZINN / Ark-ZPF), network state-index
# synchronization/congestion-control protocol implementation, and high-risk or
# non-peaceful applications are strictly prohibited without a separate written
# commercial license agreement executed with the Author or Arkhenetics. All
# patent rights are expressly reserved; no patent or commercial rights are
# granted by implication. Governed by the latest LICENSE.txt (Policy v2.2.0+).
# ==============================================================================
"""
2026 Grand Unified Framework - Part 2: Golden M0 Tensor Mechanics
Module: CAS_Proof2_Diophantine_Bound.py
Synchronized with: Section 3.1-3.2, Appendix A (Lemma A.1) & Theorem1_Diophantine.lean
"""

import itertools
import sympy as sp


def run_cas_proof2() -> None:
    print("=" * 78)
    print("[CAS_Proof2] Multi-Dimensional Diophantine Bounds & KAM Non-Resonance Audit")
    print("=" * 78)

    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2

    # 1. Symbolic Decomposition of k . omega_phi on Transverse Lattice K_phi
    k1, k2, k3 = sp.symbols("k1 k2 k3", integer=True)
    A_k = k1 - k2 + 2 * k3
    B_k = k2 - k3

    inner_raw = k1 + k2 * phi**(-1) + k3 * phi**(-2)
    inner_golden = A_k + B_k * phi

    assert sp.simplify(inner_raw - inner_golden) == 0, "Failed: Golden basis reduction"
    print("[PASS] 1. Symbolic Reduction k1 + k2*phi^(-1) + k3*phi^(-2) = A_k + B_k*phi: Verified")

    # 2. Exhaustive Lattice Shell Audit on K_phi for k in [-5, 5]^3 \ Z(1, -1, -1)
    phi_num = float(phi.evalf())
    gamma_2d = 1.0 / (2.0 * phi_num)  # Explicit Hurwitz-Golden constant 1 / (2*phi)
    checked_modes = 0
    min_ratio = float("inf")

    for v1, v2, v3 in itertools.product(range(-5, 6), repeat=3):
        if v1 == 0 and v2 == 0 and v3 == 0:
            continue
        # Exclude longitudinal compression line Z*(1, -1, -1) eliminated by div(u) = 0
        if v2 == -v1 and v3 == -v1:
            continue

        a_val = v1 - v2 + 2 * v3
        b_val = v2 - v3
        alg_norm = abs(a_val**2 + a_val * b_val - b_val**2)
        assert alg_norm >= 1, f"Failed integer norm >= 1 at k=({v1},{v2},{v3})"

        k_l1 = abs(v1) + abs(v2) + abs(v3)
        xi_abs = abs(a_val + b_val * phi_num)
        lower_bound = gamma_2d / k_l1

        assert xi_abs >= lower_bound, f"Diophantine bound violated at k=({v1},{v2},{v3})"
        min_ratio = min(min_ratio, xi_abs / lower_bound)
        checked_modes += 1

    print(f"[PASS] 2. Transverse Solenoidal Lattice K_phi Audit ({checked_modes} modes): Verified")
    print(f"       -> Minimum safety ratio |k.omega_phi| / (gamma_phi / |k|) = {min_ratio:.6f} >= 1.0")

    # 3. Full 3D Unconstrained Cubic Pisot Basis Audit (Lemma A.1, tau = 2)
    # Minimal polynomial of Narayana cubic Pisot unit: theta^3 - theta^2 - 1 = 0
    # Here theta^(-1) = theta^2 - theta and theta^(-2) = theta - 1 (Q-linearly independent)
    x = sp.Symbol("x")
    poly_roots = [complex(r.evalf()) for r in sp.Poly(x**3 - x**2 - 1, x).all_roots()]
    poly_roots.sort(key=lambda z: -abs(z))
    theta_real = poly_roots[0].real
    sigma2_theta, sigma3_theta = poly_roots[1], poly_roots[2]

    assert theta_real > 1.0 and abs(sigma2_theta) < 1.0 and abs(sigma3_theta) < 1.0

    def eval_basis(r: complex) -> tuple[complex, complex, complex]:
        return (1.0 + 0j, r**2 - r, r - 1.0)

    b1_r, b2_r, b3_r = eval_basis(theta_real)
    b1_s2, b2_s2, b3_s2 = eval_basis(sigma2_theta)
    M_K = max(abs(b1_s2), abs(b2_s2), abs(b3_s2))
    gamma_cubic = 1.0 / (M_K**2)

    cubic_checked = 0
    for v1, v2, v3 in itertools.product(range(-4, 5), repeat=3):
        if v1 == 0 and v2 == 0 and v3 == 0:
            continue
        xi_1 = (v1 * b1_r + v2 * b2_r + v3 * b3_r).real
        xi_2 = v1 * b1_s2 + v2 * b2_s2 + v3 * b3_s2
        xi_3 = v1 * b1_s2.conjugate() + v2 * b2_s2.conjugate() + v3 * b3_s2.conjugate()

        field_norm = abs(xi_1 * xi_2 * xi_3)
        assert round(field_norm) >= 1, f"Cubic norm < 1 at ({v1},{v2},{v3})"

        k_l1 = abs(v1) + abs(v2) + abs(v3)
        assert abs(xi_1) >= (gamma_cubic / (k_l1**2)) * (1.0 - 1e-12)
        cubic_checked += 1

    print(f"[PASS] 3. Full 3D Cubic Pisot Lattice Audit ({cubic_checked} modes, tau=2): Verified")
    print("=" * 78)
    print("STATUS: ALL CAS_PROOF2 ASSERTIONS PASSED WITH ZERO RESONANCE COLLAPSE.")
    print("=" * 78)


if __name__ == "__main__":
    run_cas_proof2()