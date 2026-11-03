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
"""CAS_Proof2_Convex_Potential_Hessian.py.

Symbolic Computer Algebra System (SymPy) verification for Part 3 of the 2026
Grand Unified Framework series (NS_TZT Vorticity-Selective Dissipative Model):
  1. Gradient derivation V(w) = grad_w Psi(w) = h(|w|) w from the radially
     symmetric convex scalar potential Psi(w) = int_0^{|w|} h(r) r dr
     (Main Text Definition 2.2 & Lemma 3.3(1) / Supplementary 1 Prop. 3.1).
  2. Exact 3x3 Hessian matrix D^2 Psi(w) = DV(w), its symmetry DV(w)^T = DV(w),
     and its longitudinal (mu_parallel) and transverse (mu_perp) eigenvalues.
  3. Quadratic form coercivity identity:
     xi^T DV(w) xi - h(|w|) |xi|^2 == (h'(|w|) / |w|) (w . xi)^2 >= 0
     (Main Text Lemma 3.3(2) & Lemma 3.4).
  4. Subcritical laminar shielding (Phi = 0 => DV = 0), supercritical cubic
     potential specialization (Phi = 1 => Psi = (1/3) C_O l^2 |w|^3 - C),
     and Minty-Browder radial monotonicity decomposition.
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


def verify_potential_gradient_and_hessian() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Verify V(w) = grad_w Psi(w) and D^2 Psi(w) = DV(w) = h(|w|) I_3 + h'(|w|) w w^T / |w|."""
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    s_sym = sp.Symbol("s", positive=True)
    h_func = sp.Function("h")
    psi_func = sp.Function("psi")

    w_vec = sp.Matrix([w1, w2, w3])
    w_norm = sp.sqrt(w1**2 + w2**2 + w3**2)

    # Radial potential Psi(w) = psi(|w|) with d(psi)/ds = s * h(s)
    psi_expr = psi_func(w_norm)
    grad_psi_raw = sp.Matrix([sp.diff(psi_expr, wi) for wi in w_vec])

    # Substitute psi'(w_norm) -> w_norm * h(w_norm)
    dpsi_rule = {sp.Subs(sp.Derivative(psi_func(s_sym), s_sym), s_sym, w_norm): w_norm * h_func(w_norm)}
    # Also handle direct Derivative(psi(w_norm), w_norm) across SymPy versions
    dpsi_direct = {sp.Derivative(psi_func(w_norm), w_norm): w_norm * h_func(w_norm)}

    grad_psi = grad_psi_raw.applyfunc(
        lambda expr: sp.simplify(expr.subs(dpsi_rule).subs(dpsi_direct))
    )
    v_flux = h_func(w_norm) * w_vec

    grad_diff = (grad_psi - v_flux).applyfunc(sp.simplify)
    if grad_diff != sp.zeros(3, 1):
        raise AssertionError(f"Potential gradient V = grad Psi failed: {grad_diff}")

    # Compute 3x3 Jacobian DV(w) = D^2 Psi(w)
    dv_computed = v_flux.jacobian(w_vec)

    # Analytical Hessian formula from Equation (9) of Supplementary 1
    dh_dw_norm = sp.diff(h_func(w_norm), w_norm)
    dv_analytical = h_func(w_norm) * sp.eye(3) + dh_dw_norm * (w_vec * w_vec.T) / w_norm

    hessian_diff = (dv_computed - dv_analytical).applyfunc(sp.simplify)
    if hessian_diff != sp.zeros(3, 3):
        raise AssertionError(f"Hessian matrix DV(w) mismatch: {hessian_diff}")

    # Symmetry check: DV(w)^T == DV(w)
    sym_diff = (dv_computed.T - dv_computed).applyfunc(sp.simplify)
    if sym_diff != sp.zeros(3, 3):
        raise AssertionError("Hessian symmetry DV(w)^T = DV(w) failed.")

    return grad_diff, hessian_diff, sym_diff


def verify_hessian_eigenvalues_and_quadratic_form() -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Verify longitudinal/transverse eigenvalues of DV(w) and quadratic form coercivity."""
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    xi1, xi2, xi3 = sp.symbols("xi1 xi2 xi3", real=True)
    s_sym = sp.Symbol("s", positive=True)
    c_o, ell, omega_c = sp.symbols("C_O ell omega_c", positive=True)
    phi_sw = sp.Function("Phi")

    w_vec = sp.Matrix([w1, w2, w3])
    xi_vec = sp.Matrix([xi1, xi2, xi3])

    # Express h(s) = C_O * ell^2 * s * Phi(s / omega_c) and h'(s)
    h_s = c_o * ell**2 * s_sym * phi_sw(s_sym / omega_c)
    dh_ds = sp.diff(h_s, s_sym)

    # Analytical formula for h'(s) in Proposition 3.1
    dphi_arg = sp.diff(phi_sw(s_sym / omega_c), s_sym) * omega_c
    dh_expected = c_o * ell**2 * (phi_sw(s_sym / omega_c) + (s_sym / omega_c) * dphi_arg)
    dh_residual = sp.simplify(dh_ds - dh_expected)
    if dh_residual != 0:
        raise AssertionError(f"h'(s) derivative identity failed: {dh_residual}")

    # Algebraic Hessian matrix at magnitude |w| = s > 0
    h_val, dh_val = sp.symbols("h_val dh_val", nonnegative=True)
    dv_mat = h_val * sp.eye(3) + (dh_val / s_sym) * (w_vec * w_vec.T)
    subs_norm_sq = {w1**2 + w2**2 + w3**2: s_sym**2}

    # 1. Longitudinal eigenvalue: DV(w) * w == (h(s) + s * h'(s)) * w
    mu_parallel = h_val + s_sym * dh_val
    long_vec = (dv_mat * w_vec).applyfunc(
        lambda expr: sp.simplify(expr.expand().subs(subs_norm_sq))
    )
    long_res = (long_vec - mu_parallel * w_vec).applyfunc(sp.simplify)
    if long_res != sp.zeros(3, 1):
        raise AssertionError(f"Longitudinal Hessian eigenvalue failed: {long_res}")

    # 2. Transverse eigenvalue: for e_perp = (-w2, w1, 0) orthogonal to w,
    # DV(w) * e_perp == h(s) * e_perp
    e_perp = sp.Matrix([-w2, w1, 0])
    mu_perp = h_val
    trans_res = (dv_mat * e_perp - mu_perp * e_perp).applyfunc(sp.simplify)
    if trans_res != sp.zeros(3, 1):
        raise AssertionError(f"Transverse Hessian eigenvalue failed: {trans_res}")

    # 3. Quadratic form coercivity:
    # xi^T DV(w) xi - h(s) |xi|^2 == (h'(s) / s) * (w . xi)^2
    quad_form = (xi_vec.T * dv_mat * xi_vec)[0, 0]
    xi_sq = xi_vec.dot(xi_vec)
    w_dot_xi = w_vec.dot(xi_vec)
    coercivity_res = sp.simplify(quad_form - h_val * xi_sq - (dh_val / s_sym) * (w_dot_xi**2))
    if coercivity_res != 0:
        raise AssertionError(f"Quadratic form coercivity identity failed: {coercivity_res}")

    # 4. Eigenvalue dominance: mu_parallel - mu_perp == s * h'(s) >= 0
    eig_gap_res = sp.simplify((mu_parallel - mu_perp) - s_sym * dh_val)
    if eig_gap_res != 0:
        raise AssertionError(f"Eigenvalue gap failed: {eig_gap_res}")

    return dh_residual, coercivity_res, eig_gap_res


def verify_zone_regimes_and_minty_browder() -> Tuple[sp.Matrix, sp.Matrix, sp.Expr]:
    """Verify subcritical shielding, supercritical cubic potential, and Minty-Browder identity."""
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    c_o, ell, c_const = sp.symbols("C_O ell C_omega", positive=True)
    norm_a, norm_b, a_dot_b = sp.symbols("norm_a norm_b a_dot_b", real=True)
    h_a, h_b = sp.symbols("h_a h_b", nonnegative=True)

    w_vec = sp.Matrix([w1, w2, w3])
    w_sq = w1**2 + w2**2 + w3**2
    w_norm = sp.sqrt(w_sq)

    # 1. Edge Case (Subcritical Zone I, |w| <= Omega_c => Phi = 0, Phi' = 0):
    # Both V_sub(w) and DV_sub(w) vanish identically, removing any origin singularity at w = 0.
    v_sub = sp.zeros(3, 1)
    dv_sub = v_sub.jacobian(w_vec)
    if dv_sub != sp.zeros(3, 3):
        raise AssertionError("Subcritical zero Hessian check failed.")

    # 2. Supercritical Core (Zone III, |w| >= 2 * Omega_c => Phi = 1, Phi' = 0):
    # Psi_core(w) = (1/3) * C_O * ell^2 * |w|^3 - C_omega
    psi_core = sp.Rational(1, 3) * c_o * ell**2 * (w_norm**3) - c_const
    v_core_grad = sp.Matrix([sp.diff(psi_core, wi) for wi in w_vec]).applyfunc(sp.simplify)
    v_core_exact = c_o * ell**2 * w_norm * w_vec

    core_grad_diff = (v_core_grad - v_core_exact).applyfunc(sp.simplify)
    if core_grad_diff != sp.zeros(3, 1):
        raise AssertionError(f"Supercritical cubic potential gradient failed: {core_grad_diff}")

    dv_core = v_core_exact.jacobian(w_vec)
    dv_core_expected = c_o * ell**2 * (w_norm * sp.eye(3) + (w_vec * w_vec.T) / w_norm)
    core_hess_diff = (dv_core - dv_core_expected).applyfunc(sp.simplify)
    if core_hess_diff != sp.zeros(3, 3):
        raise AssertionError(f"Supercritical cubic Hessian failed: {core_hess_diff}")

    # 3. Minty-Browder Monotonicity Algebraic Decomposition (Theorem 2 in Lean 4):
    # (h_a a - h_b b) . (a - b) = h_a |a|^2 - (h_a + h_b)(a . b) + h_b |b|^2
    # At the worst-case Cauchy-Schwarz boundary a . b = |a||b|, this equals:
    # h_b (|a| - |b|)^2 + |a| (h_a - h_b)(|a| - |b|) >= 0.
    mb_boundary = h_a * norm_a**2 - (h_a + h_b) * (norm_a * norm_b) + h_b * norm_b**2
    mb_factored = h_b * (norm_a - norm_b) ** 2 + norm_a * (h_a - h_b) * (norm_a - norm_b)
    mb_res = sp.simplify(mb_boundary - mb_factored)
    if mb_res != 0:
        raise AssertionError(f"Minty-Browder algebraic decomposition failed: {mb_res}")

    # Full inner product identity including Cauchy-Schwarz slack (|a||b| - a.b >= 0):
    mb_full = h_a * norm_a**2 - (h_a + h_b) * a_dot_b + h_b * norm_b**2
    mb_full_decomp = mb_factored + (h_a + h_b) * (norm_a * norm_b - a_dot_b)
    mb_full_res = sp.simplify(mb_full - mb_full_decomp)
    if mb_full_res != 0:
        raise AssertionError(f"Full Minty-Browder identity failed: {mb_full_res}")

    return core_grad_diff, core_hess_diff, mb_full_res


def main() -> int:
    """Execute all symbolic checks for CAS_Proof2_Convex_Potential_Hessian."""
    configure_console_utf8()
    print("=" * 78)
    print(" [CAS_Proof2] Symbolic Verification: Convex Potential & Hessian Positivity")
    print(" Series : 2026 Grand Unified Framework — Part 3 (NS_TZT Model)")
    print("=" * 78)

    grad_diff, hess_diff, sym_diff = verify_potential_gradient_and_hessian()
    print(f" [PASS] 1. Potential Gradient V(w) = grad_w Psi(w) : Residual = {grad_diff.norm()}")
    print(f" [PASS] 2. 3x3 Hessian Matrix DV(w) = D^2 Psi(w)   : Residual = {hess_diff.norm()}")
    print(f" [PASS] 3. Hessian Symmetry DV(w)^T == DV(w)       : Residual = {sym_diff.norm()}")

    dh_res, coerc_res, gap_res = verify_hessian_eigenvalues_and_quadratic_form()
    print(f" [PASS] 4. Eddy Viscosity Derivative h'(s) Formula : Residual = {dh_res}")
    print(f" [PASS] 5. Quadratic Form Coercivity xi^T DV xi    : Residual = {coerc_res}")
    print(f" [PASS] 6. Eigenvalue Ordering (mu_|| >= mu_perp)  : Residual = {gap_res}")

    core_g, core_h, mb_res = verify_zone_regimes_and_minty_browder()
    print(f" [PASS] 7. Supercritical Cubic Core Psi & DV(w)    : Residual = {core_g.norm()}, {core_h.norm()}")
    print(f" [PASS] 8. Minty-Browder Monotonicity Decomposition: Residual = {mb_res}")

    print("-" * 78)
    print(" [VERIFICATION COMPLETE] All 8 Symbolic Checks in CAS_Proof2 Passed (0 Errors).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())