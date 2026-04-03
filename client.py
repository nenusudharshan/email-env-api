import requests

BASE_URL = "http://127.0.0.1:8000"


from openai import OpenAI

client = OpenAI()


def ai_agent(email_text):
    prompt = f"""
        You are an email assistant.

        Given an email, classify it into:
        - category: spam / important / normal
        - action: reply / ignore / schedule
        - priority: low / medium / high

        Return ONLY JSON like:
        {{"category": "...", "action": "...", "priority": "..."}}

        Email:
        {email_text}
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content

    # Convert string → dict
    import json
    try:
        return json.loads(output)
    except:
            print("Invalid AI response, fallback")
            return simple_agent(email_text)

def simple_agent(email_text):
    email_text = email_text.lower()

    # Spam detection
    if "free" in email_text or "win" in email_text:
        return {
            "category": "spam",
            "action": "ignore",
            "priority": "low"
        }

    # Meeting / work
    if "meeting" in email_text:
        return {
            "category": "important",
            "action": "reply",
            "priority": "high"
        }

    # Billing / payment
    if "payment" in email_text or "subscription" in email_text:
        return {
            "category": "important",
            "action": "schedule",
            "priority": "medium"
        }

    # Default
    return {
        "category": "normal",
        "action": "ignore",
        "priority": "low"
    }

def run_episode():
    # Step 1: Reset
    reset_res = requests.post(f"{BASE_URL}/reset")
    obs = reset_res.json()

    print("\n Email:")
    print(obs["email_text"])
    print("Difficulty:", obs["difficulty"])

    # Step 2: Agent decides
    try:
        action = ai_agent(obs["email_text"])
    except:
        print("Falling back to rule-based agent")
        action = simple_agent(obs["email_text"])

    print("\n Agent Action:")
    print(action)

    # Step 3: Step
    step_res = requests.post(f"{BASE_URL}/step", json=action)
    result = step_res.json()

    print("\n Result:")
    print("Reward:", result["reward"])
    print("Done:", result["done"])


if __name__ == "__main__":
    for i in range(3):
        print(f"\n====== Episode {i+1} ======")
        run_episode()