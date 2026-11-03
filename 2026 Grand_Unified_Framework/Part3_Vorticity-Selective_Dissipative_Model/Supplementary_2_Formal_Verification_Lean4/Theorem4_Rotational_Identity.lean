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

namespace Arkhenomia.Part3.Theorem4

/-- Three-dimensional vector representation on T^3. -/
@[ext]
structure Vec3 where
  x : ℝ
  y : ℝ
  z : ℝ

/-- Vector subtraction on Vec3. -/
def subVec (u v : Vec3) : Vec3 :=
  ⟨u.x - v.x, u.y - v.y, u.z - v.z⟩

/-- Scalar multiplication on Vec3. -/
def smul (c : ℝ) (u : Vec3) : Vec3 :=
  ⟨c * u.x, c * u.y, c * u.z⟩

/-- Pointwise 2-jet of a smooth velocity field u = (u_x, u_y, u_z) and 1-jet
    of a spatially varying scalar eddy viscosity \nu_t on T^3. -/
structure VelocityViscosityJet where
  nu_t  : ℝ
  dnu_x : ℝ
  dnu_y : ℝ
  dnu_z : ℝ
  dux_x : ℝ
  dux_y : ℝ
  dux_z : ℝ
  duy_x : ℝ
  duy_y : ℝ
  duy_z : ℝ
  duz_x : ℝ
  duz_y : ℝ
  duz_z : ℝ
  d2ux_xx : ℝ
  d2ux_yy : ℝ
  d2ux_zz : ℝ
  d2ux_xy : ℝ
  d2ux_xz : ℝ
  d2ux_yz : ℝ
  d2uy_xx : ℝ
  d2uy_yy : ℝ
  d2uy_zz : ℝ
  d2uy_xy : ℝ
  d2uy_xz : ℝ
  d2uy_yz : ℝ
  d2uz_xx : ℝ
  d2uz_yy : ℝ
  d2uz_zz : ℝ
  d2uz_xy : ℝ
  d2uz_xz : ℝ
  d2uz_yz : ℝ

/-- Vorticity vector \omega = \nabla \times u on the jet space. -/
def omegaVec (J : VelocityViscosityJet) : Vec3 :=
  ⟨J.duz_y - J.duy_z,
   J.dux_z - J.duz_x,
   J.duy_x - J.dux_y⟩

/-- First-order spatial derivatives of vorticity \partial_j \omega_k. -/
def d_omega_x_dx (J : VelocityViscosityJet) : ℝ := J.d2uz_xy - J.d2uy_xz
def d_omega_x_dy (J : VelocityViscosityJet) : ℝ := J.d2uz_yy - J.d2uy_yz
def d_omega_x_dz (J : VelocityViscosityJet) : ℝ := J.d2uz_yz - J.d2uy_zz
def d_omega_y_dx (J : VelocityViscosityJet) : ℝ := J.d2ux_xz - J.d2uz_xx
def d_omega_y_dy (J : VelocityViscosityJet) : ℝ := J.d2ux_yz - J.d2uz_xy
def d_omega_y_dz (J : VelocityViscosityJet) : ℝ := J.d2ux_zz - J.d2uz_xz
def d_omega_z_dx (J : VelocityViscosityJet) : ℝ := J.d2uy_xx - J.d2ux_xy
def d_omega_z_dy (J : VelocityViscosityJet) : ℝ := J.d2uy_xy - J.d2ux_yy
def d_omega_z_dz (J : VelocityViscosityJet) : ℝ := J.d2uy_xz - J.d2ux_yz

/-- Rotational selective dissipation operator F_rot := -\nabla \times (\nu_t \omega). -/
def neg_curl_nut_omega (J : VelocityViscosityJet) : Vec3 :=
  let w := omegaVec J
  ⟨-(J.dnu_y * w.z + J.nu_t * d_omega_z_dy J - (J.dnu_z * w.y + J.nu_t * d_omega_y_dz J)),
   -(J.dnu_z * w.x + J.nu_t * d_omega_x_dz J - (J.dnu_x * w.z + J.nu_t * d_omega_z_dx J)),
   -(J.dnu_x * w.y + J.nu_t * d_omega_y_dx J - (J.dnu_y * w.x + J.nu_t * d_omega_x_dy J))⟩

/-- Symmetric strain divergence operator F_sym := \nabla \cdot (2 \nu_t S(u)). -/
def div_two_nut_S (J : VelocityViscosityJet) : Vec3 :=
  ⟨J.dnu_x * (J.dux_x + J.dux_x) + J.nu_t * (J.d2ux_xx + J.d2ux_xx) +
   J.dnu_y * (J.dux_y + J.duy_x) + J.nu_t * (J.d2ux_yy + J.d2uy_xy) +
   J.dnu_z * (J.dux_z + J.duz_x) + J.nu_t * (J.d2ux_zz + J.d2uz_xz),

   J.dnu_x * (J.duy_x + J.dux_y) + J.nu_t * (J.d2uy_xx + J.d2ux_xy) +
   J.dnu_y * (J.duy_y + J.duy_y) + J.nu_t * (J.d2uy_yy + J.d2uy_yy) +
   J.dnu_z * (J.duy_z + J.duz_y) + J.nu_t * (J.d2uy_zz + J.d2uz_yz),

   J.dnu_x * (J.duz_x + J.dux_z) + J.nu_t * (J.d2uz_xx + J.d2ux_xz) +
   J.dnu_y * (J.duz_y + J.duy_z) + J.nu_t * (J.d2uz_yy + J.d2uy_yz) +
   J.dnu_z * (J.duz_z + J.duz_z) + J.nu_t * (J.d2uz_zz + J.d2uz_zz)⟩

/-- Viscosity-gradient commutator 2 (\nabla u)^T \nabla \nu_t. -/
def two_graduT_gradnut (J : VelocityViscosityJet) : Vec3 :=
  ⟨2 * (J.dux_x * J.dnu_x + J.duy_x * J.dnu_y + J.duz_x * J.dnu_z),
   2 * (J.dux_y * J.dnu_x + J.duy_y * J.dnu_y + J.duz_y * J.dnu_z),
   2 * (J.dux_z * J.dnu_x + J.duy_z * J.dnu_y + J.duz_z * J.dnu_z)⟩

/-- Gradient of velocity divergence \nabla(\nabla \cdot u). -/
def grad_div_u (J : VelocityViscosityJet) : Vec3 :=
  ⟨J.d2ux_xx + J.d2uy_xy + J.d2uz_xz,
   J.d2ux_xy + J.d2uy_yy + J.d2uz_yz,
   J.d2ux_xz + J.d2uy_yz + J.d2uz_zz⟩

/-- Vector Laplacian \Delta u = (\Delta u_x, \Delta u_y, \Delta u_z). -/
def laplacian_u (J : VelocityViscosityJet) : Vec3 :=
  ⟨J.d2ux_xx + J.d2ux_yy + J.d2ux_zz,
   J.d2uy_xx + J.d2uy_yy + J.d2uy_zz,
   J.d2uz_xx + J.d2uz_yy + J.d2uz_zz⟩

/-- Theorem 4.1: Exact solenoidality of vorticity \nabla \cdot \omega = \nabla \cdot (\nabla \times u) = 0
    on the C^2 velocity jet space. -/
theorem vorticity_divergence_zero_jet (J : VelocityViscosityJet) :
    d_omega_x_dx J + d_omega_y_dy J + d_omega_z_dz J = 0 := by
  unfold d_omega_x_dx d_omega_y_dy d_omega_z_dz
  ring

/-- Theorem 4.2: General Unconstrained Rotational-to-Strain Identity:
    -\nabla \times (\nu_t \omega)
      = \nabla \cdot (2 \nu_t S(u)) - 2 \nu_t \nabla(\nabla \cdot u) - 2 (\nabla u)^T \nabla \nu_t. -/
theorem rotational_strain_unconstrained_identity (J : VelocityViscosityJet) :
    neg_curl_nut_omega J =
      subVec (subVec (div_two_nut_S J) (smul (2 * J.nu_t) (grad_div_u J)))
             (two_graduT_gradnut J) := by
  ext <;>
  simp [neg_curl_nut_omega, div_two_nut_S, two_graduT_gradnut, grad_div_u,
        omegaVec, d_omega_x_dy, d_omega_x_dz, d_omega_y_dx, d_omega_y_dz,
        d_omega_z_dx, d_omega_z_dy, subVec, smul] <;>
  ring

/-- Theorem 4.3 (Main Text Eq. (28) & Lemma A.1): Solenoidal Rotational-to-Strain Identity:
    For every divergence-free velocity field satisfying \nabla(\nabla \cdot u) = 0,
    -\nabla \times (\nu_t \omega) = \nabla \cdot (2 \nu_t S(u)) - 2 (\nabla u)^T \nabla \nu_t. -/
theorem rotational_to_strain_solenoidal_identity (J : VelocityViscosityJet)
    (h_div_x : J.d2ux_xx + J.d2uy_xy + J.d2uz_xz = 0)
    (h_div_y : J.d2ux_xy + J.d2uy_yy + J.d2uz_yz = 0)
    (h_div_z : J.d2ux_xz + J.d2uy_yz + J.d2uz_zz = 0) :
    neg_curl_nut_omega J = subVec (div_two_nut_S J) (two_graduT_gradnut J) := by
  have h_gen := rotational_strain_unconstrained_identity J
  have h_grad_zero : grad_div_u J = ⟨0, 0, 0⟩ := by
    unfold grad_div_u
    rw [h_div_x, h_div_y, h_div_z]
  rw [h_gen, h_grad_zero]
  ext <;> simp [subVec, smul]

/-- Theorem 4.4 (Section 5.1(1) of Part 3): Interior Vortex Core Equivalence:
    Whenever \nabla \nu_t = 0 and \nabla(\nabla \cdot u) = 0,
    -\nabla \times (\nu_t \omega) = \nabla \cdot (2 \nu_t S(u)) = \nu_t \Delta u. -/
theorem interior_core_equivalence (J : VelocityViscosityJet)
    (h_div_x : J.d2ux_xx + J.d2uy_xy + J.d2uz_xz = 0)
    (h_div_y : J.d2ux_xy + J.d2uy_yy + J.d2uz_yz = 0)
    (h_div_z : J.d2ux_xz + J.d2uy_yz + J.d2uz_zz = 0)
    (h_dnu_x : J.dnu_x = 0) (h_dnu_y : J.dnu_y = 0) (h_dnu_z : J.dnu_z = 0) :
    neg_curl_nut_omega J = div_two_nut_S J ∧
    neg_curl_nut_omega J = smul J.nu_t (laplacian_u J) := by
  constructor
  · have h_sol := rotational_to_strain_solenoidal_identity J h_div_x h_div_y h_div_z
    rw [h_sol]
    ext <;> simp [subVec, two_graduT_gradnut, h_dnu_x, h_dnu_y, h_dnu_z]
  · have h_x : J.d2ux_xx = -(J.d2uy_xy + J.d2uz_xz) := by linarith [h_div_x]
    have h_y : J.d2uy_yy = -(J.d2ux_xy + J.d2uz_yz) := by linarith [h_div_y]
    have h_z : J.d2uz_zz = -(J.d2ux_xz + J.d2uy_yz) := by linarith [h_div_z]
    ext
    · simp [neg_curl_nut_omega, omegaVec, d_omega_z_dy, d_omega_y_dz,
            smul, laplacian_u, h_dnu_y, h_dnu_z]
      rw [h_x]
      ring
    · simp [neg_curl_nut_omega, omegaVec, d_omega_x_dz, d_omega_z_dx,
            smul, laplacian_u, h_dnu_z, h_dnu_x]
      rw [h_y]
      ring
    · simp [neg_curl_nut_omega, omegaVec, d_omega_y_dx, d_omega_x_dy,
            smul, laplacian_u, h_dnu_x, h_dnu_y]
      rw [h_z]
      ring

/-- Theorem 4.5: Non-positivity of rotational energy dissipation density
    -\nu_t |\omega|^2 \le 0 whenever \nu_t \ge 0. -/
theorem rotational_dissipation_energy_nonpos (J : VelocityViscosityJet)
    (h_nut : 0 ≤ J.nu_t) :
    -J.nu_t * ((omegaVec J).x ^ 2 + (omegaVec J).y ^ 2 + (omegaVec J).z ^ 2) ≤ 0 := by
  have h_w_sq : 0 ≤ (omegaVec J).x ^ 2 + (omegaVec J).y ^ 2 + (omegaVec J).z ^ 2 := by
    positivity
  have h_prod : 0 ≤ J.nu_t * ((omegaVec J).x ^ 2 + (omegaVec J).y ^ 2 + (omegaVec J).z ^ 2) :=
    mul_nonneg h_nut h_w_sq
  linarith

end Arkhenomia.Part3.Theorem4