from typing import Literal

from pydantic import BaseModel, field_validator


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct: int
    explanation: str

    @field_validator("options")
    @classmethod
    def four_options(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("exactly 4 options required")
        return v

    @field_validator("correct")
    @classmethod
    def valid_index(cls, v: int) -> int:
        if v not in range(4):
            raise ValueError("correct must be 0-3")
        return v


class LessonStep(BaseModel):
    type: Literal["text", "concept", "example", "callout", "calculator"]
    content: str
    calculator: str | None = None

    @field_validator("calculator")
    @classmethod
    def calculator_only_when_needed(cls, v: str | None, info: object) -> str | None:
        return v


class Lesson(BaseModel):
    id: str
    title: str
    description: str
    estimated_minutes: int
    tags: list[str]
    steps: list[LessonStep]
    quiz: list[QuizQuestion]
