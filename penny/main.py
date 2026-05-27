import typer
from rich.console import Console

app = typer.Typer(
    name="penny",
    help="Penny by Next Venture — investment education for everyone.",
    add_completion=False,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Launch the Penny interactive learning platform."""
    if ctx.invoked_subcommand is None:
        _launch_tui()


def _launch_tui() -> None:
    from penny.ui.app import PennyApp

    PennyApp().run()


@app.command()
def learn(lesson_id: str | None = typer.Argument(None)) -> None:
    """Start a specific lesson or browse all lessons."""
    from penny.ui.app import PennyApp

    PennyApp(start_screen="lessons", lesson_id=lesson_id).run()


@app.command()
def quiz(lesson_id: str | None = typer.Argument(None)) -> None:
    """Take a quiz for a specific lesson."""
    from penny.ui.app import PennyApp

    PennyApp(start_screen="quiz", lesson_id=lesson_id).run()


@app.command()
def tutor() -> None:
    """Open the AI tutor chat (requires ANTHROPIC_API_KEY)."""
    from penny.ui.app import PennyApp

    PennyApp(start_screen="tutor").run()
