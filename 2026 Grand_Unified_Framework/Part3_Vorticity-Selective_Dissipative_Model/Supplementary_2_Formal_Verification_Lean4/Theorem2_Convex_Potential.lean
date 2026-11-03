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

import Mathlib.Basic.Real.Basic
import Mathlib.Tactic

namespace Arkhenomia.Part3.Theorem2

/-- Selective eddy viscosity h(s) = C_O \ell^2 s \Phi(s/\Omega_c) is non-negative. -/
theorem selective_viscosity_nonneg (CO l s phi_val : ℝ)
    (hCO : 0 ≤ CO) (hs : 0 ≤ s) (hphi : 0 ≤ phi_val) :
    0 ≤ CO * (l ^ 2) * s * phi_val := by
  positivity

/-- Derivative h'(s) = C_O \ell^2 (\Phi(s/\Omega_c) + (s/\Omega_c)\Phi'(s/\Omega_c)) \ge 0. -/
theorem selective_viscosity_deriv_nonneg (CO l s Ωc phi_val dphi_val : ℝ)
    (hCO : 0 ≤ CO) (hs : 0 ≤ s) (hΩ : 0 < Ωc)
    (hphi : 0 ≤ phi_val) (hdphi : 0 ≤ dphi_val) :
    0 ≤ CO * (l ^ 2) * (phi_val + (s / Ωc) * dphi_val) := by
  positivity

/-- Longitudinal vs. Transverse Eigenvalue Ordering of DV(\omega):
    0 \le \mu_\perp = h(|w|) \le \mu_\parallel = h(|w|) + |w| h'(|w|). -/
theorem hessian_eigenvalue_ordering (h dh_ds w_norm : ℝ)
    (hh : 0 ≤ h) (hdh : 0 ≤ dh_ds) (hw : 0 ≤ w_norm) :
    0 ≤ h ∧ h ≤ h + w_norm * dh_ds := by
  constructor
  · exact hh
  · have h_prod : 0 ≤ w_norm * dh_ds := mul_nonneg hw hdh
    linarith

/-- Main Text Mechanized Excerpt (Lemma 3.3(2) / Proposition 3.1):
    \xi^T DV(\omega) \xi = h |\xi|^2 + (h'/|\omega|)(w \cdot \xi)^2 \ge h |\xi|^2. -/
theorem convex_jacobian_quadratic_form (h dh_ds w_norm ξ_norm w_dot_ξ : ℝ)
    (hh : 0 ≤ h) (hdh : 0 ≤ dh_ds) (hw : 0 < w_norm) :
    h * (ξ_norm ^ 2) ≤ h * (ξ_norm ^ 2) + (dh_ds / w_norm) * (w_dot_ξ ^ 2) := by
  have _ := hh
  have h_extra_nonneg : 0 ≤ (dh_ds / w_norm) * (w_dot_ξ ^ 2) := by
    positivity
  linarith

/-- Non-negativity of the full Hessian quadratic form \xi^T DV(\omega) \xi \ge 0. -/
theorem convex_jacobian_nonneg (h dh_ds w_norm ξ_norm w_dot_ξ : ℝ)
    (hh : 0 ≤ h) (hdh : 0 ≤ dh_ds) (hw : 0 < w_norm) :
    0 ≤ h * (ξ_norm ^ 2) + (dh_ds / w_norm) * (w_dot_ξ ^ 2) := by
  positivity

/-- Lemma 3.4 (Enstrophy-Level Rotational Dissipation Lower Bound):
    \sum_{k=1}^3 (\partial_k \omega)^T DV(\omega) (\partial_k \omega) \ge h(|\omega|) |\nabla \omega|^2. -/
theorem enstrophy_diffusion_coercivity
    (h dh_ds w_norm : ℝ) (g1_sq g2_sq g3_sq dot1 dot2 dot3 : ℝ)
    (hdh : 0 ≤ dh_ds) (hw : 0 < w_norm) :
    h * (g1_sq + g2_sq + g3_sq) ≤
      (h * g1_sq + (dh_ds / w_norm) * (dot1 ^ 2)) +
      (h * g2_sq + (dh_ds / w_norm) * (dot2 ^ 2)) +
      (h * g3_sq + (dh_ds / w_norm) * (dot3 ^ 2)) := by
  have h1 : 0 ≤ (dh_ds / w_norm) * (dot1 ^ 2) := by positivity
  have h2 : 0 ≤ (dh_ds / w_norm) * (dot2 ^ 2) := by positivity
  have h3 : 0 ≤ (dh_ds / w_norm) * (dot3 ^ 2) := by positivity
  linarith

/-- Minty-Browder Monotonicity of V(\omega) = h(|\omega|)\omega (Lemma 3.3(1)):
    For any vectors a, b \in R^3 satisfying Cauchy-Schwarz a \cdot b \le |a||b|,
    non-negative viscosities h_a, h_b \ge 0, and monotone growth
    (h_a - h_b)(|a| - |b|) \ge 0, we have (V(a) - V(b)) \cdot (a - b) \ge 0. -/
theorem minty_browder_radial_monotonicity
    (norm_a norm_b a_dot_b h_a h_b : ℝ)
    (ha : 0 ≤ norm_a) (hb : 0 ≤ norm_b)
    (h_cs : a_dot_b ≤ norm_a * norm_b)
    (hh_a : 0 ≤ h_a) (hh_b : 0 ≤ h_b)
    (h_mono : (h_a - h_b) * (norm_a - norm_b) ≥ 0) :
    h_a * (norm_a ^ 2) - (h_a + h_b) * a_dot_b + h_b * (norm_b ^ 2) ≥ 0 := by
  have _ := hb
  have h_sum_nonneg : 0 ≤ h_a + h_b := add_nonneg hh_a hh_b
  have h_cs_scaled : (h_a + h_b) * a_dot_b ≤ (h_a + h_b) * (norm_a * norm_b) :=
    mul_le_mul_of_nonneg_left h_cs h_sum_nonneg
  have h_decomp :
      h_a * (norm_a ^ 2) - (h_a + h_b) * (norm_a * norm_b) + h_b * (norm_b ^ 2) =
      h_b * ((norm_a - norm_b) ^ 2) + norm_a * ((h_a - h_b) * (norm_a - norm_b)) := by ring
  have h_sq : 0 ≤ h_b * ((norm_a - norm_b) ^ 2) := by positivity
  have h_second : 0 ≤ norm_a * ((h_a - h_b) * (norm_a - norm_b)) := mul_nonneg ha h_mono
  linarith

end Arkhenomia.Part3.Theorem2