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

namespace Arkhenomia.Part3.Theorem3

/-- If 0 \le a \le b, then a^3 \le b^3. -/
lemma cube_le_cube_of_nonneg (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b) :
    a ^ 3 ≤ b ^ 3 := by
  have h_diff : b ^ 3 - a ^ 3 = (b - a) * (b ^ 2 + b * a + a ^ 2) := by ring
  have h_ba : 0 ≤ b - a := by linarith
  have h_hb : 0 ≤ b := by linarith
  have h_quad : 0 ≤ b ^ 2 + b * a + a ^ 2 := by positivity
  have h_prod : 0 ≤ (b - a) * (b ^ 2 + b * a + a ^ 2) := mul_nonneg h_ba h_quad
  linarith

/-- Normalized Three-Zone Cubic Threshold Coercivity (Lemma 3.3(3) / Proposition 3.2):
    For any vorticity magnitude s \ge 0, threshold \Omega_c > 0, and smooth cutoff
    switch \Phi : R \to [0, 1] satisfying \Phi(r) = 1 for all r \ge 2,
    s^3 \le \Phi(s/\Omega_c) s^3 + 8 \Omega_c^3. -/
theorem cubic_threshold_coercivity (s Ωc : ℝ) (Phi : ℝ → ℝ)
    (hs : 0 ≤ s) (hΩ : 0 < Ωc)
    (h_range : ∀ r, 0 ≤ Phi r ∧ Phi r ≤ 1)
    (h_sat : ∀ r, 2 ≤ r → Phi r = 1) :
    s ^ 3 ≤ Phi (s / Ωc) * (s ^ 3) + 8 * (Ωc ^ 3) := by
  rcases le_or_gt (2 * Ωc) s with h_zone | h_zone
  · -- Zone III: Supercritical Active Core (s \ge 2 \Omega_c \implies s / \Omega_c \ge 2)
    have h_ratio : 2 ≤ s / Ωc := by
      rw [le_div_iff₀ hΩ]
      linarith
    have h_phi_one : Phi (s / Ωc) = 1 := h_sat (s / Ωc) h_ratio
    rw [h_phi_one]
    have h_eight_pos : 0 ≤ 8 * (Ωc ^ 3) := by positivity
    linarith
  · -- Zones I & II: Subcritical & Transition Shell (0 \le s < 2 \Omega_c)
    have h_le_two : s ≤ 2 * Ωc := le_of_lt h_zone
    have h_cube : s ^ 3 ≤ (2 * Ωc) ^ 3 := cube_le_cube_of_nonneg s (2 * Ωc) hs h_le_two
    have h_eight : (2 * Ωc) ^ 3 = 8 * (Ωc ^ 3) := by ring
    have h_phi_nonneg : 0 ≤ Phi (s / Ωc) := (h_range (s / Ωc)).1
    have h_s3_nonneg : 0 ≤ s ^ 3 := by positivity
    have h_prod_nonneg : 0 ≤ Phi (s / Ωc) * (s ^ 3) := mul_nonneg h_phi_nonneg h_s3_nonneg
    linarith

/-- Pointwise rotational flux coercivity (Equation (11) of Part 3):
    V(\omega) \cdot \omega = C_O \ell^2 \Phi(|\omega|/\Omega_c) |\omega|^3
      \ge C_O \ell^2 (|\omega|^3 - 8 \Omega_c^3). -/
theorem rotational_flux_cubic_lower_bound (CO l s Ωc : ℝ) (Phi : ℝ → ℝ)
    (hCO : 0 < CO) (hl : 0 < l) (hs : 0 ≤ s) (hΩ : 0 < Ωc)
    (h_range : ∀ r, 0 ≤ Phi r ∧ Phi r ≤ 1)
    (h_sat : ∀ r, 2 ≤ r → Phi r = 1) :
    CO * (l ^ 2) * (s ^ 3 - 8 * (Ωc ^ 3)) ≤
      CO * (l ^ 2) * Phi (s / Ωc) * (s ^ 3) := by
  have _ := hl
  have h_base := cubic_threshold_coercivity s Ωc Phi hs hΩ h_range h_sat
  have h_coeff_pos : 0 ≤ CO * (l ^ 2) := by positivity
  have h_rearr : s ^ 3 - 8 * (Ωc ^ 3) ≤ Phi (s / Ωc) * (s ^ 3) := by linarith
  have h_mul := mul_le_mul_of_nonneg_left h_rearr h_coeff_pos
  linarith

/-- Step 2 of Theorem 4.1 (Unconditional Space-Time L^3 Vorticity Bound, Eq. (20)):
    L3_int \le \mathcal{E}(t) / (C_O \ell^2) + 8 \Omega_c^3 Vol t. -/
theorem spacetime_L3_vorticity_bound
    (L3_int Phi_L3_int E_t CO l_sq Ωc Vol t : ℝ)
    (h_CO_pos : 0 < CO * l_sq)
    (h_coercive_int : L3_int ≤ Phi_L3_int + 8 * (Ωc ^ 3) * Vol * t)
    (h_energy_diss : (CO * l_sq) * Phi_L3_int ≤ E_t) :
    L3_int ≤ E_t / (CO * l_sq) + 8 * (Ωc ^ 3) * Vol * t := by
  have h_div : Phi_L3_int ≤ E_t / (CO * l_sq) := by
    rw [le_div_iff₀ h_CO_pos]
    linarith
  linarith

end Arkhenomia.Part3.Theorem3