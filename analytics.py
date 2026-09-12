from typing import Dict, List, Optional

import pandas as pd

from database import get_answers, get_attempts
from models import classification_label, classify_accuracy


def attempts_dataframe(student_id: str) -> pd.DataFrame:
    attempts = get_attempts(student_id)
    if not attempts:
        return pd.DataFrame()
    df = pd.DataFrame(attempts)
    if "submitted_at" in df.columns:
        df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    return df


def answers_dataframe(student_id: str) -> pd.DataFrame:
    answers = get_answers(student_id)
    if not answers:
        return pd.DataFrame()
    df = pd.DataFrame(answers)
    if "submitted_at" in df.columns:
        df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    return df


def get_overall_metrics(student_id: str) -> Dict:
    attempts_df = attempts_dataframe(student_id)
    answers_df = answers_dataframe(student_id)

    if attempts_df.empty or answers_df.empty:
        return {
            "overall_accuracy": 0,
            "quizzes_completed": 0,
            "strongest_subject": "Not enough data",
            "weakest_subject": "Not enough data",
            "total_questions": 0,
        }

    total_questions = len(answers_df)
    correct = int(answers_df["is_correct"].sum())
    overall_accuracy = round((correct / total_questions) * 100, 2) if total_questions else 0

    subject_perf = (
        answers_df.groupby("subject")["is_correct"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )

    return {
        "overall_accuracy": overall_accuracy,
        "quizzes_completed": len(attempts_df),
        "strongest_subject": subject_perf.index[0] if not subject_perf.empty else "Not enough data",
        "weakest_subject": subject_perf.index[-1] if not subject_perf.empty else "Not enough data",
        "total_questions": total_questions,
    }


def calculate_topic_performance(student_id: str) -> pd.DataFrame:
    answers_df = answers_dataframe(student_id)
    if answers_df.empty:
        return pd.DataFrame(
            columns=[
                "subject",
                "topic",
                "total_questions",
                "correct_answers",
                "incorrect_answers",
                "accuracy",
                "recent_mistakes",
                "classification",
                "classification_text",
            ]
        )

    grouped = answers_df.groupby(["subject", "topic"])
    rows = []
    for (subject, topic), group in grouped:
        total = len(group)
        correct = int(group["is_correct"].sum())
        incorrect = total - correct
        accuracy = round((correct / total) * 100, 2) if total else 0
        recent_group = group.sort_values("submitted_at", ascending=False).head(10)
        recent_mistakes = int((~recent_group["is_correct"]).sum())
        rows.append(
            {
                "subject": subject,
                "topic": topic,
                "total_questions": total,
                "correct_answers": correct,
                "incorrect_answers": incorrect,
                "accuracy": accuracy,
                "recent_mistakes": recent_mistakes,
                "classification": classify_accuracy(accuracy),
                "classification_text": classification_label(accuracy),
            }
        )

    df = pd.DataFrame(rows)
    return df.sort_values(["accuracy", "incorrect_answers"], ascending=[True, False]).reset_index(drop=True)


def get_weak_topics(student_id: str, limit: Optional[int] = None) -> pd.DataFrame:
    df = calculate_topic_performance(student_id)
    if df.empty:
        return df
    weak_df = df[df["accuracy"] < 85].sort_values(["accuracy", "incorrect_answers"], ascending=[True, False])
    return weak_df.head(limit) if limit else weak_df


def detect_repeated_mistakes(student_id: str) -> pd.DataFrame:
    attempts_df = attempts_dataframe(student_id)
    if attempts_df.empty:
        return pd.DataFrame()

    rows: List[Dict] = []
    for topic, group in attempts_df.groupby("topic"):
        recent = group.sort_values("submitted_at", ascending=False).head(3).sort_values("submitted_at")
        if len(recent) < 2:
            continue
        poor_attempts = recent[recent["percentage"] < 65]
        avg_accuracy = round(recent["percentage"].mean(), 2)
        if len(poor_attempts) >= 2 or avg_accuracy < 65:
            rows.append(
                {
                    "subject": recent.iloc[-1]["subject"],
                    "topic": topic,
                    "attempts": [f"{int(r.correct_answers)}/{int(r.total_questions)}" for _, r in recent.iterrows()],
                    "average_accuracy": avg_accuracy,
                    "message": f"You have repeatedly struggled with {topic} across your recent attempts.",
                }
            )
    return pd.DataFrame(rows).sort_values("average_accuracy") if rows else pd.DataFrame()


def subject_performance(student_id: str) -> pd.DataFrame:
    answers_df = answers_dataframe(student_id)
    if answers_df.empty:
        return pd.DataFrame(columns=["subject", "accuracy"])
    return (
        answers_df.groupby("subject")["is_correct"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index(name="accuracy")
        .sort_values("accuracy", ascending=False)
    )


def performance_over_time(student_id: str) -> pd.DataFrame:
    attempts_df = attempts_dataframe(student_id)
    if attempts_df.empty:
        return pd.DataFrame(columns=["submitted_at", "subject", "topic", "percentage", "score"])
    return attempts_df.sort_values("submitted_at")[["submitted_at", "subject", "topic", "percentage", "score"]]


def classification_distribution(student_id: str) -> pd.DataFrame:
    topic_df = calculate_topic_performance(student_id)
    if topic_df.empty:
        return pd.DataFrame(columns=["classification_text", "count"])
    order = ["Weak", "Needs Practice", "Strong"]
    dist = topic_df["classification_text"].value_counts().reindex(order, fill_value=0).reset_index()
    dist.columns = ["classification_text", "count"]
    return dist
