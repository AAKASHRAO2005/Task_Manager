def grade_easy(env):
    total_tasks = len(env.tasks) or 1
    return env.completed / total_tasks


def grade_medium(env):
    total = 0
    done = 0

    for t in env.tasks:
        total += t.priority
        if t.completed:
            done += t.priority

    return done / total if total else 0.0


def grade_hard(env):
    total_tasks = len(env.tasks) or 1
    score = env.completed - env.missed

    if score < 0:
        score = 0

    return score / total_tasks