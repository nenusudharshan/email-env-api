import random
from models import EmailAction, EmailObservation, EmailState


class EmailEnv:

    def __init__(self):
        self.tasks = [
            {
                "id": "easy_spam_detection",
                "difficulty": "easy",
                "email": {
                    "text": "Win a free iPhone now!!! Click here",
                    "sender": "unknown@spam.com",
                    "subject": "Free iPhone"
                },
                "solution": {
                    "category": "spam",
                    "action": "ignore",
                    "priority": "low"
                }
            },
            {
                "id": "medium_meeting",
                "difficulty": "medium",
                "email": {
                    "text": "Reminder: Team meeting tomorrow at 10 AM",
                    "sender": "boss@company.com",
                    "subject": "Meeting Reminder"
                },
                "solution": {
                    "category": "important",
                    "action": "reply",
                    "priority": "high"
                }
            },
            {
                "id": "hard_billing",
                "difficulty": "hard",
                "email": {
                    "text": "Your Netflix subscription renewal failed. Update payment.",
                    "sender": "billing@netflix.com",
                    "subject": "Payment Issue"
                },
                "solution": {
                    "category": "important",
                    "action": "schedule",
                    "priority": "medium"
                }
            }
        ]

        self.current_task = None
        self.state = None

    # RESET
    def reset(self):
        self.current_task = random.choice(self.tasks)

        email = self.current_task["email"]
        solution = self.current_task["solution"]

        self.state = EmailState(
        current_email=email["text"],
        correct_category=solution["category"],
        correct_action=solution["action"],
        correct_priority=solution["priority"],
        difficulty=self.current_task["difficulty"],   
        step_count=0
        )

        return EmailObservation(
            email_text=email["text"],
            sender=email["sender"],
            subject=email["subject"],
            difficulty=self.current_task["difficulty"],   
            priority_hint=solution["priority"] if self.current_task["difficulty"] == "easy" else None,
            done=False,
            reward=0.0
        )

    # STEP (WITH TASK-AWARE GRADER)
    def step(self, action: EmailAction):
        self.state.step_count += 1

        solution = self.current_task["solution"]
        difficulty = self.current_task["difficulty"]

        score = 0.0

        if difficulty == "easy":
            if action.category == solution["category"]:
                score = 1.0

        elif difficulty == "medium":
            if action.category == solution["category"]:
                score += 0.5
            if action.action == solution["action"]:
                score += 0.5

        elif difficulty == "hard":
            if action.category == solution["category"]:
                score += 0.4
            if action.action == solution["action"]:
                score += 0.3
            if action.priority == solution["priority"]:
                score += 0.3

        return EmailObservation(
            email_text=self.state.current_email,
            sender="hidden",
            subject="hidden",
            difficulty=self.current_task["difficulty"],
            done=True,
            reward=score
        )

    # STATE
    def get_state(self):
        return {
            "current_email": self.state.current_email,
            "correct_category": self.state.correct_category,
            "correct_action": self.state.correct_action,
            "correct_priority": self.state.correct_priority,
            "difficulty": self.current_task["difficulty"],
            "task_id": self.current_task["id"],
            "step_count": self.state.step_count
        }