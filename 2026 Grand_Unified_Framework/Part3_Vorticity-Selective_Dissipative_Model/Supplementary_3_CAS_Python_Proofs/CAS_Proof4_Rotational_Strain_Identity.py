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
"""CAS_Proof4_Rotational_Strain_Identity.py.

Symbolic Computer Algebra System (SymPy) verification for Part 3 of the 2026
Grand Unified Framework series (NS_TZT Vorticity-Selective Dissipative Model):
  1. Exhaustive 81-component verification of the Levi-Civita contraction
     identity eps_{ijk} eps_{klm} == delta_{il} delta_{jm} - delta_{im} delta_{jl}
     (Main Text Appendix A, Lemma A.1 / Supplementary 1 Theorem 4.1).
  2. Exact unconstrained 3D vector calculus identity:
     -curl(nu_t * omega) == div(2 * nu_t * S(u)) - 2 * nu_t * grad(div u)
                            - 2 * (grad u)^T * grad(nu_t).
  3. Exact solenoidal rotational-to-strain bridge identity under div u == 0:
     -curl(nu_t * omega) == div(2 * nu_t * S(u)) - 2 * (grad u)^T * grad(nu_t)
     (Main Text Equation (28) & Lemma A.1).
  4. Interior homogeneous vortex core equivalence (grad(nu_t) == 0, div u == 0
     => -curl(nu_t * omega) == div(2 * nu_t * S(u)) == nu_t * Laplacian(u))
     and pointwise divergence identity for global L^2(T^3) dissipation.
"""

from __future__ import annotations

import itertools
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


def verify_levi_civita_contraction() -> int:
    """Verify eps_{ijk} eps_{klm} == delta_{il} delta_{jm} - delta_{im} delta_{jl} on {0,1,2}^4."""
    mismatch_count = 0
    for i, j, l_idx, m_idx in itertools.product(range(3), repeat=4):
        lhs = sum(
            sp.LeviCivita(i, j, k) * sp.LeviCivita(k, l_idx, m_idx)
            for k in range(3)
        )
        rhs = (
            sp.KroneckerDelta(i, l_idx) * sp.KroneckerDelta(j, m_idx)
            - sp.KroneckerDelta(i, m_idx) * sp.KroneckerDelta(j, l_idx)
        )
        if sp.simplify(lhs - rhs) != 0:
            mismatch_count += 1

    if mismatch_count != 0:
        raise AssertionError(f"Levi-Civita contraction failed on {mismatch_count} indices.")

    return mismatch_count


def verify_rotational_to_strain_identities() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Verify the unconstrained, solenoidal, and interior-core rotational-to-strain identities."""
    x, y, z = sp.symbols("x y z", real=True)
    coords = (x, y, z)

    ux_fn = sp.Function("u_x")(x, y, z)
    uy_fn = sp.Function("u_y")(x, y, z)
    uz_fn = sp.Function("u_z")(x, y, z)
    nut_fn = sp.Function("nu_t")(x, y, z)

    u_vec = sp.Matrix([ux_fn, uy_fn, uz_fn])

    # 1. Vorticity omega = curl u: omega_k = eps_{klm} d_l u_m
    omega_vec = sp.Matrix([
        sp.diff(u_vec[2], y) - sp.diff(u_vec[1], z),
        sp.diff(u_vec[0], z) - sp.diff(u_vec[2], x),
        sp.diff(u_vec[1], x) - sp.diff(u_vec[0], y),
    ])

    # 2. Rotational dissipation F_rot = -curl(nu_t * omega)
    nut_omega = nut_fn * omega_vec
    f_rot = -sp.Matrix([
        sp.diff(nut_omega[2], y) - sp.diff(nut_omega[1], z),
        sp.diff(nut_omega[0], z) - sp.diff(nut_omega[2], x),
        sp.diff(nut_omega[1], x) - sp.diff(nut_omega[0], y),
    ])

    # 3. Symmetric strain divergence F_sym_i = d_j (2 * nu_t * S_{ij}),
    # where S_{ij} = 1/2 (d_i u_j + d_j u_i)
    f_sym = sp.zeros(3, 1)
    for i in range(3):
        f_sym[i] = sum(
            sp.diff(nut_fn * (sp.diff(u_vec[j], coords[i]) + sp.diff(u_vec[i], coords[j])), coords[j])
            for j in range(3)
        )

    # 4. Commutator 2 * (grad u)^T * grad(nu_t), i-th component = 2 * sum_j (d_i u_j)(d_j nu_t)
    commutator_vec = sp.zeros(3, 1)
    for i in range(3):
        commutator_vec[i] = 2 * sum(
            sp.diff(u_vec[j], coords[i]) * sp.diff(nut_fn, coords[j])
            for j in range(3)
        )

    # 5. Divergence gradient 2 * nu_t * grad(div u)
    div_u = sp.diff(ux_fn, x) + sp.diff(uy_fn, y) + sp.diff(uz_fn, z)
    grad_div_term = 2 * nut_fn * sp.Matrix([sp.diff(div_u, c) for c in coords])

    # Check A: Unconstrained Vector Identity (for arbitrary smooth u)
    unconstrained_res = (f_rot - (f_sym - grad_div_term - commutator_vec)).applyfunc(sp.simplify)
    if unconstrained_res != sp.zeros(3, 1):
        raise AssertionError(f"Unconstrained identity failed: {unconstrained_res}")

    # Check B: Solenoidal Identity (Main Text Eq. (28) & Lemma A.1) under div u == 0
    # Impose d_x u_x = -(d_y u_y + d_z u_z) and its spatial partial derivatives
    solenoidal_subs = {
        sp.diff(ux_fn, x, x): -(sp.diff(uy_fn, x, y) + sp.diff(uz_fn, x, z)),
        sp.diff(ux_fn, x, y): -(sp.diff(uy_fn, y, y) + sp.diff(uz_fn, y, z)),
        sp.diff(ux_fn, x, z): -(sp.diff(uy_fn, y, z) + sp.diff(uz_fn, z, z)),
        sp.diff(ux_fn, x): -(sp.diff(uy_fn, y) + sp.diff(uz_fn, z)),
    }
    solenoidal_res = (f_rot - (f_sym - commutator_vec)).applyfunc(
        lambda expr: sp.simplify(expr.doit().subs(solenoidal_subs))
    )
    if solenoidal_res != sp.zeros(3, 1):
        raise AssertionError(f"Solenoidal identity Eq. (28) failed: {solenoidal_res}")

    # Check C: Interior Homogeneous Vortex Core Equivalence (grad(nu_t) == 0, div u == 0)
    # Verify -curl(nu_t * omega) == nu_t * Laplacian(u)
    const_nut_subs = {
        sp.diff(nut_fn, x): 0,
        sp.diff(nut_fn, y): 0,
        sp.diff(nut_fn, z): 0,
    }
    laplacian_u = sp.Matrix([
        sp.diff(u_comp, x, x) + sp.diff(u_comp, y, y) + sp.diff(u_comp, z, z)
        for u_comp in u_vec
    ])
    core_res = (f_rot - nut_fn * laplacian_u).applyfunc(
        lambda expr: sp.simplify(expr.doit().subs(const_nut_subs).subs(solenoidal_subs))
    )
    if core_res != sp.zeros(3, 1):
        raise AssertionError(f"Interior core equivalence failed: {core_res}")

    return unconstrained_res, solenoidal_res, core_res


def verify_vector_potential_solenoidal_witness() -> Tuple[sp.Matrix, sp.Expr]:
    """Verify Eq. (28) and the L^2 dissipation density identity for u = curl Psi."""
    x, y, z = sp.symbols("x y z", real=True)
    coords = (x, y, z)

    psi1 = sp.Function("Psi_1")(x, y, z)
    psi2 = sp.Function("Psi_2")(x, y, z)
    psi3 = sp.Function("Psi_3")(x, y, z)
    nut_fn = sp.Function("nu_t")(x, y, z)

    # Construct an identically divergence-free velocity field u = curl Psi
    u_sol = sp.Matrix([
        sp.diff(psi3, y) - sp.diff(psi2, z),
        sp.diff(psi1, z) - sp.diff(psi3, x),
        sp.diff(psi2, x) - sp.diff(psi1, y),
    ])

    # Confirm div(curl Psi) == 0 identically
    div_u_sol = sp.simplify(
        sp.diff(u_sol[0], x) + sp.diff(u_sol[1], y) + sp.diff(u_sol[2], z)
    )
    if div_u_sol != 0:
        raise AssertionError(f"div(curl Psi) != 0: {div_u_sol}")

    omega_sol = sp.Matrix([
        sp.diff(u_sol[2], y) - sp.diff(u_sol[1], z),
        sp.diff(u_sol[0], z) - sp.diff(u_sol[2], x),
        sp.diff(u_sol[1], x) - sp.diff(u_sol[0], y),
    ])

    nut_omega = nut_fn * omega_sol
    f_rot = -sp.Matrix([
        sp.diff(nut_omega[2], y) - sp.diff(nut_omega[1], z),
        sp.diff(nut_omega[0], z) - sp.diff(nut_omega[2], x),
        sp.diff(nut_omega[1], x) - sp.diff(nut_omega[0], y),
    ])

    f_sym = sp.zeros(3, 1)
    commutator_vec = sp.zeros(3, 1)
    for i in range(3):
        f_sym[i] = sum(
            sp.diff(nut_fn * (sp.diff(u_sol[j], coords[i]) + sp.diff(u_sol[i], coords[j])), coords[j])
            for j in range(3)
        )
        commutator_vec[i] = 2 * sum(
            sp.diff(u_sol[j], coords[i]) * sp.diff(nut_fn, coords[j])
            for j in range(3)
        )

    # Without any manual substitutions, Eq. (28) holds identically on u = curl Psi!
    vec_pot_res = (f_rot - (f_sym - commutator_vec)).applyfunc(sp.simplify)
    if vec_pot_res != sp.zeros(3, 1):
        raise AssertionError(f"Vector potential solenoidal check failed: {vec_pot_res}")

    # Verify the pointwise L^2(T^3) energy density identity (Lemma 1.1 & Theorem 4.1(2) of Supp. 1):
    # 2 * |S(u)|^2 - |omega|^2 == (d_i u_j)(d_j u_i) == d_i(u_j d_j u_i) - u_j d_j(div u).
    grad_u = sp.Matrix(3, 3, lambda i, j: sp.diff(u_sol[j], coords[i]))
    s_mat = sp.Rational(1, 2) * (grad_u + grad_u.T)
    two_s_sq = 2 * sum(s_mat[i, j] ** 2 for i in range(3) for j in range(3))
    omega_sq = omega_sol.dot(omega_sol)

    # Divergence of convective flux div((u . grad) u) = d_i (u_j d_j u_i) when div u = 0
    div_flux = sum(
        sp.diff(sum(u_sol[j] * sp.diff(u_sol[i], coords[j]) for j in range(3)), coords[i])
        for i in range(3)
    )
    energy_density_res = sp.simplify((two_s_sq - omega_sq) - div_flux)
    if energy_density_res != 0:
        raise AssertionError(f"Energy density divergence identity failed: {energy_density_res}")

    return vec_pot_res, energy_density_res


def main() -> int:
    """Execute all symbolic checks for CAS_Proof4_Rotational_Strain_Identity."""
    configure_console_utf8()
    print("=" * 78)
    print(" [CAS_Proof4] Symbolic Verification: Rotational-to-Strain Subgrid Identity")
    print(" Series : 2026 Grand Unified Framework — Part 3 (NS_TZT Model)")
    print("=" * 78)

    lc_mismatches = verify_levi_civita_contraction()
    print(f" [PASS] 1. Levi-Civita 81-Index Contraction Audit : Mismatches = {lc_mismatches}")

    uncon_res, sol_res, core_res = verify_rotational_to_strain_identities()
    print(f" [PASS] 2. Unconstrained 3D Vector Identity       : Residual = {uncon_res.norm()}")
    print(f" [PASS] 3. Solenoidal Bridge Identity Eq. (28)    : Residual = {sol_res.norm()}")
    print(f" [PASS] 4. Interior Homogeneous Core Equivalence  : Residual = {core_res.norm()}")

    vp_res, ed_res = verify_vector_potential_solenoidal_witness()
    print(f" [PASS] 5. Vector Potential Solenoidal Witness    : Residual = {vp_res.norm()}")
    print(f" [PASS] 6. Strain-Vorticity L^2 Divergence Split  : Residual = {ed_res}")

    print("-" * 78)
    print(" [VERIFICATION COMPLETE] All 6 Symbolic Checks in CAS_Proof4 Passed (0 Errors).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())