import pytest

from penny.lessons.loader import load_all_lessons, load_lesson, LessonParseError
from penny.lessons.runner import LessonRunner
from penny.models.lesson import Lesson, QuizQuestion, LessonStep


class TestLessonLoader:
    def test_load_all_lessons_returns_list(self):
        lessons = load_all_lessons()
        assert isinstance(lessons, list)
        assert len(lessons) == 11

    def test_all_lessons_have_required_fields(self):
        for lesson in load_all_lessons():
            assert lesson.id
            assert lesson.title
            assert lesson.description
            assert lesson.estimated_minutes > 0
            assert len(lesson.steps) > 0
            assert len(lesson.quiz) > 0

    def test_all_quizzes_have_4_options(self):
        for lesson in load_all_lessons():
            for q in lesson.quiz:
                assert len(q.options) == 4

    def test_all_correct_indices_valid(self):
        for lesson in load_all_lessons():
            for q in lesson.quiz:
                assert 0 <= q.correct <= 3

    def test_load_specific_lesson(self):
        lesson = load_lesson("01-how-markets-work")
        assert lesson.id == "01-how-markets-work"

    def test_load_nonexistent_raises(self):
        with pytest.raises(LessonParseError):
            load_lesson("99-does-not-exist")

    def test_no_eval_or_exec_in_content(self):
        for lesson in load_all_lessons():
            for step in lesson.steps:
                assert "eval(" not in step.content
                assert "exec(" not in step.content
                assert "__import__" not in step.content

    def test_lesson_ids_match_filenames(self):
        lessons = load_all_lessons()
        ids = {lesson.id for lesson in lessons}
        assert "01-how-markets-work" in ids
        assert "11-private-equity" in ids


class TestLessonRunner:
    def test_runner_starts_at_step_zero(self):
        lesson = load_lesson("01-how-markets-work")
        runner = LessonRunner(lesson)
        assert runner.progress == (0, len(lesson.steps))

    def test_advance_moves_to_next_step(self):
        lesson = load_lesson("01-how-markets-work")
        runner = LessonRunner(lesson)
        first = runner.current_step
        runner.advance()
        second = runner.current_step
        assert first is not second

    def test_complete_when_all_steps_done(self):
        lesson = load_lesson("01-how-markets-work")
        runner = LessonRunner(lesson)
        for _ in lesson.steps:
            runner.advance()
        assert runner.complete is True

    def test_reset_goes_back_to_start(self):
        lesson = load_lesson("01-how-markets-work")
        runner = LessonRunner(lesson)
        runner.advance()
        runner.advance()
        runner.reset()
        assert runner.progress == (0, len(lesson.steps))


class TestLessonModels:
    def test_quiz_question_rejects_wrong_option_count(self):
        with pytest.raises(Exception):
            QuizQuestion(
                question="test",
                options=["a", "b", "c"],
                correct=0,
                explanation="test",
            )

    def test_quiz_question_rejects_invalid_correct_index(self):
        with pytest.raises(Exception):
            QuizQuestion(
                question="test",
                options=["a", "b", "c", "d"],
                correct=4,
                explanation="test",
            )

    def test_valid_quiz_question_accepted(self):
        q = QuizQuestion(
            question="What is 1+1?",
            options=["1", "2", "3", "4"],
            correct=1,
            explanation="1 + 1 = 2.",
        )
        assert q.correct == 1
