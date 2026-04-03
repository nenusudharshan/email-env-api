from pydantic import BaseModel, Field
from typing import Optional


# ACTION
class EmailAction(BaseModel):
    category: str = Field(..., description="spam / important / normal")
    action: str = Field(..., description="reply / ignore / schedule")
    priority: str = Field(..., description="low / medium / high")


# OBSERVATION
class EmailObservation(BaseModel):
    email_text: str
    sender: str
    subject: str

    difficulty: str   
    priority_hint: Optional[str] = None

    done: bool
    reward: float


# STATE
class EmailState(BaseModel):
    current_email: str
    correct_category: str
    correct_action: str
    correct_priority: str
    difficulty: str    
    step_count: int = 0