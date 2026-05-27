from penny.config import config
from penny.tutor.claude_tutor import AITutor, TutorUnavailable


def get_followup_question(lesson_id: str, missed_topic: str) -> str | None:
    """Generate a follow-up question for a missed topic using AI.

    Returns None if AI is unavailable — quiz proceeds with built-in questions only.
    """
    if not config.ai_enabled:
        return None

    tutor = AITutor()
    try:
        prompt = (
            f"A student just got a quiz question wrong about '{missed_topic}' "
            f"in lesson '{lesson_id}'. Write one short follow-up question (plain English, "
            f"simple multiple choice) to help them understand the concept. "
            f"Keep it under 30 words."
        )
        return tutor.ask(prompt, [])
    except TutorUnavailable:
        return None
