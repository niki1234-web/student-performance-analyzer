from dataclasses import dataclass
from typing import List
from dataclasses import dataclass
from typing import List
# --- Class Levels & Streams ---
CLASS_LEVELS = [
    "Primary (1-5)",
    "Middle (6-8)",
    "Secondary (9-10)",
    "Senior Secondary (11-12)",
    "Graduate (UG)",
    "Post Graduate (PG)",
]

STREAMS = ["General", "Science", "Commerce", "Arts"]

CLASSES_BY_LEVEL = {
    "Primary (1-5)": ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"],
    "Middle (6-8)": ["Class 6", "Class 7", "Class 8"],
    "Secondary (9-10)": ["Class 9", "Class 10"],
    "Senior Secondary (11-12)": ["Class 11", "Class 12"],
    "Graduate (UG)": ["1st Year", "2nd Year", "3rd Year"],
    "Post Graduate (PG)": ["1st Year", "2nd Year"],
}

STREAMS_BY_LEVEL = {
    "Primary (1-5)": ["General"],
    "Middle (6-8)": ["General"],
    "Secondary (9-10)": ["General"],
    "Senior Secondary (11-12)": ["Science", "Commerce", "Arts"],
    "Graduate (UG)": ["Science", "Commerce", "Arts"],
    "Post Graduate (PG)": ["Science", "Commerce", "Arts"],
}
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
