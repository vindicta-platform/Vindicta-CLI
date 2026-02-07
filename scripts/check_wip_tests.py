"""Pre-commit hook: detect WIP-marked test items.

Collects tests marked with @pytest.mark.wip and fails if any are found,
signaling that WIP tests should not be committed without review.

Exit codes:
  0 — no WIP tests found (pass)
  1 — WIP tests detected (fail)
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-m", "wip", "-q"],
        capture_output=True,
        text=True,
    )

    # Exit code 5 = "no tests collected" → no WIP tests → success
    if result.returncode == 5:
        return 0

    # Exit code 0 = tests *were* collected → WIP tests exist → fail
    if result.returncode == 0:
        print("❌ WIP tests detected! Review before committing:")
        print(result.stdout)
        return 1

    # Any other exit code is an unexpected error — surface it
    print("⚠️  pytest collection failed unexpectedly:")
    print(result.stdout)
    print(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
