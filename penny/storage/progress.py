import sqlite3
from pathlib import Path

from penny.config import config


def _get_conn() -> sqlite3.Connection:
    db_path = Path(config.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    _init_schema(conn)
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            lesson_id TEXT PRIMARY KEY,
            completed_steps INTEGER DEFAULT 0,
            total_steps INTEGER DEFAULT 0,
            completed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS quiz_results (
            lesson_id TEXT,
            score INTEGER,
            total INTEGER,
            taken_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (lesson_id, taken_at)
        );
    """)
    conn.commit()


def mark_lesson_step(lesson_id: str, step: int, total: int) -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO lesson_progress (lesson_id, completed_steps, total_steps)
            VALUES (?, ?, ?)
            ON CONFLICT(lesson_id) DO UPDATE SET
                completed_steps = MAX(completed_steps, excluded.completed_steps),
                total_steps = excluded.total_steps
            """,
            (lesson_id, step, total),
        )


def mark_lesson_complete(lesson_id: str, total_steps: int) -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO lesson_progress (lesson_id, completed_steps, total_steps, completed_at)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(lesson_id) DO UPDATE SET
                completed_steps = excluded.total_steps,
                completed_at = datetime('now')
            """,
            (lesson_id, total_steps, total_steps),
        )


def save_quiz_result(lesson_id: str, score: int, total: int) -> None:
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO quiz_results (lesson_id, score, total) VALUES (?, ?, ?)",
            (lesson_id, score, total),
        )


def get_progress() -> dict[str, dict]:
    with _get_conn() as conn:
        rows = conn.execute("SELECT * FROM lesson_progress").fetchall()
        return {
            row[0]: {
                "completed_steps": row[1],
                "total_steps": row[2],
                "completed_at": row[3],
            }
            for row in rows
        }
