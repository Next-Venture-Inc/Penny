from pathlib import Path

import yaml

from penny.models.lesson import Lesson

CONTENT_DIR = Path(__file__).parent / "content"


class LessonParseError(Exception):
    pass


def load_lesson(lesson_id: str) -> Lesson:
    """Load and validate a lesson from its YAML file."""
    path = CONTENT_DIR / f"{lesson_id}.yaml"
    if not path.exists():
        raise LessonParseError(f"Lesson file not found: {path}")

    try:
        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise LessonParseError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise LessonParseError(f"Lesson file must be a YAML mapping: {path}")

    try:
        return Lesson.model_validate(data)
    except Exception as exc:
        raise LessonParseError(f"Lesson validation failed for {path}: {exc}") from exc


def load_all_lessons() -> list[Lesson]:
    """Load all lessons sorted by filename."""
    lessons = []
    for yaml_file in sorted(CONTENT_DIR.glob("*.yaml")):
        lesson_id = yaml_file.stem
        try:
            lessons.append(load_lesson(lesson_id))
        except LessonParseError:
            pass
    return lessons
