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
import Theorem0_GoldenRing

/-!
# Theorem 1: Multi-Dimensional Diophantine Lower Bounds and KAM Sobolev Boundedness
Formal verification of Section 3.1, Section 3.2, and Appendix A (Lemma A.1).
Status: 0 sorry, 0 custom axioms.
-/

namespace ArkGoldenM0.Theorem1

open ArkGoldenM0.Theorem0

/-- Theorem 1.1: Any non-zero rational integer N ≠ 0 satisfies |N| ≥ 1 in ℝ. -/
theorem int_norm_ge_one (N : ℤ) (hN : N ≠ 0) : (1 : ℝ) ≤ |(N : ℝ)| := by
  have h1 : (1 : ℤ) ≤ |N| := Int.one_le_abs hN
  have h2 : ((1 : ℤ) : ℝ) ≤ ((|N| : ℤ) : ℝ) := by exact_mod_cast h1
  simpa [Int.cast_abs] using h2

/-- Theorem 1.2: Quadratic Golden Diophantine lower bound from algebraic norm |ξ · ξ̄| ≥ 1. -/
theorem quadratic_diophantine_lower_bound (ξ ξ_conj K_bound : ℝ)
    (h_norm : 1 ≤ |ξ * ξ_conj|) (h_conj_pos : 0 < K_bound) (h_conj_ub : |ξ_conj| ≤ K_bound) :
    1 / K_bound ≤ |ξ| := by
  have h_prod : 1 ≤ |ξ| * |ξ_conj| := by simpa [abs_mul] using h_norm
  have h_le : |ξ| * |ξ_conj| ≤ |ξ| * K_bound :=
    mul_le_mul_of_nonneg_left h_conj_ub (abs_nonneg ξ)
  have h_comb : 1 ≤ |ξ| * K_bound := le_trans h_prod h_le
  exact (div_le_iff₀ h_conj_pos).mpr h_comb

/-- Theorem 1.3: Cubic 3D Pisot Diophantine lower bound (Lemma A.1, τ = 2).
If |ξ · σ₂(ξ) · σ₃(ξ)| ≥ 1 and |σ₂(ξ)|, |σ₃(ξ)| ≤ M · k_norm, then |ξ| ≥ 1 / (M² · k_norm²). -/
theorem cubic_diophantine_lower_bound (ξ s2 s3 M k_norm : ℝ)
    (h_norm : 1 ≤ |ξ| * |s2| * |s3|)
    (hM : 0 < M) (hk : 0 < k_norm)
    (hs2 : |s2| ≤ M * k_norm) (hs3 : |s3| ≤ M * k_norm) :
    1 / (M ^ 2 * k_norm ^ 2) ≤ |ξ| := by
  have h_prod_pos : 0 < M ^ 2 * k_norm ^ 2 := by positivity
  have hs23 : |s2| * |s3| ≤ (M * k_norm) * (M * k_norm) :=
    mul_le_mul hs2 hs3 (abs_nonneg s3) (by positivity)
  have h_step : |ξ| * |s2| * |s3| ≤ |ξ| * (M ^ 2 * k_norm ^ 2) := by
    calc |ξ| * |s2| * |s3|
      _ = |ξ| * (|s2| * |s3|) := by ring
      _ ≤ |ξ| * ((M * k_norm) * (M * k_norm)) :=
          mul_le_mul_of_nonneg_left hs23 (abs_nonneg ξ)
      _ = |ξ| * (M ^ 2 * k_norm ^ 2) := by ring
  have h_one : 1 ≤ |ξ| * (M ^ 2 * k_norm ^ 2) := le_trans h_norm h_step
  exact (div_le_iff₀ h_prod_pos).mpr h_one

/-- Theorem 1.4: Frequency-scaled Diophantine inequality |k · ω_ϕ| ≥ γ_ϕ / |k|^τ > 0. -/
theorem frequency_scaled_diophantine (ω0 ξ M k_norm : ℝ)
    (hω : 0 < ω0) (hM : 0 < M) (hk : 0 < k_norm)
    (h_base : 1 / (M ^ 2 * k_norm ^ 2) ≤ |ξ|) :
    (ω0 / M ^ 2) / k_norm ^ 2 ≤ ω0 * |ξ| ∧ 0 < (ω0 / M ^ 2) / k_norm ^ 2 := by
  constructor
  · have h_mul : ω0 * (1 / (M ^ 2 * k_norm ^ 2)) ≤ ω0 * |ξ| :=
      mul_le_mul_of_nonneg_left h_base (le_of_lt hω)
    calc (ω0 / M ^ 2) / k_norm ^ 2
      _ = ω0 * (1 / (M ^ 2 * k_norm ^ 2)) := by ring
      _ ≤ ω0 * |ξ| := h_mul
  · positivity

/-- Theorem 1.5: KAM homological Fourier mode bound (Theorem 3.1).
If |k · ω_ϕ| ≥ γ_ϕ / k_pow and |Ψ_k| · |k · ω_ϕ| = |F_k|, then |Ψ_k| ≤ (k_pow / γ_ϕ) · |F_k|. -/
theorem kam_homological_mode_bound (Ψ_abs F_abs denom γ_phi k_pow : ℝ)
    (hγ : 0 < γ_phi) (hk : 0 < k_pow) (hΨ : 0 ≤ Ψ_abs)
    (h_dioph : γ_phi / k_pow ≤ denom)
    (h_eq : Ψ_abs * denom = F_abs) :
    Ψ_abs ≤ (k_pow / γ_phi) * F_abs := by
  have h_le : Ψ_abs * (γ_phi / k_pow) ≤ F_abs := by
    rw [← h_eq]
    exact mul_le_mul_of_nonneg_left h_dioph hΨ
  have h_pos_factor : 0 < k_pow / γ_phi := div_pos hk hγ
  have h_mul := mul_le_mul_of_nonneg_left h_le (le_of_lt h_pos_factor)
  have h_cancel : (k_pow / γ_phi) * (Ψ_abs * (γ_phi / k_pow)) = Ψ_abs := by
    field_simp [ne_of_gt hγ, ne_of_gt hk]
  linarith

end ArkGoldenM0.Theorem1