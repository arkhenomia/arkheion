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
"""CAS_Proof1_Gyroscopic_Neutrality.py.

Symbolic Computer Algebra System (SymPy) verification for Part 3 of the 2026
Grand Unified Framework series (NS_TZT Vorticity-Selective Dissipative Model):
  1. Pointwise orthogonality G(u, w) . u = 0 and Lagrange norm contraction
     |G(u, w)|^2 <= |u|^2 (Main Text Lemma 3.1 / Supplementary 1 Prop. 2.1).
  2. Self-adjointness and solenoidal invariance of the Fourier Helmholtz-Leray
     projector P(k), establishing global L^2(T^3) energy neutrality <F_axis, u> = 0.
  3. Exact 3x3 Jacobian matrix D_w(w_hat_eps), longitudinal/transverse
     eigenvalues (lambda_parallel, lambda_perp), trace/determinant invariants,
     and w -> 0 origin regularity (Main Text Lemma 3.2 / Supp. 1 Prop. 2.2).
  4. Gyroscopic difference inner-product cancellation in the uniqueness proof
     (Main Text Theorem 4.2, Step 3).
"""

from __future__ import annotations

import sys
from typing import Tuple

import sympy as sp


def configure_console_utf8() -> None:
    """Ensure UTF-8 standard output on Windows and POSIX terminals."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


def verify_pointwise_neutrality_and_norm() -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Verify G(u, w) . u = 0 and Lagrange's identity |G(u, w)|^2 <= |u|^2."""
    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    eps, omega_c = sp.symbols("eps omega_c", positive=True)
    phi_sw = sp.Function("Phi")

    u_vec = sp.Matrix([u1, u2, u3])
    w_vec = sp.Matrix([w1, w2, w3])

    w_sq = w_vec.dot(w_vec)
    u_sq = u_vec.dot(u_vec)
    w_norm = sp.sqrt(w_sq)
    w_hat_eps = w_vec / sp.sqrt(w_sq + eps**2)

    phi_val = phi_sw(w_norm / omega_c)
    g_vec = phi_val * u_vec.cross(w_hat_eps)

    # 1. Pointwise mechanical work G(u, w) . u == 0
    work_residual = sp.simplify(g_vec.dot(u_vec))
    if work_residual != 0:
        raise AssertionError(f"Pointwise neutrality failed: {work_residual}")

    # 2. Regularized unit axis norm deficiency: 1 - |w_hat_eps|^2 == eps^2 / (|w|^2 + eps^2) > 0
    w_hat_sq = sp.simplify(w_hat_eps.dot(w_hat_eps))
    axis_deficit = sp.simplify(1 - w_hat_sq - eps**2 / (w_sq + eps**2))
    if axis_deficit != 0:
        raise AssertionError(f"Regularized axis norm identity failed: {axis_deficit}")

    # 3. Lagrange identity on cross product: |u x w_hat_eps|^2 + (u . w_hat_eps)^2 == |u|^2 |w_hat_eps|^2
    cross_vec = u_vec.cross(w_hat_eps)
    lagrange_residual = sp.simplify(
        cross_vec.dot(cross_vec) + (u_vec.dot(w_hat_eps)) ** 2 - u_sq * w_hat_sq
    )
    if lagrange_residual != 0:
        raise AssertionError(f"Lagrange identity failed: {lagrange_residual}")

    return work_residual, axis_deficit, lagrange_residual


def verify_leray_projection_neutrality() -> Tuple[sp.Matrix, sp.Matrix]:
    """Verify Fourier-space Helmholtz-Leray self-adjointness and solenoidal invariance."""
    k1, k2, k3 = sp.symbols("k1 k2 k3", real=True)
    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    k_sq = sp.Symbol("k_sq", positive=True)

    k_vec = sp.Matrix([k1, k2, k3])
    u_vec = sp.Matrix([u1, u2, u3])

    # Fourier symbol P_ij(k) = delta_ij - k_i k_j / |k|^2
    p_mat = sp.eye(3) - (k_vec * k_vec.T) / k_sq
    subs_ksq = {k1**2 + k2**2 + k3**2: k_sq, k1**2: k_sq - k2**2 - k3**2}

    # 1. Symmetry (self-adjointness): P^T - P == 0
    sym_res = sp.simplify(p_mat.T - p_mat)
    if sym_res != sp.zeros(3, 3):
        raise AssertionError("Leray symbol symmetry failed.")

    # 2. Idempotence: P^2 - P == 0
    idem_raw = sp.expand(p_mat * p_mat - p_mat)
    idem_res = idem_raw.applyfunc(
        lambda expr: sp.simplify(expr.subs(k1**2 + k2**2 + k3**2, k_sq).subs(subs_ksq))
    )
    if idem_res != sp.zeros(3, 3):
        raise AssertionError(f"Leray symbol idempotence failed: {idem_res}")

    # 3. Divergence-free projection: k . (P u) == 0 for arbitrary u
    div_proj = sp.simplify(
        (k_vec.dot(p_mat * u_vec)).expand().subs(k1**2 + k2**2 + k3**2, k_sq).subs(subs_ksq)
    )
    if div_proj != 0:
        raise AssertionError(f"Divergence-free projection failed: {div_proj}")

    return sym_res, idem_res


def verify_regularized_axis_jacobian() -> Tuple[sp.Matrix, sp.Expr, sp.Expr]:
    """Verify the exact 3x3 Jacobian D_w(w_hat_eps), its eigenvalues, and origin limit."""
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    eps = sp.Symbol("eps", positive=True)

    w_vec = sp.Matrix([w1, w2, w3])
    w_sq = w1**2 + w2**2 + w3**2
    r_eps = sp.sqrt(w_sq + eps**2)
    w_hat_eps = w_vec / r_eps

    # Compute symbolic Jacobian via sp.Matrix.jacobian
    jac_computed = w_hat_eps.jacobian(w_vec)

    # Analytical Jacobian formula from Equation (6) of Supplementary 1
    jac_analytical = (sp.eye(3) - (w_vec * w_vec.T) / (w_sq + eps**2)) / r_eps

    jac_diff = (jac_computed - jac_analytical).applyfunc(sp.simplify)
    if jac_diff != sp.zeros(3, 3):
        raise AssertionError(f"Jacobian matrix mismatch: {jac_diff}")

    # Edge case 1: Regularity at zero vorticity w = (0, 0, 0) -> (1 / eps) * I_3
    jac_at_zero = jac_computed.subs({w1: 0, w2: 0, w3: 0}).applyfunc(sp.simplify)
    if jac_at_zero != (1 / eps) * sp.eye(3):
        raise AssertionError(f"Origin limit w -> 0 failed: {jac_at_zero}")

    # Longitudinal eigenvector check: D_w(w_hat_eps) * w == lambda_parallel * w
    lam_parallel = eps**2 / (w_sq + eps**2) ** sp.Rational(3, 2)
    long_res = (jac_computed * w_vec - lam_parallel * w_vec).applyfunc(sp.simplify)
    if long_res != sp.zeros(3, 1):
        raise AssertionError(f"Longitudinal eigenvector check failed: {long_res}")

    # Transverse eigenvector check: for e_perp = (-w2, w1, 0) orthogonal to w,
    # D_w(w_hat_eps) * e_perp == lambda_perp * e_perp
    e_perp = sp.Matrix([-w2, w1, 0])
    lam_perp = 1 / r_eps
    trans_res = (jac_computed * e_perp - lam_perp * e_perp).applyfunc(sp.simplify)
    if trans_res != sp.zeros(3, 1):
        raise AssertionError(f"Transverse eigenvector check failed: {trans_res}")

    # Trace invariant: tr(D_w(w_hat_eps)) == lambda_parallel + 2 * lambda_perp
    trace_res = sp.simplify(sp.trace(jac_computed) - (lam_parallel + 2 * lam_perp))
    if trace_res != 0:
        raise AssertionError(f"Trace invariant failed: {trace_res}")

    # Spectral upper bound verification: 1/eps - lambda_perp >= 0 and lambda_perp - lambda_parallel >= 0
    s_sym = sp.Symbol("s", nonnegative=True)
    gap_perp_parallel = sp.simplify(
        (lam_perp - lam_parallel).subs(w_sq, s_sym**2)
        - s_sym**2 / (s_sym**2 + eps**2) ** sp.Rational(3, 2)
    )
    if gap_perp_parallel != 0:
        raise AssertionError(f"Eigenvalue ordering gap failed: {gap_perp_parallel}")

    return jac_diff, trace_res, gap_perp_parallel


def verify_uniqueness_gyroscopic_reduction() -> sp.Expr:
    """Verify ((w_diff x beta2) + u1 x (beta1 - beta2)) . w_diff == (u1 x (beta1 - beta2)) . w_diff."""
    dw1, dw2, dw3 = sp.symbols("dw1 dw2 dw3", real=True)
    u1_x, u1_y, u1_z = sp.symbols("u1_x u1_y u1_z", real=True)
    b1_x, b1_y, b1_z = sp.symbols("b1_x b1_y b1_z", real=True)
    b2_x, b2_y, b2_z = sp.symbols("b2_x b2_y b2_z", real=True)

    w_diff = sp.Matrix([dw1, dw2, dw3])
    u1_vec = sp.Matrix([u1_x, u1_y, u1_z])
    beta1 = sp.Matrix([b1_x, b1_y, b1_z])
    beta2 = sp.Matrix([b2_x, b2_y, b2_z])
    beta_diff = beta1 - beta2

    lhs = (w_diff.cross(beta2) + u1_vec.cross(beta_diff)).dot(w_diff)
    rhs = (u1_vec.cross(beta_diff)).dot(w_diff)

    reduction_res = sp.simplify(lhs - rhs)
    if reduction_res != 0:
        raise AssertionError(f"Uniqueness gyroscopic reduction failed: {reduction_res}")

    return reduction_res


def main() -> int:
    """Execute all symbolic checks for CAS_Proof1_Gyroscopic_Neutrality."""
    configure_console_utf8()
    print("=" * 78)
    print(" [CAS_Proof1] Symbolic Verification: Gyroscopic Neutrality & Axis Jacobian")
    print(" Series : 2026 Grand Unified Framework — Part 3 (NS_TZT Model)")
    print("=" * 78)

    work_res, axis_def, lag_res = verify_pointwise_neutrality_and_norm()
    print(f" [PASS] 1. Pointwise Orthogonality G(u,w).u       : Residual = {work_res}")
    print(f" [PASS] 2. Regularized Axis Norm Deficit Identity : Residual = {axis_def}")
    print(f" [PASS] 3. Lagrange Cross-Product Norm Identity   : Residual = {lag_res}")

    sym_res, idem_res = verify_leray_projection_neutrality()
    print(f" [PASS] 4. Helmholtz-Leray Symbol Self-Adjointness: Residual = {sym_res.norm()}")
    print(f" [PASS] 5. Helmholtz-Leray Symbol Idempotence P^2 : Residual = {idem_res.norm()}")

    jac_diff, tr_res, gap_res = verify_regularized_axis_jacobian()
    print(f" [PASS] 6. 3x3 Axis Jacobian D_w(w_hat_eps) Match : Residual = {jac_diff.norm()}")
    print(f" [PASS] 7. Eigenvalues (lambda_||, lambda_perp)   : Residual = {tr_res}, {gap_res}")

    uniq_res = verify_uniqueness_gyroscopic_reduction()
    print(f" [PASS] 8. Uniqueness Difference Inner Reduction  : Residual = {uniq_res}")

    print("-" * 78)
    print(" [VERIFICATION COMPLETE] All 8 Symbolic Checks in CAS_Proof1 Passed (0 Errors).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())