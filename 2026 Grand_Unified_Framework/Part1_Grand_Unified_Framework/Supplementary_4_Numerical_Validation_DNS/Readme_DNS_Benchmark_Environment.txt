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
# granted by implication. Governed by the latest LICENSE.txt (Policy v2.2.2+).
# ==============================================================================

# DNS Benchmark Environment and Ablation Counter-Example Notes
# 2026 Grand Unified Framework - Part 1 (v1.5 Canonical Release):
# Macroscopic Gravity-Fluid Dynamics (H.U.G.G.E.R) & Topological Zero Tensor (TZT) Validation

## 1. Note on Ablation Counter-Example Data and Figures
The enclosed ablation figures, `CounterExample_1_Ill_Posed_Ablation_Without_Solenoidal_Condition.png` and `CounterExample_2_Energy_Blowup_Without_Mantle_Dissipation.png`, visualize the rapid numerical and energetic blow-up that occurs when the solenoidal Helmholtz-Leray projection condition (\nabla \cdot \mathcal{X} = 0) specified in Section 3 and Section 4.2, or the macroscopic Virial stress buffer (\bm{\Phi}_{mantle}) and localized cutoff valve (\chi_\Lambda) detailed in Section 2 and Section 5 of the main manuscript, are intentionally omitted.

This ablation test demonstrates that violating the coupled canonical constraints (solenoidality and localized counter-strain dissipation) causes the system to deteriorate into non-physical instability on an under-resolved grid. In contrast, the canonical pseudo-spectral solver (`Source_Code_1_TZT_Dynamics_Solver.py`), which enforces the solenoidal projection and localized supercritical valve constraints, suppresses the singularity spike and maintains bounded enstrophy evolution, as plotted by `Source_Code_2_Figure1_Visualization.py` using `Data_1_Euler_Inviscid_Limit_DNS.csv` (`Figure1_Geometric_Cancellation.png` / `TZT_Euler_Stabilization_PRL.png`).

## 2. Direct Numerical Simulation (DNS) Parameters
The numerical validations in the inviscid Euler limit and the high-Reynolds-number viscous regime (Re = 10,000) were conducted under the following benchmark specifications:

* Domain: 3D Periodic Flat Torus T^3 = [0, 2\pi)^3
* Spatial Discretization: Pseudo-spectral Fourier-Galerkin method with the 2/3 dealiasing rule
* Time Integration: Classical 4th-order explicit Runge-Kutta (RK4)
* Grid Resolutions (N^3): 32^3, 48^3, 64^3, and 96^3
* Time Step (dt): 0.025 (halved to 0.0125 for temporal convergence and robustness checks)
* Baseline Regimes: Inviscid Euler limit (\nu = 0) and Viscous Navier-Stokes at Re = 10,000 (\nu = 10^{-4})

## 3. TZT-Augmented Configuration and Localized Valve Execution
In `Source_Code_1_TZT_Dynamics_Solver.py`, the TZT counter-strain and rotational regularization operators are configured with the following baseline parameters:

* C_X (Solenoidal Intake Scaling): \pm 0.1
* C_O (Rotational Spin Tensor Scaling): 1.0
* \delta_m (Denominator Regularizer in \mathcal{X}): 1.0
* \varepsilon (Spin Saturation Regularizer in \mathcal{O}^{turb}): 10^{-2}
* \nu_{turb} (Subgrid Eddy Viscosity Scale): Coupled with C_s = 0.17 and grid filter scale \Delta = 2\pi / N
* --valve (Localization Mode, synchronized with Lean 4 `CriticalRegion`):
  - `--valve omega` (Default in v1.5): Activates TZT forcing strictly on the supercritical vorticity region K = {x \in T^3 : |\omega(x)|^2 > \Lambda^2}, preserving unmodified Navier-Stokes/Euler kinematics outside K.
  - `--valve global`: Applies the TZT operator across the entire domain K = T^3 (retained for comparison with baseline global-limit data).

---
## 4. License, Attribution, and Governance (Policy v2.2.2+)

* Author & Institute: Jung Soo Kim (ORCID: 0009-0006-5140-0604) / Arkhenomia Institute (https://arkhenomia.org)
* License: CC BY-NC 4.0 (Commercial licensing administered by Arkhenetics; see LICENSE.txt)
* Canonical Repository: https://github.com/arkhenomia/arkheion
* Dataset Archive: https://huggingface.co/datasets/arkhenomia/arkheion
* Commercial Licensing & Enterprise Inquiries: Arkhenetics (https://arkhenetics.com)

All manuscripts, formal verification proofs, symbolic CAS scripts, numerical solvers, and benchmark datasets in this repository are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0, https://creativecommons.org/licenses/by-nc/4.0/) and governed by the latest version of `LICENSE.txt` (Policy Version 2.2.2+).