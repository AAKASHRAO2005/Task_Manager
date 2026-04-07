"""Grader functions for Task Manager OpenEnv submission.

The submission checker expects at least 3 task-specific graders.
This file exposes one grader per difficulty level.
"""

from __future__ import annotations

from environment import TaskManagerEnv


def grade_easy(env: TaskManagerEnv) -> float:
    """Score by completion rate."""
    total_tasks = len(env.tasks) or 1
    return max(0.0, min(1.0, env.completed / total_tasks))


def grade_medium(env: TaskManagerEnv) -> float:
    """Score by weighted completion using priority."""
    total_weight = sum(task.priority for task in env.tasks) or 1
    completed_weight = sum(
        task.priority for task in env.tasks if task.completed and task.duration <= 0
    )
    return max(0.0, min(1.0, completed_weight / total_weight))


def grade_hard(env: TaskManagerEnv) -> float:
    """Reward completions while penalizing missed tasks."""
    total_tasks = len(env.tasks) or 1
    raw_score = env.completed - env.missed
    normalized = max(0.0, raw_score / total_tasks)
    return max(0.0, min(1.0, normalized))


TASK_GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard,
}


def evaluate_env(env: TaskManagerEnv) -> float:
    """Run the matching grader for the current environment difficulty."""
    grader = TASK_GRADERS.get(env.difficulty)
    if grader is None:
        raise ValueError(f"No grader configured for difficulty: {env.difficulty}")
    return grader(env)