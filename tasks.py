def grade_hard(env):
    total_possible = 0
    achieved = 0

    for t in env.tasks:
        weight = (t.priority * 2) + max(1, 10 - t.deadline)
        total_possible += weight

        if getattr(t, "completed", False):
            achieved += weight

    penalty = env.missed * 2
    score = (achieved - penalty) / (total_possible or 1)
    return max(0.0, min(1.0, float(score)))