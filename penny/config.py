import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str | None
    ai_enabled: bool
    data_cache_dir: str
    db_path: str

    @classmethod
    def from_env(cls) -> "Config":
        key = os.environ.get("ANTHROPIC_API_KEY")
        return cls(
            anthropic_api_key=key,
            ai_enabled=bool(key),
            data_cache_dir=os.environ.get(
                "PENNY_CACHE_DIR",
                os.path.expanduser("~/.penny/cache"),
            ),
            db_path=os.environ.get(
                "PENNY_DB_PATH",
                os.path.expanduser("~/.penny/progress.db"),
            ),
        )

    def __repr__(self) -> str:
        return (
            f"Config(ai_enabled={self.ai_enabled}, "
            f"data_cache_dir={self.data_cache_dir!r}, "
            f"db_path={self.db_path!r})"
        )


# Module-level singleton — import this everywhere, never re-read env
config = Config.from_env()
