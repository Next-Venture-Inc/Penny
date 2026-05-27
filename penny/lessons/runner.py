from penny.models.lesson import Lesson, LessonStep


class LessonRunner:
    """Walks through lesson steps one at a time."""

    def __init__(self, lesson: Lesson) -> None:
        self.lesson = lesson
        self._index = 0

    @property
    def current_step(self) -> LessonStep | None:
        if self._index < len(self.lesson.steps):
            return self.lesson.steps[self._index]
        return None

    @property
    def progress(self) -> tuple[int, int]:
        return self._index, len(self.lesson.steps)

    @property
    def complete(self) -> bool:
        return self._index >= len(self.lesson.steps)

    def advance(self) -> LessonStep | None:
        self._index += 1
        return self.current_step

    def reset(self) -> None:
        self._index = 0
