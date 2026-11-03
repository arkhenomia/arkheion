#!/usr/bin/env bash
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
#
# Taylor-Green Re=1600 benchmark pipeline for NS_TZT.
# Usage:
#   ./run_benchmark.sh            # quick (N=32, t=2) then full (N=64, t=20)
#   ./run_benchmark.sh quick      # N=32, t-end 2.0 only
#   ./run_benchmark.sh full       # N=64, t-end 20.0 only
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

MODE="${1:-all}"
RESULTS="$ROOT/results"
mkdir -p "$RESULTS"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing command: $1" >&2
    exit 1
  }
}

need python3

echo "[deps] checking numpy scipy matplotlib"
if ! python3 - << 'PY'
import importlib.util, sys
missing = [m for m in ("numpy", "scipy", "matplotlib") if importlib.util.find_spec(m) is None]
if missing:
    print("missing packages:", ", ".join(missing))
    sys.exit(2)
print("ok")
PY
then
  echo "[deps] installing from requirements.txt"
  python3 -m pip install -r "$ROOT/requirements.txt"
fi

run_one() {
  local tag="$1" n="$2" tend="$3"
  local out="$RESULTS/$tag"
  mkdir -p "$out"
  echo "[run] $tag  N=$n  t-end=$tend"
  python3 "$ROOT/tzt_tgv_benchmark.py" --n "$n" --t-end "$tend" --out "$out"
  # the solver already writes into --out; keep a flat copy of the four deliverables
  for f in tgv_dissipation_rate.png tgv_energy_spectrum.png tgv_max_vorticity.png tgv_metrics.csv; do
    if [[ -f "$out/$f" ]]; then
      cp -f "$out/$f" "$RESULTS/${tag}_${f}"
    fi
  done
  echo "[done] $tag -> $RESULTS"
}

case "$MODE" in
  quick)
    run_one quick 32 2.0
    ;;
  full)
    run_one full 64 20.0
    ;;
  all)
    run_one quick 32 2.0
    run_one full 64 20.0
    ;;
  *)
    echo "unknown mode: $MODE (use quick | full | all)" >&2
    exit 1
  esac

echo "[results]"
ls -la "$RESULTS"