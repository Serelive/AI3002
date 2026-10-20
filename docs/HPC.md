# Continue Lab 1 on the 107 Slurm platform

Use the login node for Git, file transfers, environment setup, and job submission. Run training, numerical tests, and notebooks on allocated compute nodes. The [107 guide](https://xinchengo.github.io/ustc107/guides/ai/deep-learning-homework/) describes shared home storage and portal file transfers; consult the portal for your current partition, QoS, account, and limits. Course-provided settings supplied by the user are partition `Students`, QoS `qos_stu_default`, and no explicit account. The typical course profile is 1 GPU, 4 CPUs, 16 GB RAM, and up to 4 hours. These settings are configurable at submission; the first job confirms their availability for this account.

## Set up once on the login node

After publishing the branch yourself, clone it into storage visible from both login and compute nodes:

```bash
mkdir -p ~/projects ~/models
cd ~/projects
git clone --branch feat/lab1 https://github.com/Serelive/AI3002.git
cd AI3002
uv sync --locked
```

Use the site's approved Python/uv installation or load its Python module first. The project requires Python 3.11 or later; local verification used Python 3.14.4. `uv sync --locked` creates the root `.venv` from `pyproject.toml` and `uv.lock`; rebuild it on the cluster instead of copying the workstation environment. If package downloads are unavailable, prepare the environment through the site's supported package mirror or offline workflow before submitting jobs. Jobs use the prepared environment and perform no downloads.

Keep the checkout, `.venv`, and inputs on shared storage. An optional feature-extraction script uses PyTorch/Transformers and a GPU; those dependencies are outside the current NumPy probe environment. The supplied feature files let Tasks 2 and 3 run on CPUs.

### Using the course Conda environment instead

To use your user-managed `ai26` environment directly, activate it on the login node and install the locked dependencies there. Its Python must satisfy the project's Python 3.11+ requirement. With uv available, run from the checkout root:

```bash
conda activate ai26
mkdir -p scratch
uv export --locked --no-dev --no-emit-project --format requirements.txt \
  --output-file scratch/hpc-requirements.txt
python -m pip install -r scratch/hpc-requirements.txt
python -m pip install --no-deps -e .
export AI3002_PYTHON="$CONDA_PREFIX/bin/python"
```

The export uses `uv.lock` instead of resolving a new set of package versions. `AI3002_PYTHON` tells the launcher which executable to use and is inherited by `sbatch` under its default environment export. Keep the Conda environment activated when submitting so any activation-provided library settings are also inherited. Set this variable again in each new submission shell. Without it, the launcher uses the root `.venv/bin/python`. Choose one environment for a batch of experiments and record it with the results.

The repository and environment are accessible from the shared `$HOME`. Keep the checkout under `~/projects/AI3002` and optional downloaded LLMs under `~/models/`; probe training uses the supplied feature arrays and does not need those models.

## Transfer the inputs separately

Create a portable input bundle on your workstation, from the repository root:

```bash
mkdir -p scratch/hpc-transfer
tar -czf scratch/hpc-transfer/lab1-datasets.tar.gz \
  assignments/labs/lab1/main/datasets
sha256sum scratch/hpc-transfer/lab1-datasets.tar.gz
```

Upload the bundle using the portal's file manager. On the cluster, verify its checksum and extract it from the repository root into a fresh checkout. This restores `assignments/labs/lab1/main/datasets/` without replacing code. Check all 16 dataset files:

```bash
sha256sum /path/to/uploaded/lab1-datasets.tar.gz
tar -xzf /path/to/uploaded/lab1-datasets.tar.gz
grep 'main/datasets/' assignments/labs/lab1/docs/input-checksums.sha256 | sha256sum -c -
```

Replace `/path/to/uploaded/` with the actual upload directory. For handouts and the full original archive, use [input recovery instructions](../assignments/labs/lab1/docs/INPUTS.md). Copy selected prior experiment outputs separately if you want to compare against them; Git does not carry these artifacts.

## Submit a small check, then train

From the checkout root in a Bash login shell, set the resource options to values permitted by your account:

```bash
# Course-provided defaults; adjust if your portal allocation differs.
slurm_options=(--partition=Students --qos=qos_stu_default)
mkdir -p assignments/labs/lab1/output/slurm/logs
sbatch "${slurm_options[@]}" \
  --output=assignments/labs/lab1/output/slurm/logs/%x-%j.log \
  scripts/slurm/lab1.sbatch "$PWD" check
```

The launcher defaults to one CPU, 4 GiB memory, and 30 minutes, with one Slurm task. No account is specified; add `--account=...` only if your allocation requires it. Override these with `sbatch --cpus-per-task`, `--mem`, and `--time` before the script path as needed. NumPy/BLAS thread counts follow the CPU allocation. The `check` job runs the three focused test scripts, including real-data smoke checks.

For the course's larger resource profile, extend the submission options:

```bash
slurm_options+=(--cpus-per-task=4 --mem=16G --time=04:00:00)
# Add --gres=gpu:1 when the workload or partition policy requires a GPU.
```

The current probe code computes with NumPy on CPUs. Requesting a GPU does not accelerate it. Keep GPU allocation optional and follow the partition policy shown in the portal.

After the check job succeeds, submit a short Task 3 pilot:

```bash
sbatch "${slurm_options[@]}" \
  --output=assignments/labs/lab1/output/slurm/logs/%x-%j.log \
  scripts/slurm/lab1.sbatch "$PWD" truth 11 \
  --lr 0.01 --l1 0.01 --l2 0.01 --max_iter 100
```

For Task 2, replace `truth 11 ...` with `world 11 --lr 0.0001 --l1 0.3 --l2 0.3 --max_iter 10000`. For a small comparison, use `comparison --layers 11 35 --l1 0.3 --l2 0.3 --lr 0.0001 --max_iter 100`. Increase the update budget after checking the pilot.

Each job stores artifacts under `assignments/labs/lab1/output/slurm/job-JOBID/`, with command, commit, working-tree status, and dependency versions in `environment.txt`. The existing models initialize at zero, so these training runs do not need a random seed. Training prints validation metrics to the Slurm log. The comparison runner also writes its result table. Keep the log, environment record, and model together when selecting a result.

Slurm copies the batch script, not the repository: keep the checkout unchanged while its jobs are queued or running. Commit/pull between batches, or use separate checkouts for simultaneous versions. Jobs can pass an explicit `--output_dir`, but the default job-specific paths are easiest to keep separate.

## Monitor and continue

```bash
squeue -u "$USER"
# Replace JOBID with the submitted numeric ID:
sacct -j JOBID --format=JobID,State,ExitCode,Elapsed,MaxRSS
tail -f assignments/labs/lab1/output/slurm/logs/ai3002-lab1-JOBID.log
# Cancel a job when needed:
scancel JOBID
```

A successful `sbatch` command means the job was submitted; check its completion state and log for the training result. Use the portal's compute-backed Jupyter/VS Code sessions for interactive experiments. Preserve the shared `.venv` and use the same branch there.

Launcher options and job-ID log expansion follow the [Slurm sbatch documentation](https://slurm.schedmd.com/sbatch.html). Local checks validate the launcher and Python scripts; the first cluster check job verifies the actual scheduler, filesystem, and environment together.

## Local verification of this handoff

On October 20, the 12 existing model/comparison/iteration tests and five launcher tests passed. The launcher tests simulate Slurm commands to check paths containing spaces, CPU thread limits, argument forwarding, login-node rejection, failure propagation, and an explicit Conda interpreter. Reproduce them locally with:

```bash
bash -n scripts/slurm/lab1.sbatch
.venv/bin/python tests/test_slurm_launcher.py
uv lock --check --offline
```

All 21 recorded input checksums also passed. No cluster job has been submitted; the supplied partition/QoS and chosen cluster environment still need the first on-cluster check.
