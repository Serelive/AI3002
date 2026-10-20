"""Exercise the batch launcher without a Slurm installation or job submission."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

LAUNCHER = Path(__file__).resolve().parents[1] / "scripts/slurm/lab1.sbatch"


class SlurmLauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ai3002-slurm-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces"
        self.bin = self.root / ".venv/bin"
        self.bin.mkdir(parents=True)
        for name, body in {
            "python": 'printf "mock Python environment\\n"\n',
            "git": 'if [[ "$1" == rev-parse ]]; then echo test-commit; fi\n',
            "srun": 'printf "%s\\n" "$@" >> "$CAPTURE"\nprintf "threads=%s\\n" "$OPENBLAS_NUM_THREADS" >> "$CAPTURE"\nexit "${MOCK_EXIT:-0}"\n',
        }.items():
            p = self.bin / name
            p.write_text("#!/usr/bin/env bash\n" + body)
            p.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}",
                        CAPTURE=str(self.root / "calls"),
                        SLURM_JOB_ID="12345", SLURM_CPUS_PER_TASK="2")
        self.env.pop("SLURM_ARRAY_TASK_ID", None)

    def run_job(self, *args):
        return subprocess.run(["bash", str(LAUNCHER), str(self.root), *args],
                              env=self.env, text=True, capture_output=True)

    def test_training_paths_threads_and_arguments(self):
        result = self.run_job("truth", "11", "--max_iter", "100")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = (self.root / "calls").read_text().splitlines()
        self.assertIn(str(self.bin / "python"), calls)
        self.assertIn("assignments/labs/lab1/output/slurm/job-12345/truth", calls)
        self.assertIn("threads=2", calls)
        self.assertIn("100", calls)
        self.assertTrue((self.root / "assignments/labs/lab1/output/slurm/job-12345/environment.txt").exists())

    def test_check_and_comparison(self):
        self.assertEqual(self.run_job("check").returncode, 0)
        calls = (self.root / "calls").read_text()
        self.assertEqual(calls.count("threads=2"), 3)
        result = self.run_job("comparison", "--layers", "11", "35")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("p02_comparison.py", (self.root / "calls").read_text())

    def test_reject_login_node_and_invalid_mode(self):
        self.assertEqual(self.run_job("unknown").returncode, 2)
        self.assertEqual(self.run_job("truth").returncode, 2)
        self.env.pop("SLURM_JOB_ID")
        result = self.run_job("check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Submit this script with sbatch", result.stderr)
        self.assertFalse((self.root / "calls").exists())

    def test_propagates_step_failure(self):
        self.env["MOCK_EXIT"] = "7"
        self.assertEqual(self.run_job("check").returncode, 7)
        self.assertEqual((self.root / "calls").read_text().count("threads=2"), 1)


if __name__ == "__main__":
    unittest.main()
