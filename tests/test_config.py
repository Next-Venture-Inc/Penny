import os

import pytest

from penny.config import Config


def test_from_env_never_raises_with_no_env(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("PENNY_CACHE_DIR", raising=False)
    monkeypatch.delenv("PENNY_DB_PATH", raising=False)
    config = Config.from_env()
    assert config is not None


def test_api_key_is_none_when_absent(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = Config.from_env()
    assert config.anthropic_api_key is None


def test_ai_disabled_when_key_absent(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = Config.from_env()
    assert config.ai_enabled is False


def test_ai_enabled_when_key_present(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-value")
    config = Config.from_env()
    assert config.ai_enabled is True
    assert config.anthropic_api_key == "test-key-value"


def test_repr_does_not_expose_api_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-supersecret")
    config = Config.from_env()
    representation = repr(config)
    assert "sk-ant-supersecret" not in representation
    assert "supersecret" not in representation


def test_custom_cache_dir(monkeypatch):
    monkeypatch.setenv("PENNY_CACHE_DIR", "/tmp/test-penny-cache")
    config = Config.from_env()
    assert config.data_cache_dir == "/tmp/test-penny-cache"


def test_custom_db_path(monkeypatch):
    monkeypatch.setenv("PENNY_DB_PATH", "/tmp/test-penny.db")
    config = Config.from_env()
    assert config.db_path == "/tmp/test-penny.db"
