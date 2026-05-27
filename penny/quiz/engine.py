from penny.models.lesson import Lesson, QuizQuestion
from penny.models.quiz import QuizState


class QuizEngine:
    """Runs a quiz for a lesson, tracking state."""

    def __init__(self, lesson: Lesson) -> None:
        self.lesson = lesson
        self.state = QuizState(
            lesson_id=lesson.id,
            total_questions=len(lesson.quiz),
        )

    @property
    def current_question(self) -> QuizQuestion | None:
        if self.state.complete:
            return None
        return self.lesson.quiz[self.state.current_index]

    def answer(self, choice: int) -> tuple[bool, str]:
        """Submit an answer. Returns (is_correct, explanation)."""
        q = self.current_question
        if q is None:
            raise RuntimeError("Quiz is already complete.")
        is_correct = choice == q.correct
        if is_correct:
            self.state.score += 1
        self.state.answers.append(choice)
        self.state.current_index += 1
        return is_correct, q.explanation

    @property
    def summary(self) -> str:
        pct = self.state.percent_correct
        return (
            f"You got {self.state.score} out of {self.state.total_questions} right "
            f"({pct:.0f}%). "
            + ("Great work!" if pct >= 80 else "Keep practicing!")
        )
