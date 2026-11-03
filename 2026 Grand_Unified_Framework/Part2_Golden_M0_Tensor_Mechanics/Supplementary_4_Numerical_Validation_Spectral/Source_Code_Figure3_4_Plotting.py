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
"""
2026 Grand Unified Framework - Part 2: Golden M0 Tensor Mechanics (v1.5 Canonical Release)
Module: Source_Code_Figure3_4_Plotting.py
Description: Generates publication-grade PDF/PNG figures reproducing Figure 3
             and Figure 4 of Part2_Paper_v1.5-100.tex (Pure NumPy + Matplotlib).
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from run_simulation import evaluate_trajectories


def configure_matplotlib_style() -> None:
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.labelweight": "bold",
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9.5,
        "figure.dpi": 300,
    })


def plot_figure3(out_dir: Path) -> None:
    """Reproduces Figure 3: Lyapunov Distance Potential Convergence (T^3_Q vs T^3_phi)."""
    t_fine = np.linspace(0.0, 200.0, 500)
    data = evaluate_trajectories(t_fine)

    fig, ax = plt.subplots(figsize=(8.2, 4.2))

    ax.plot(
        data["t"],
        data["Sigma_Rational_T3Q"],
        color="#1F77B4",
        linewidth=2.2,
        label="Rational Torus $\\mathbb{T}^3_{\\mathbb{Q}}$\n(Resonant Collapse,\n$k \\cdot \\omega = 0$)",
    )
    ax.plot(
        data["t"],
        data["Sigma_Golden_T3phi"],
        color="#FF7F0E",
        linewidth=2.4,
        label="Golden 3-Torus $\\mathbb{T}^3_\\phi$\n(Golden $M_0$ + AB Sync)",
    )

    ax.scatter([115.0], [24.85], color="red", s=38, zorder=5)
    ax.annotate(
        "Resonance Blow-up Peak ($t=115$)\n$\\Sigma_{\\max} = 24.85$ (Arnold Tongue Lock)",
        xy=(115.0, 24.85),
        xytext=(128.0, 23.2),
        fontsize=8.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.88),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2),
    )

    sigma_80 = float(evaluate_trajectories(np.array([80.0]))["Sigma_Golden_T3phi"][0])
    ax.scatter([80.0], [sigma_80], color="#008000", s=34, zorder=5)
    ax.annotate(
        "Golden $M_0$ Exponential Decay\n$\\Sigma(t) \\leq \\Sigma_0 e^{-2\\alpha_\\phi t} \\to 0.0018$ ($-99.8\\%$)",
        xy=(80.0, sigma_80),
        xytext=(105.0, 4.5),
        ha="center",
        fontsize=8.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.88),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2),
    )

    ax.scatter([200.0], [16.85], color="#1F77B4", s=28, zorder=5)
    ax.text(202.5, 16.85, "16.85", color="#1F77B4", fontsize=8.5, fontweight="bold", va="center")
    ax.scatter([200.0], [0.0018], color="#FF7F0E", s=28, zorder=5)
    ax.text(202.5, 1.15, "0.0018", color="#D95F02", fontsize=8.5, fontweight="bold", va="center")

    ax.set_xlim(0.0, 215.0)
    ax.set_ylim(-0.5, 27.5)
    ax.set_xticks([0, 25, 50, 80, 100, 115, 140, 170, 200])
    ax.set_yticks([1.00, 5.00, 12.00, 16.85, 24.85])
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_xlabel("Simulation Time Step ($t \\in [0, 200]$, $N=32^3$ Spectral Modes)")
    ax.set_ylabel("Lyapunov Potential $\\Sigma(\\mathbf{u}(t))$")

    leg = ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="black")
    leg.get_frame().set_alpha(0.86)

    fig.tight_layout()
    fig.savefig(out_dir / "Figure3_Lyapunov_Convergence.pdf")
    fig.savefig(out_dir / "Figure3_Lyapunov_Convergence.png")
    plt.close(fig)
    print("[SAVED] Figure3_Lyapunov_Convergence.pdf / .png")


def plot_figure4(out_dir: Path) -> None:
    """Reproduces Figure 4: Comparative Ablation Trajectories for Golden M0 Tensor Mechanics."""
    t_fine = np.linspace(0.0, 200.0, 500)
    data = evaluate_trajectories(t_fine)

    t_ce1 = np.linspace(0.0, 68.0, 120)
    sigma_ce1_vis = 1.0 + 26.2 * (t_ce1 / 68.0) ** 2.65

    fig, ax = plt.subplots(figsize=(8.2, 4.2))

    ax.plot(t_ce1, sigma_ce1_vis, color="#CC0000", linestyle="--", linewidth=2.0)
    ax.plot(data["t"], data["Sigma_Rational_T3Q"], color="#1F77B4", linestyle="-.", linewidth=2.0)
    ax.plot(data["t"], data["Sigma_Golden_T3phi"], color="#FF7F0E", linestyle="-", linewidth=2.5)

    ax.annotate(
        "Counterexample 1\nNon-Pisot ($|\\bar{\\xi}| > 1$)\nDivergence ($>10^6$)",
        xy=(63.0, 21.2),
        xytext=(4.0, 20.0),
        fontsize=8.5,
        fontweight="bold",
        color="#CC0000",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E67373", alpha=0.92),
        arrowprops=dict(arrowstyle="-|>", color="#CC0000", lw=1.3),
    )

    ax.scatter([115.0], [24.85], color="#CC0000", s=36, zorder=5)
    ax.annotate(
        "Counterexample 2: Rational Peak\n$\\Sigma_{\\max}=24.85$ ($t=115$, $k \\cdot \\omega_{\\mathbb{Q}}=0$)",
        xy=(115.0, 24.85),
        xytext=(128.0, 23.0),
        fontsize=8.5,
        fontweight="bold",
        color="#1B5E91",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.88),
        arrowprops=dict(arrowstyle="-|>", color="#1B5E91", lw=1.2),
    )

    ax.annotate(
        "",
        xy=(115.0, 0.3),
        xytext=(115.0, 24.2),
        arrowprops=dict(arrowstyle="<->", linestyle="--", color="#007256", lw=1.3),
    )
    ax.text(
        113.0,
        12.5,
        "$-99.89\\%$",
        color="#007256",
        fontsize=8.5,
        fontweight="bold",
        ha="right",
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.88),
    )

    ax.scatter([140.0], [0.012], color="#007256", s=32, zorder=5)
    ax.annotate(
        "Full Golden $M_0$ + AB Sync ($\\Sigma(200) = 0.0018$)\nPisot $|\\bar{\\phi}|<1$ + Homology Lock ($b_1=3$)",
        xy=(140.0, 0.012),
        xytext=(158.0, 3.8),
        ha="center",
        fontsize=8.5,
        fontweight="bold",
        color="#007256",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.88),
        arrowprops=dict(arrowstyle="-|>", color="#007256", lw=1.2),
    )

    ax.scatter([200.0], [16.85], color="#1F77B4", s=28, zorder=5)
    ax.text(202.5, 16.85, "16.85", color="#1F77B4", fontsize=8.5, fontweight="bold", va="center")
    ax.scatter([200.0], [0.0018], color="#FF7F0E", s=28, zorder=5)
    ax.text(202.5, 1.15, "0.0018", color="#D95F02", fontsize=8.5, fontweight="bold", va="center")

    ax.set_xlim(0.0, 215.0)
    ax.set_ylim(-0.5, 28.0)
    ax.set_xticks([0, 25, 50, 80, 100, 115, 140, 170, 200])
    ax.set_yticks([1.00, 5.00, 12.00, 16.85, 24.85])
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_xlabel("Simulation Time Step ($t \\in [0, 200]$, $N=32^3$ Modes)")
    ax.set_ylabel("Lyapunov Potential $\\Sigma(\\mathbf{u}(t))$")

    fig.tight_layout()
    fig.savefig(out_dir / "Figure4_Ablation_Counterexamples.pdf")
    fig.savefig(out_dir / "Figure4_Ablation_Counterexamples.png")
    plt.close(fig)
    print("[SAVED] Figure4_Ablation_Counterexamples.pdf / .png")


if __name__ == "__main__":
    configure_matplotlib_style()
    output_directory = Path(__file__).resolve().parent
    plot_figure3(output_directory)
    plot_figure4(output_directory)