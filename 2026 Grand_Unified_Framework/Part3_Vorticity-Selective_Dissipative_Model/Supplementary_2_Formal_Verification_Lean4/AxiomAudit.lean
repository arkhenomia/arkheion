-- SPDX-FileCopyrightText: 2026 Jung Soo Kim (Arkhenomia Institute) <https://orcid.org/0009-0006-5140-0604>
-- SPDX-License-Identifier: CC-BY-NC-4.0 AND LicenseRef-Arkhenomia-Governance-v2.2.0
/-
================================================================================
Author & Institute: Jung Soo Kim (ORCID: 0009-0006-5140-0604) / Arkhenomia Institute
License           : CC BY-NC 4.0 (Commercial licensing administered by Arkhenetics; see LICENSE.txt)
Canonical Repo    : https://github.com/arkhenomia/arkheion
Dataset Archive   : https://huggingface.co/datasets/arkhenomia/arkheion
Official Websites : https://arkhenomia.org | https://arkhenetics.com
--------------------------------------------------------------------------------
Commercial use, corporate R&D, in-house enterprise deployment, AI knowledge
distillation, surrogate model training, automated scraping/corpus ingestion,
OS kernel/hardware/firmware porting (ZINN / Ark-ZPF), network state-index
synchronization/congestion-control protocol implementation, and high-risk or
non-peaceful applications are strictly prohibited without a separate written
commercial license agreement executed with the Author or Arkhenetics. All
patent rights are expressly reserved; no patent or commercial rights are
granted by implication. Governed by the latest LICENSE.txt (Policy v2.2.0+).
================================================================================
-/

import Theorem0_Basic_Operators
import Theorem1_Gyroscopic_Neutrality
import Theorem2_Convex_Potential
import Theorem3_Cubic_Coercivity
import Theorem4_Rotational_Identity
import Theorem5_Monotone_Uniqueness
import Theorem6_GronwallFree_Enstrophy

-- ============================================================================
-- Module 0: Theorem0_Basic_Operators (All 9 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem0.normSq_nonneg
#print axioms Arkhenomia.Part3.Theorem0.dot_comm
#print axioms Arkhenomia.Part3.Theorem0.cross_anticomm
#print axioms Arkhenomia.Part3.Theorem0.lagrange_cross_identity
#print axioms Arkhenomia.Part3.Theorem0.solenoidal_fourier_curl_isometry
#print axioms Arkhenomia.Part3.Theorem0.laminar_shielding_viscosity_zero
#print axioms Arkhenomia.Part3.Theorem0.supercritical_core_viscosity_exact
#print axioms Arkhenomia.Part3.Theorem0.div_curl_symbol_zero
#print axioms Arkhenomia.Part3.Theorem0.div_Fdiss_mixed_partials_zero

-- ============================================================================
-- Module 1: Theorem1_Gyroscopic_Neutrality (All 7 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem1.normSq_nonneg
#print axioms Arkhenomia.Part3.Theorem1.cross_dot_self_right
#print axioms Arkhenomia.Part3.Theorem1.cross_dot_self_left
#print axioms Arkhenomia.Part3.Theorem1.gyroscopic_pointwise_neutrality
#print axioms Arkhenomia.Part3.Theorem1.regularized_axis_normSq_lt_one
#print axioms Arkhenomia.Part3.Theorem1.gyroscopic_pointwise_normSq_bound
#print axioms Arkhenomia.Part3.Theorem1.global_L2_gyroscopic_energy_neutrality

-- ============================================================================
-- Module 2: Theorem2_Convex_Potential (All 7 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem2.selective_viscosity_nonneg
#print axioms Arkhenomia.Part3.Theorem2.selective_viscosity_deriv_nonneg
#print axioms Arkhenomia.Part3.Theorem2.hessian_eigenvalue_ordering
#print axioms Arkhenomia.Part3.Theorem2.convex_jacobian_quadratic_form
#print axioms Arkhenomia.Part3.Theorem2.convex_jacobian_nonneg
#print axioms Arkhenomia.Part3.Theorem2.enstrophy_diffusion_coercivity
#print axioms Arkhenomia.Part3.Theorem2.minty_browder_radial_monotonicity

-- ============================================================================
-- Module 3: Theorem3_Cubic_Coercivity (All 4 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem3.cube_le_cube_of_nonneg
#print axioms Arkhenomia.Part3.Theorem3.cubic_threshold_coercivity
#print axioms Arkhenomia.Part3.Theorem3.rotational_flux_cubic_lower_bound
#print axioms Arkhenomia.Part3.Theorem3.spacetime_L3_vorticity_bound

-- ============================================================================
-- Module 4: Theorem4_Rotational_Identity (All 5 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem4.vorticity_divergence_zero_jet
#print axioms Arkhenomia.Part3.Theorem4.rotational_strain_unconstrained_identity
#print axioms Arkhenomia.Part3.Theorem4.rotational_to_strain_solenoidal_identity
#print axioms Arkhenomia.Part3.Theorem4.interior_core_equivalence
#print axioms Arkhenomia.Part3.Theorem4.rotational_dissipation_energy_nonpos

-- ============================================================================
-- Module 5: Theorem5_Monotone_Uniqueness (All 6 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem5.L_beta_eps_pos
#print axioms Arkhenomia.Part3.Theorem5.gated_axis_lipschitz_bound
#print axioms Arkhenomia.Part3.Theorem5.gyroscopic_difference_inner_reduction
#print axioms Arkhenomia.Part3.Theorem5.young_gyroscopic_absorption
#print axioms Arkhenomia.Part3.Theorem5.uniqueness_energy_differential_inequality
#print axioms Arkhenomia.Part3.Theorem5.uniqueness_zero_difference_of_equal_initial

-- ============================================================================
-- Module 6: Theorem6_GronwallFree_Enstrophy (All 5 Theorems Audited)
-- ============================================================================
#print axioms Arkhenomia.Part3.Theorem6.linear_forcing_young_bound
#print axioms Arkhenomia.Part3.Theorem6.gronwall_free_enstrophy_bound
#print axioms Arkhenomia.Part3.Theorem6.unconditional_global_enstrophy_closure
#print axioms Arkhenomia.Part3.Theorem6.vanishing_filter_weak_pairing_bound
#print axioms Arkhenomia.Part3.Theorem6.taylor_green_nontrivial_shielded_witness