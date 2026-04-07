#!/usr/bin/env bash
set -euo pipefail

echo "Validating submission..."
python -m py_compile app.py environment.py models.py grader.py tasks.py server/app.py
python - <<'PY'
from grader import grade_easy, grade_medium, grade_hard
from environment import TaskManagerEnv

env = TaskManagerEnv("easy")
assert callable(grade_easy)
assert callable(grade_medium)
assert callable(grade_hard)
print("Graders loaded successfully")
PY

echo "Validation complete!"