from environment import TaskManagerEnv


def grade_easy(env: TaskManagerEnv) -> float:
    total_tasks = len(env.tasks) or 1
    return max(0.0, min(1.0, env.completed / total_tasks))


def grade_medium(env: TaskManagerEnv) -> float:
    total_weight = sum(task.priority for task in env.tasks) or 1
    completed_weight = sum(
        task.priority for task in env.tasks if getattr(task, "completed", False)
    )
    return max(0.0, min(1.0, completed_weight / total_weight))


def grade_hard(env: TaskManagerEnv) -> float:
    total_tasks = len(env.tasks) or 1
    score = max(0, env.completed - env.missed)
    return max(0.0, min(1.0, score / total_tasks))