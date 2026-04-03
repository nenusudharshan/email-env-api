from fastapi import FastAPI
from server.email_env_environment import EmailEnv
from models import EmailAction
import requests

app = FastAPI()
env = EmailEnv()

@app.get("/baseline")
def run_baseline():
    total_reward = 0.0
    episodes = 3

    for _ in range(episodes):
        # Reset
        obs = env.reset()
        
        # Use simple agent logic
        email = obs["email_text"].lower()

        if "free" in email or "win" in email:
            action = {"category": "spam", "action": "ignore", "priority": "low"}
        elif "meeting" in email:
            action = {"category": "important", "action": "reply", "priority": "high"}
        elif "payment" in email or "subscription" in email:
            action = {"category": "important", "action": "schedule", "priority": "medium"}
        else:
            action = {"category": "normal", "action": "ignore", "priority": "low"}

        # Step
        result = env.step(EmailAction(**action))
        total_reward += result["reward"]

    return {
        "episodes": episodes,
        "average_score": total_reward / episodes
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: EmailAction):
    return env.step(action)


# ✅ ONLY ONE STATE ENDPOINT
@app.get("/state")
def get_state():
    return env.get_state()

@app.get("/tasks")
def get_tasks():
    return [
        {
            "id": task["id"],
            "difficulty": task["difficulty"],
            "description": task["email"]["subject"]
        }
        for task in env.tasks
    ]