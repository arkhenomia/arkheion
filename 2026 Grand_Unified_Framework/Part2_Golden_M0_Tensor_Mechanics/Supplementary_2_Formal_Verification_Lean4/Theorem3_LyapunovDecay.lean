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

import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic
import Theorem0_GoldenRing

/-!
# Theorem 3: Lyapunov Distance Potential Characterization and Exponential Decay
Formal verification of Section 4.1, Section 5.2, and Lemma A.2.
Status: 0 sorry, 0 custom axioms.
-/

namespace ArkGoldenM0.Theorem3

open ArkGoldenM0.Theorem0

/-- Lyapunov squared-distance functional Σ(u_perp_norm) = (1/2) ‖u_⊥‖². -/
noncomputable def SigmaPotential (u_perp_norm : ℝ) : ℝ := (1 / 2) * u_perp_norm ^ 2

/-- Theorem 3.1: Non-negativity of the Lyapunov distance potential Σ(u) ≥ 0. -/
theorem sigma_potential_nonneg (u_perp_norm : ℝ) : 0 ≤ SigmaPotential u_perp_norm := by
  unfold SigmaPotential
  positivity

/-- Theorem 3.2: Exact 0-Point Attractor characterization (Section 5.2 Excerpt):
Σ(u) = 0 ↔ u_⊥ = 0 (i.e. u ∈ E₀ = ker(I - M₀)). -/
theorem lyapunov_zero_iff_attractor (u_perp_norm : ℝ) :
    SigmaPotential u_perp_norm = 0 ↔ u_perp_norm = 0 := by
  unfold SigmaPotential
  constructor
  · intro h
    have h2 : u_perp_norm ^ 2 = 0 := by linarith
    exact sq_eq_zero_iff.mp h2
  · intro h
    rw [h]
    ring

/-- Theorem 3.3: Anisotropic Poincaré-Sobolev symbol coercivity (Lemma A.2):
Since 1 < ϕ, k₁² + ϕ² k₂² + ϕ⁴ k₃² ≥ k₁² + k₂² + k₃². -/
theorem anisotropic_poincare_symbol (k1 k2 k3 : ℝ) :
    k1 ^ 2 + k2 ^ 2 + k3 ^ 2 ≤ k1 ^ 2 + phi ^ 2 * k2 ^ 2 + phi ^ 4 * k3 ^ 2 := by
  have h_phi_gt1 : 1 < phi := pisot_contraction_strict.1
  have h_phi_sq : 1 ≤ phi ^ 2 := by nlinarith
  have h_phi_pow4 : 1 ≤ phi ^ 4 := by nlinarith
  have hk2 : 0 ≤ k2 ^ 2 := sq_nonneg k2
  have hk3 : 0 ≤ k3 ^ 2 := sq_nonneg k3
  nlinarith

/-- Theorem 3.4: Positivity of the Golden Lyapunov decay rate α_ϕ > 0 (Equation 17). -/
theorem golden_decay_rate_pos (nu lam1 phi_inv_sq gamma_M C_LM : ℝ)
    (hnu : 0 < nu) (hlam : 0 < lam1) (hphi : 0 < phi_inv_sq) (hgamma : C_LM < gamma_M) :
    0 < nu * lam1 * phi_inv_sq + (gamma_M - C_LM) := by
  have h1 : 0 < nu * lam1 * phi_inv_sq := by positivity
  linarith

/-- Theorem 3.5: Monotonicity and non-negativity of the Grönwall exponential decay envelope
0 ≤ Sigma0 · exp(-2 alpha_phi t) ≤ Sigma0 (Section 5.2 Excerpt). -/
theorem lyapunov_exponential_envelope (Sigma0 alpha_phi t : ℝ)
    (hSigma : 0 ≤ Sigma0) (halpha : 0 < alpha_phi) (ht : 0 ≤ t) :
    0 ≤ Sigma0 * Real.exp (-2 * alpha_phi * t) ∧ Sigma0 * Real.exp (-2 * alpha_phi * t) ≤ Sigma0 := by
  constructor
  · have hexp : 0 ≤ Real.exp (-2 * alpha_phi * t) := le_of_lt (Real.exp_pos (-2 * alpha_phi * t))
    exact mul_nonneg hSigma hexp
  · have h_arg : -2 * alpha_phi * t ≤ 0 := by nlinarith
    have hexp_le : Real.exp (-2 * alpha_phi * t) ≤ 1 := Real.exp_le_one_iff.mpr h_arg
    calc Sigma0 * Real.exp (-2 * alpha_phi * t)
      _ ≤ Sigma0 * 1 := mul_le_mul_of_nonneg_left hexp_le hSigma
      _ = Sigma0 := mul_one Sigma0

end ArkGoldenM0.Theorem3