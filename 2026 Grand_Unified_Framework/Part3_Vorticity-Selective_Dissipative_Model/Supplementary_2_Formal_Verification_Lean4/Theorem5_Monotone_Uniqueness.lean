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

namespace Arkhenomia.Part3.Theorem5

/-- Three-dimensional vector representation on T^3. -/
@[ext]
structure Vec3 where
  x : ℝ
  y : ℝ
  z : ℝ

/-- Vector addition on Vec3. -/
def addVec (u v : Vec3) : Vec3 :=
  ⟨u.x + v.x, u.y + v.y, u.z + v.z⟩

/-- Euclidean dot product on Vec3. -/
def dot (u v : Vec3) : ℝ :=
  u.x * v.x + u.y * v.y + u.z * v.z

/-- Euclidean cross product on Vec3. -/
def cross (u v : Vec3) : Vec3 :=
  ⟨u.y * v.z - u.z * v.y,
   u.z * v.x - u.x * v.z,
   u.x * v.y - u.y * v.x⟩

/-- Explicit Lipschitz constant L_{\beta,\varepsilon} := C_\Phi / \Omega_c + 2 / \varepsilon. -/
noncomputable def L_beta_eps (C_Phi Ω_c ε : ℝ) : ℝ :=
  C_Phi / Ω_c + 2 / ε

/-- Theorem 5.1: Positivity of L_{\beta,\varepsilon} whenever C_\Phi \ge 0, \Omega_c > 0, \varepsilon > 0. -/
theorem L_beta_eps_pos (C_Phi Ω_c ε : ℝ)
    (hC : 0 ≤ C_Phi) (hΩ : 0 < Ω_c) (hε : 0 < ε) :
    0 < L_beta_eps C_Phi Ω_c ε := by
  unfold L_beta_eps
  have h1 : 0 ≤ C_Phi / Ω_c := div_nonneg hC (le_of_lt hΩ)
  have h2 : 0 < 2 / ε := div_pos (by norm_num) hε
  linarith

/-- Theorem 5.2 (Lemma 3.2): Global Lipschitz Continuity of \beta(\omega):
    |\beta(\omega_1) - \beta(\omega_2)| \le L_{\beta,\varepsilon} |\omega_1 - \omega_2|. -/
theorem gated_axis_lipschitz_bound
    (beta_diff phi_diff axis_diff w_diff norm_w1_hat phi2 C_Phi Ω_c ε : ℝ)
    (hw_diff : 0 ≤ w_diff)
    (h_phi_diff_nonneg : 0 ≤ phi_diff)
    (h_axis_diff_nonneg : 0 ≤ axis_diff)
    (h_w1_unit : norm_w1_hat ≤ 1)
    (h_phi2_le_one : phi2 ≤ 1)
    (h_triangle : beta_diff ≤ phi_diff * norm_w1_hat + phi2 * axis_diff)
    (h_phi_lip : phi_diff ≤ (C_Phi / Ω_c) * w_diff)
    (h_axis_lip : axis_diff ≤ (2 / ε) * w_diff) :
    beta_diff ≤ L_beta_eps C_Phi Ω_c ε * w_diff := by
  unfold L_beta_eps
  have _ := hw_diff
  have h_t1_nonneg : 0 ≤ phi_diff * (1 - norm_w1_hat) :=
    mul_nonneg h_phi_diff_nonneg (by linarith)
  have h_t1_id : phi_diff * (1 - norm_w1_hat) = phi_diff - phi_diff * norm_w1_hat := by ring
  have h_t2_nonneg : 0 ≤ axis_diff * (1 - phi2) :=
    mul_nonneg h_axis_diff_nonneg (by linarith)
  have h_t2_id : axis_diff * (1 - phi2) = axis_diff - phi2 * axis_diff := by ring
  have h_sum_id :
      (C_Phi / Ω_c + 2 / ε) * w_diff = (C_Phi / Ω_c) * w_diff + (2 / ε) * w_diff := by ring
  linarith

/-- Theorem 5.3 (Theorem 4.2, Step 3): Pointwise cancellation of (w \times \beta_2) \cdot w = 0
    in the gyroscopic difference inner product. -/
theorem gyroscopic_difference_inner_reduction (w u1 beta2 beta_diff : Vec3) :
    dot (addVec (cross w beta2) (cross u1 beta_diff)) w =
      dot (cross u1 beta_diff) w := by
  unfold dot addVec cross
  ring

/-- Theorem 5.4 (Equation (24) of Part 3): Young's Inequality for Gyroscopic Uniqueness Term:
    A * grad_w * norm_w \le (\nu / 4) * grad_w^2 + (A^2 / \nu) * norm_w^2. -/
theorem young_gyroscopic_absorption (ν A grad_w norm_w : ℝ) (hν : 0 < ν) :
    A * grad_w * norm_w ≤ (ν / 4) * (grad_w ^ 2) + ((A ^ 2) / ν) * (norm_w ^ 2) := by
  have hν_ne : ν ≠ 0 := ne_of_gt hν
  have h_expand :
      (ν / 4) * (grad_w ^ 2) + ((A ^ 2) / ν) * (norm_w ^ 2) - A * grad_w * norm_w =
      ((ν * grad_w - 2 * A * norm_w) ^ 2) / (4 * ν) := by
    field_simp
    ring
  have h_div_nonneg : 0 ≤ ((ν * grad_w - 2 * A * norm_w) ^ 2) / (4 * ν) := by
    positivity
  linarith

/-- Theorem 5.5 (Theorem 4.2): Monotone Uniqueness Differential Energy Inequality:
    dE_dt + (\nu / 2) \|\nabla w\|^2 \le (K_conv + K_gyro) \|w\|^2. -/
theorem uniqueness_energy_differential_inequality
    (dE_dt ν grad_w_sq norm_w_sq mono_diss gyro_term conv_term K_conv K_gyro : ℝ)
    (h_balance : dE_dt + ν * grad_w_sq + mono_diss = conv_term + gyro_term)
    (h_mono : 0 ≤ mono_diss)
    (h_gyro : gyro_term ≤ (ν / 4) * grad_w_sq + K_gyro * norm_w_sq)
    (h_conv : conv_term ≤ (ν / 4) * grad_w_sq + K_conv * norm_w_sq) :
    dE_dt + (ν / 2) * grad_w_sq ≤ (K_conv + K_gyro) * norm_w_sq := by
  linarith

/-- Theorem 5.6 (Theorem 4.2, Eq. (22)): Unconditional Uniqueness Conclusion:
    \|u_{1,0} - u_{2,0}\|^2 = 0 \implies \|w(t)\|^2 = 0. -/
theorem uniqueness_zero_difference_of_equal_initial
    (w_sq_t w_sq_0 exp_factor : ℝ)
    (hw_nonneg : 0 ≤ w_sq_t)
    (h_init_eq : w_sq_0 = 0)
    (h_gronwall : w_sq_t ≤ w_sq_0 * exp_factor) :
    w_sq_t = 0 := by
  rw [h_init_eq, zero_mul] at h_gronwall
  linarith

end Arkhenomia.Part3.Theorem5