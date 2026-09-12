from typing import Dict, Optional

import pandas as pd

from analytics import answers_dataframe, calculate_topic_performance, performance_over_time


def _recent_performance_label(topic_attempts: pd.DataFrame) -> str:
    if topic_attempts.empty:
        return "Not enough data"
    recent_avg = topic_attempts.sort_values("submitted_at", ascending=False).head(3)["percentage"].mean()
    if recent_avg < 65:
        return "Poor"
    if recent_avg < 85:
        return "Needs Practice"
    return "Good"


def generate_recommendation(student_id: str) -> Optional[Dict]:
    """Generate a rule-based study recommendation from actual stored answers."""
    topic_df = calculate_topic_performance(student_id)
    if topic_df.empty:
        return None

    answers_df = answers_dataframe(student_id)
    attempts_df = performance_over_time(student_id)

    scored_topics = topic_df.copy()
    difficulty_weight = {"Easy": 1, "Medium": 2, "Hard": 3}
    difficulty_scores = []
    for _, row in scored_topics.iterrows():
        topic_answers = answers_df[(answers_df["topic"] == row["topic"]) & (answers_df["is_correct"] == False)]
        difficulty_score = sum(difficulty_weight.get(x, 1) for x in topic_answers.get("difficulty", []))
        difficulty_scores.append(difficulty_score)

    scored_topics["difficulty_score"] = difficulty_scores
    scored_topics["priority_score"] = (
        (100 - scored_topics["accuracy"]) * 2
        + scored_topics["incorrect_answers"] * 5
        + scored_topics["recent_mistakes"] * 3
        + scored_topics["difficulty_score"]
    )
    priority = scored_topics.sort_values(["priority_score", "accuracy"], ascending=[False, True]).iloc[0]

    topic_attempts = attempts_df[attempts_df["topic"] == priority["topic"]] if not attempts_df.empty else pd.DataFrame()
    recent_label = _recent_performance_label(topic_attempts)

    if priority["accuracy"] < 65:
        reason = f"Your performance in {priority['topic']} is below the 65% weakness threshold."
        action = "Review the basic concepts and complete 5 additional practice questions."
    elif priority["accuracy"] < 85:
        reason = f"Your performance in {priority['topic']} is between 65% and 84%, so it still needs practice."
        action = "Practice mixed medium-level questions and review every incorrect answer."
    else:
        reason = f"{priority['topic']} is currently strong, but it has the highest priority score among your attempted topics."
        action = "Maintain performance with a short revision quiz."

    return {
        "topic": priority["topic"],
        "subject": priority["subject"],
        "accuracy": float(priority["accuracy"]),
        "incorrect_answers": int(priority["incorrect_answers"]),
        "recent_performance": recent_label,
        "classification": priority["classification"],
        "reason": reason,
        "recommended_action": action,
    }
