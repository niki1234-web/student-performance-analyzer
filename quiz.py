import random
from typing import Dict, List

from database import list_questions


def get_quiz_questions(subject: str, topic: str, num_questions: int) -> List[Dict]:
    questions = list_questions(subject=subject, topic=topic)
    if not questions:
        return []
    random.shuffle(questions)
    return questions[: min(num_questions, len(questions))]


def grade_quiz(questions: List[Dict], selected_answers: Dict[str, str]) -> List[Dict]:
    answer_rows = []
    for q in questions:
        qid = str(q["_id"])
        student_answer = selected_answers.get(qid, "No answer")
        correct_answer = q["correct_answer"]
        answer_rows.append(
            {
                "question_id": qid,
                "question": q["question"],
                "topic": q["topic"],
                "student_answer": student_answer,
                "correct_answer": correct_answer,
                "is_correct": student_answer == correct_answer,
                "difficulty": q.get("difficulty", "Medium"),
            }
        )
    return answer_rows
