from dataclasses import dataclass
from typing import List

DIFFICULTIES = ["Easy", "Medium", "Hard"]


@dataclass
class Question:
    question: str
    options: List[str]
    correct_answer: str
    subject: str
    topic: str
    difficulty: str


@dataclass
class Topic:
    subject: str
    name: str


def classify_accuracy(accuracy: float) -> str:
    """Classify topic performance using the required MVP thresholds."""
    if accuracy < 65:
        return "🔴 Weak"
    if accuracy < 85:
        return "🟡 Needs Practice"
    return "🟢 Strong"


def classification_label(accuracy: float) -> str:
    if accuracy < 65:
        return "Weak"
    if accuracy < 85:
        return "Needs Practice"
    return "Strong"
