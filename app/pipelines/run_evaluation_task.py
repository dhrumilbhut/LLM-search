import subprocess
import sys


def run_evaluation():
    result = subprocess.run(
        [sys.executable, "/opt/project/scripts/run_evaluation.py"],
        capture_output=True,
        text=True
    )

    # Always print output for observability
    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    # Only fail if the process actually failed
    if result.returncode != 0:
        raise RuntimeError(
            f"Evaluation script failed with exit code {result.returncode}"
        )
