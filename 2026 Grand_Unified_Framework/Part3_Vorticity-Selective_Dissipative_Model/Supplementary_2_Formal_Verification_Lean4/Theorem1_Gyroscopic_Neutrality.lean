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

namespace Arkhenomia.Part3.Theorem1

/-- Three-dimensional vector structure on T^3. -/
@[ext]
structure Vec3 where
  x : ℝ
  y : ℝ
  z : ℝ

/-- Scalar multiplication on Vec3. -/
def smul (c : ℝ) (u : Vec3) : Vec3 :=
  ⟨c * u.x, c * u.y, c * u.z⟩

/-- Euclidean dot product on Vec3. -/
def dot (u v : Vec3) : ℝ :=
  u.x * v.x + u.y * v.y + u.z * v.z

/-- Squared Euclidean norm on Vec3. -/
def normSq (u : Vec3) : ℝ :=
  dot u u

/-- Euclidean cross product on Vec3. -/
def cross (u v : Vec3) : Vec3 :=
  ⟨u.y * v.z - u.z * v.y,
   u.z * v.x - u.x * v.z,
   u.x * v.y - u.y * v.x⟩

/-- Squared norm is non-negative for every vector v \in R^3. -/
lemma normSq_nonneg (v : Vec3) : 0 ≤ normSq v := by
  unfold normSq dot
  nlinarith [mul_self_nonneg v.x, mul_self_nonneg v.y, mul_self_nonneg v.z]

/-- Elementary vector triple product orthogonality: (u \times w) \cdot u = 0. -/
theorem cross_dot_self_right (u w : Vec3) :
    dot (cross u w) u = 0 := by
  unfold dot cross
  ring

/-- Elementary vector triple product orthogonality: (u \times w) \cdot w = 0. -/
theorem cross_dot_self_left (u w : Vec3) :
    dot (cross u w) w = 0 := by
  unfold dot cross
  ring

/-- Main Text Mechanized Excerpt (Lemma 3.1 / Proposition 2.1):
    Pointwise orthogonality of G(u, \omega) = \Phi(|\omega|/\Omega_c) (u \times \hat{\omega}_\varepsilon)
    against the velocity vector u. -/
theorem gyroscopic_pointwise_neutrality (u w_hat : Vec3) (phi_val : ℝ) :
    dot (smul phi_val (cross u w_hat)) u = 0 := by
  unfold dot smul cross
  ring

/-- Regularized vorticity direction squared norm bound:
    |\hat{\omega}_\varepsilon|^2 = |\omega|^2 / (|\omega|^2 + \varepsilon^2) < 1. -/
theorem regularized_axis_normSq_lt_one (w_sq ε : ℝ)
    (hw : 0 ≤ w_sq) (hε : 0 < ε) :
    w_sq / (w_sq + ε ^ 2) < 1 ∧ w_sq / (w_sq + ε ^ 2) ≤ 1 := by
  have h_pos : 0 < w_sq + ε ^ 2 := by positivity
  have h_lt : w_sq / (w_sq + ε ^ 2) < 1 := by
    rw [div_lt_iff₀ h_pos]
    have hε2 : 0 < ε ^ 2 := sq_pos_of_pos hε
    linarith
  exact ⟨h_lt, le_of_lt h_lt⟩

/-- Pointwise norm contraction of the gyroscopic vector G(u, \omega):
    Whenever |\hat{\omega}_\varepsilon|^2 \le 1 and 0 \le \Phi \le 1,
    |G(u, \omega)|^2 = |\Phi (u \times \hat{\omega}_\varepsilon)|^2 \le |u|^2. -/
theorem gyroscopic_pointwise_normSq_bound (u w_hat : Vec3) (phi_val : ℝ)
    (h_phi_nonneg : 0 ≤ phi_val) (h_phi_le_one : phi_val ≤ 1)
    (h_axis_unit : normSq w_hat ≤ 1) :
    normSq (smul phi_val (cross u w_hat)) ≤ normSq u := by
  have h_lagrange : normSq (cross u w_hat) + (dot u w_hat) ^ 2 = normSq u * normSq w_hat := by
    unfold normSq dot cross
    ring
  have h_cross_le : normSq (cross u w_hat) ≤ normSq u * normSq w_hat := by
    have h_sq : 0 ≤ (dot u w_hat) ^ 2 := sq_nonneg (dot u w_hat)
    linarith
  have h_u_nonneg : 0 ≤ normSq u := normSq_nonneg u
  have h_prod_le : normSq u * normSq w_hat ≤ normSq u := by
    nlinarith
  have h_smul_eq : normSq (smul phi_val (cross u w_hat)) = (phi_val ^ 2) * normSq (cross u w_hat) := by
    unfold normSq dot smul
    ring
  have h_phi_sq_le_one : phi_val ^ 2 ≤ 1 := by
    nlinarith
  have h_cross_nonneg : 0 ≤ normSq (cross u w_hat) := normSq_nonneg (cross u w_hat)
  rw [h_smul_eq]
  nlinarith

/-- Global L^2(T^3) Kinetic Energy Neutrality under Self-Adjoint Leray Projection:
    \langle F_axis(u, \omega), u \rangle_{L^2} = 0 whenever P u = u and \langle G, u \rangle_{L^2} = 0. -/
theorem global_L2_gyroscopic_energy_neutrality
    {H : Type*} (inner_L2 : H → H → ℝ) (smul_H : ℝ → H → H) (P_Leray : H → H)
    (u G : H) (c_X Ω_c : ℝ)
    (h_lin_left : ∀ (a : ℝ) (x y : H), inner_L2 (smul_H a x) y = a * inner_L2 x y)
    (h_P_self_adj : ∀ x y : H, inner_L2 (P_Leray x) y = inner_L2 x (P_Leray y))
    (h_u_solenoidal : P_Leray u = u)
    (h_pointwise_int_zero : inner_L2 G u = 0) :
    inner_L2 (smul_H (c_X * Ω_c) (P_Leray G)) u = 0 := by
  rw [h_lin_left, h_P_self_adj, h_u_solenoidal, h_pointwise_int_zero]
  ring

end Arkhenomia.Part3.Theorem1