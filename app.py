from flask import Flask, jsonify, request

from environment import TaskManagerEnv
from models import Action

app = Flask(__name__)
env = TaskManagerEnv()


def serialize_task(task):
    return {
        "id": task.id,
        "priority": task.priority,
        "deadline": task.deadline,
        "duration": task.duration,
        "completed": task.completed,
    }


def serialize_observation(obs):
    return {
        "time": obs.time,
        "tasks": [serialize_task(t) for t in obs.tasks],
        "completed": obs.completed,
        "missed": obs.missed,
    }


@app.get("/")
def home():
    return jsonify({"status": "ok", "message": "Task Manager OpenEnv API running"})


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.post("/reset")
def reset():
    global env
    data = request.get_json(silent=True) or {}
    difficulty = data.get("task") or data.get("difficulty") or "easy"
    env = TaskManagerEnv(difficulty=difficulty)
    obs = env.reset()
    return jsonify({
        "observation": serialize_observation(obs),
        "reward": 0.0,
        "done": False
    })


@app.get("/state")
def state():
    obs = env.state()
    return jsonify(serialize_observation(obs))


@app.post("/step")
def step():
    data = request.get_json(silent=True) or {}
    if "task_id" not in data:
        return jsonify({"error": "task_id is required"}), 400

    action = Action(task_id=int(data["task_id"]))
    obs, reward, done, info = env.step(action)

    return jsonify({
        "observation": serialize_observation(obs),
        "reward": float(reward),
        "done": bool(done),
        "info": info,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)