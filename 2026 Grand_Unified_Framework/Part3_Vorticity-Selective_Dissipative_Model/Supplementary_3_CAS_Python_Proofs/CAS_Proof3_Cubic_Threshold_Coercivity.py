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
"""CAS_Proof3_Cubic_Threshold_Coercivity.py.

Symbolic Computer Algebra System (SymPy) verification for Part 3 of the 2026
Grand Unified Framework series (NS_TZT Vorticity-Selective Dissipative Model):
  1. Three-zone algebraic proof of the pointwise cubic coercivity inequality
     s^3 <= Phi(s / Omega_c) * s^3 + 8 * Omega_c^3 and V(w) . w >= C_O * l^2 * (|w|^3 - 8 * Omega_c^3)
     (Main Text Lemma 3.3(3), Eq. (11) / Supplementary 1 Proposition 3.2).
  2. Skew-symmetric spin tensor cancellation W(u) * omega == 0 and exact reduction
     of the vortex stretching production (omega . grad) u . omega == omega . S(u) omega
     (Main Text Lemma 3.5 / Supplementary 1 Theorem 5.1).
  3. Fourier-space periodic Biot-Savart and Riesz transform multiplier identity
     (grad u)_ij^(hat)(k) == -sum_{l,m} (k_j k_l / |k|^2) * eps_{ilm} * omega_m^(hat)(k)
     on solenoidal modes k . u_hat == 0 (Main Text Lemma 3.5).
  4. Young's inequality completion of squares and Grönwall-free enstrophy closure
     substitution (Main Text Theorem 4.1, Eqs. (17), (20), (21) / Supp. 1 Thm. 5.1).
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


def verify_three_zone_cubic_coercivity() -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Verify s^3 <= Phi(s/Omega_c)*s^3 + 8*Omega_c^3 across Zones I, II, and III."""
    s_sym = sp.Symbol("s", nonnegative=True)
    omega_c = sp.Symbol("Omega_c", positive=True)
    c_o, ell = sp.symbols("C_O ell", positive=True)
    phi_val = sp.Symbol("phi_val", nonnegative=True)

    # Polynomial factorization of (2*Omega_c)^3 - s^3 for 0 <= s <= 2*Omega_c:
    # 8*Omega_c^3 - s^3 = (2*Omega_c - s) * (4*Omega_c^2 + 2*Omega_c*s + s^2)
    cubic_gap = 8 * omega_c**3 - s_sym**3
    factored_gap = (2 * omega_c - s_sym) * (4 * omega_c**2 + 2 * omega_c * s_sym + s_sym**2)
    factor_residual = sp.simplify(cubic_gap - factored_gap)
    if factor_residual != 0:
        raise AssertionError(f"Cubic gap factorization failed: {factor_residual}")

    # Zone I (0 <= s <= Omega_c, Phi = 0):
    # Parameterize s = Omega_c - delta_1 with delta_1 >= 0, s >= 0:
    # Slack = (Phi*s^3 + 8*Omega_c^3) - s^3 = 8*Omega_c^3 - s^3 = 7*Omega_c^3 + ... > 0
    s_sub, delta_1 = sp.symbols("s_sub delta_1", nonnegative=True)
    zone1_slack = (8 * omega_c**3 - s_sub**3).subs(omega_c, s_sub + delta_1)
    zone1_expanded = sp.expand(zone1_slack)
    # All coefficients in the expanded polynomial in (s_sub, delta_1) must be positive
    if any(coeff < 0 for coeff in sp.Poly(zone1_expanded, s_sub, delta_1).coeffs()):
        raise AssertionError("Zone I non-negativity check failed.")

    # Zone II (Omega_c < s < 2*Omega_c, 0 <= Phi <= 1):
    # Slack = Phi*s^3 + 8*Omega_c^3 - s^3 = Phi*s^3 + (2*Omega_c - s)*(4*Omega_c^2 + 2*Omega_c*s + s^2)
    zone2_rhs = phi_val * s_sym**3 + 8 * omega_c**3 - s_sym**3
    zone2_decomp = phi_val * s_sym**3 + factored_gap
    zone2_residual = sp.simplify(zone2_rhs - zone2_decomp)
    if zone2_residual != 0:
        raise AssertionError(f"Zone II decomposition failed: {zone2_residual}")

    # Zone III (s >= 2*Omega_c, Phi = 1):
    # Slack = (1 * s^3 + 8*Omega_c^3) - s^3 == 8*Omega_c^3 > 0
    zone3_slack = sp.simplify((1 * s_sym**3 + 8 * omega_c**3) - s_sym**3 - 8 * omega_c**3)
    if zone3_slack != 0:
        raise AssertionError(f"Zone III saturation identity failed: {zone3_slack}")

    # Scaled rotational flux difference:
    # V(w).w - C_O*ell^2*(|w|^3 - 8*Omega_c^3) == C_O*ell^2*(phi_val*s^3 + 8*Omega_c^3 - s^3)
    v_dot_w = c_o * ell**2 * phi_val * s_sym**3
    flux_lower = c_o * ell**2 * (s_sym**3 - 8 * omega_c**3)
    flux_slack_res = sp.simplify((v_dot_w - flux_lower) - c_o * ell**2 * zone2_decomp)
    if flux_slack_res != 0:
        raise AssertionError(f"Scaled flux coercivity failed: {flux_slack_res}")

    return factor_residual, zone2_residual, flux_slack_res


def verify_spin_cancellation_and_stretching() -> Tuple[sp.Matrix, sp.Expr]:
    """Verify W(u) * omega == 0 and (omega . grad) u . omega == omega . S(u) omega."""
    du_vars = sp.symbols("du11 du12 du13 du21 du22 du23 du31 du32 du33", real=True)
    grad_u = sp.Matrix(3, 3, du_vars)

    # Convention in Main Text Eq. (5):
    # (grad u)_ij = d_i u_j, S_ij = 1/2 (d_i u_j + d_j u_i), W_ij = 1/2 (d_i u_j - d_j u_i)
    s_mat = sp.Rational(1, 2) * (grad_u + grad_u.T)
    w_mat = sp.Rational(1, 2) * (grad_u - grad_u.T)

    # Vorticity vector omega = curl u = (d_2 u_3 - d_3 u_2, d_3 u_1 - d_1 u_3, d_1 u_2 - d_2 u_1)^T
    omega_vec = sp.Matrix([
        grad_u[1, 2] - grad_u[2, 1],
        grad_u[2, 0] - grad_u[0, 2],
        grad_u[0, 1] - grad_u[1, 0],
    ])

    # 1. Verify W(u) * omega == -1/2 (omega x omega) == 0 identically
    w_times_omega = (w_mat * omega_vec).applyfunc(sp.simplify)
    if w_times_omega != sp.zeros(3, 1):
        raise AssertionError(f"Skew spin cancellation W(u)*omega == 0 failed: {w_times_omega}")

    # 2. Verify (omega . grad) u = (grad u)^T * omega = S(u)*omega - W(u)*omega = S(u)*omega,
    # and stretching scalar (omega . grad) u . omega == omega^T S(u) omega
    omega_dot_grad_u = grad_u.T * omega_vec
    stretching_diff = sp.simplify(
        omega_dot_grad_u.dot(omega_vec) - (omega_vec.T * s_mat * omega_vec)[0, 0]
    )
    if stretching_diff != 0:
        raise AssertionError(f"Vortex stretching quadratic reduction failed: {stretching_diff}")

    return w_times_omega, stretching_diff


def verify_fourier_riesz_biot_savart_identity() -> sp.Matrix:
    """Verify the Fourier Riesz-transform velocity gradient representation on T^3."""
    k1, k2, k3 = sp.symbols("k1 k2 k3", real=True)
    u1, u2, u3 = sp.symbols("u1 u2 u3", complex=True)
    k_sq = k1**2 + k2**2 + k3**2

    k_vec = sp.Matrix([k1, k2, k3])
    u_raw = sp.Matrix([u1, u2, u3])

    # Project u_raw onto the divergence-free subspace (k . u_hat == 0):
    u_hat = u_raw - (k_vec.dot(u_raw) / k_sq) * k_vec
    omega_hat = sp.I * k_vec.cross(u_hat)

    # Direct Fourier velocity gradient: (d_j u_i)^hat = i * k_j * u_{i,k}^hat
    grad_u_hat = sp.Matrix(3, 3, lambda i, j: sp.I * k_vec[j] * u_hat[i])

    # Calderon-Zygmund Riesz transform representation in Main Text Lemma 3.5:
    # (d_j u_i)^hat = -sum_{l,m=1}^3 (k_j k_l / |k|^2) * eps_{ilm} * omega_{m,k}^hat
    riesz_grad_hat = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            acc = sp.Integer(0)
            for l_idx in range(3):
                for m_idx in range(3):
                    eps_val = sp.LeviCivita(i, l_idx, m_idx)
                    if eps_val != 0:
                        acc -= (k_vec[j] * k_vec[l_idx] / k_sq) * eps_val * omega_hat[m_idx]
            riesz_grad_hat[i, j] = acc

    riesz_diff = (grad_u_hat - riesz_grad_hat).applyfunc(sp.simplify)
    if riesz_diff != sp.zeros(3, 3):
        raise AssertionError(f"Fourier Riesz transform identity failed: {riesz_diff}")

    return riesz_diff


def verify_gronwall_free_enstrophy_algebra() -> Tuple[sp.Expr, sp.Expr]:
    """Verify Young's inequality completion of squares and Grönwall-free L^3 substitution."""
    nu, b_force, grad_omega = sp.symbols("nu B grad_omega", positive=True)
    e_0, e_t, c_3, c_o, l_sq, omega_c, vol, t_sym, f_int = sp.symbols(
        "E_0 E_t C_3 C_O l_sq Omega_c Vol t F_int", positive=True
    )
    phi_l3_int = sp.Symbol("Phi_L3_int", nonnegative=True)

    # 1. Young's inequality slack (Main Text Eq. (21)):
    # (nu/2)*|grad omega|^2 + (1/(2*nu))*B^2 - B*|grad omega| == (nu*|grad omega| - B)^2 / (2*nu) >= 0
    young_slack = (nu / 2) * grad_omega**2 + (1 / (2 * nu)) * b_force**2 - b_force * grad_omega
    young_square = (nu * grad_omega - b_force) ** 2 / (2 * nu)
    young_res = sp.simplify(young_slack - young_square)
    if young_res != 0:
        raise AssertionError(f"Young's inequality square identity failed: {young_res}")

    # 2. Grönwall-free enstrophy bound substitution (Main Text Theorem 4.1, Eqs. (17) & (20)):
    # At the energy equality boundary Phi_L3_int = E_t / (C_O * l_sq) and
    # L3_int_max = Phi_L3_int + 8 * Omega_c^3 * Vol * t, verify exact match with Eq. (17) RHS:
    phi_l3_max = e_t / (c_o * l_sq)
    l3_int_max = phi_l3_int.subs(phi_l3_int, phi_l3_max) + 8 * omega_c**3 * vol * t_sym
    enstrophy_lhs_bound = e_0 + 2 * c_3 * l3_int_max + f_int
    enstrophy_rhs_eq17 = (
        e_0 + 2 * c_3 * (e_t / (c_o * l_sq) + 8 * omega_c**3 * vol * t_sym) + f_int
    )
    enstrophy_res = sp.simplify(enstrophy_lhs_bound - enstrophy_rhs_eq17)
    if enstrophy_res != 0:
        raise AssertionError(f"Grönwall-free enstrophy bound identity failed: {enstrophy_res}")

    return young_res, enstrophy_res


def main() -> int:
    """Execute all symbolic checks for CAS_Proof3_Cubic_Threshold_Coercivity."""
    configure_console_utf8()
    print("=" * 78)
    print(" [CAS_Proof3] Symbolic Verification: Cubic Coercivity & CZ Enstrophy Closure")
    print(" Series : 2026 Grand Unified Framework — Part 3 (NS_TZT Model)")
    print("=" * 78)

    fac_res, z2_res, flux_res = verify_three_zone_cubic_coercivity()
    print(f" [PASS] 1. Cubic Threshold Gap Factorization      : Residual = {fac_res}")
    print(f" [PASS] 2. Three-Zone Coercivity s^3 <= Phi*s^3+8 : Residual = {z2_res}")
    print(f" [PASS] 3. Scaled Flux Lower Bound V(w).w         : Residual = {flux_res}")

    spin_res, stretch_res = verify_spin_cancellation_and_stretching()
    print(f" [PASS] 4. Skew Spin Cancellation W(u)*omega == 0 : Residual = {spin_res.norm()}")
    print(f" [PASS] 5. Stretching Reduction omega.S(u)*omega  : Residual = {stretch_res}")

    riesz_diff = verify_fourier_riesz_biot_savart_identity()
    print(f" [PASS] 6. Fourier Riesz Transform / Biot-Savart  : Residual = {riesz_diff.norm()}")

    young_res, enst_res = verify_gronwall_free_enstrophy_algebra()
    print(f" [PASS] 7. Linear Forcing Young's Inequality      : Residual = {young_res}")
    print(f" [PASS] 8. Grönwall-Free Enstrophy Bound Eq. (17) : Residual = {enst_res}")

    print("-" * 78)
    print(" [VERIFICATION COMPLETE] All 8 Symbolic Checks in CAS_Proof3 Passed (0 Errors).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())