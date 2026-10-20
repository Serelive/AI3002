#!/usr/bin/env bash
#SBATCH --job-name=ai3002-lab1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: sbatch [Slurm options] $0 /absolute/repo/root {check|world|truth|comparison} [arguments...]" >&2
    exit 2
fi
: "${SLURM_JOB_ID:?Submit this script with sbatch to run on a compute node}"
repo_root=$1
mode=$2
shift 2
[[ "$repo_root" = /* ]] || { echo "Repository path must be absolute" >&2; exit 2; }
cd "$repo_root"
python=${AI3002_PYTHON:-"$repo_root/.venv/bin/python"}
[[ -x "$python" ]] || { echo "Create .venv or export AI3002_PYTHON to your Conda Python; see docs/HPC.md" >&2; exit 2; }

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=$OMP_NUM_THREADS
export MKL_NUM_THREADS=$OMP_NUM_THREADS
export NUMEXPR_NUM_THREADS=$OMP_NUM_THREADS
export MPLBACKEND=Agg
export PYTHONUNBUFFERED=1
lab=assignments/labs/lab1
run_dir="$lab/output/slurm/job-${SLURM_JOB_ID}${SLURM_ARRAY_TASK_ID:+-${SLURM_ARRAY_TASK_ID}}"
mkdir -p "$run_dir"

case "$mode" in
    check)
        [[ $# -eq 0 ]] || { echo "check takes no arguments" >&2; exit 2; }
        ;;
    world|truth)
        [[ $# -ge 1 ]] || { echo "$mode requires a layer number" >&2; exit 2; }
        layer=$1
        shift
        command=("$python" "$lab/main/train23.py" "$mode" "$layer" --output_dir "$run_dir/$mode" "$@")
        ;;
    comparison)
        command=("$python" "$lab/main/p02_comparison.py" --output_dir "$run_dir/comparison" "$@")
        ;;
    *) echo "Unknown mode: $mode" >&2; exit 2 ;;
esac

{
    date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
    printf 'Job: %s\nHost: %s\nCPUs: %s\n' "$SLURM_JOB_ID" "$(hostname)" "$OMP_NUM_THREADS"
    git rev-parse HEAD
    git status --short
    printf 'Python executable: %s\n' "$python"
    "$python" --version
    "$python" -c 'from importlib.metadata import version; print({p: version(p) for p in ("numpy", "pandas", "matplotlib", "scikit-learn")})'
    if [[ "$mode" != check ]]; then printf 'Command: '; printf '%q ' "${command[@]}"; printf '\n'; fi
} | tee "$run_dir/environment.txt"

if [[ "$mode" == check ]]; then
    for test in p01_test_linear-regression.py p02_test_comparison.py p03_test_iteration.py; do
        srun --ntasks=1 --cpus-per-task="$OMP_NUM_THREADS" "$python" "$lab/main/$test"
    done
else
    srun --ntasks=1 --cpus-per-task="$OMP_NUM_THREADS" "${command[@]}"
fi
