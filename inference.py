import requests

BASE_URL = "http://127.0.0.1:7860"

def run():
    # Reset environment
    res = requests.post(f"{BASE_URL}/reset")
    print("Reset:", res.json())

    # Take a sample step
    action = {
        "category": "important",
        "action": "schedule",
        "priority": "high"
    }

    res = requests.post(f"{BASE_URL}/step", json=action)
    print("Step:", res.json())


if __name__ == "__main__":
    run()