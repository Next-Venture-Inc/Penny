from dataclasses import dataclass, field


@dataclass
class QuizState:
    lesson_id: str
    total_questions: int
    current_index: int = 0
    answers: list[int] = field(default_factory=list)
    score: int = 0

    @property
    def complete(self) -> bool:
        return self.current_index >= self.total_questions

    @property
    def percent_correct(self) -> float:
        if not self.answers:
            return 0.0
        return (self.score / len(self.answers)) * 100
