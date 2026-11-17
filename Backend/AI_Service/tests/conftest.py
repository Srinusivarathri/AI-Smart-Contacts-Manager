from types import SimpleNamespace

import pytest

from app import config, llm

FAKE_KEY = "sk-FAKE-KEY-123"


@pytest.fixture(autouse=True)
def fake_settings(monkeypatch):
    """Every test uses fake settings, so no test touches a real key or a real service."""
    monkeypatch.setattr(config, "AI_GATEWAY_API_KEY", FAKE_KEY)
    monkeypatch.setattr(config, "AI_GATEWAY_BASE_URL", "https://gateway.test/v1")
    monkeypatch.setattr(config, "LLM_MODEL", "test/model")
    monkeypatch.setattr(config, "CONTACTS_SERVICE_URL", "http://contacts.test")


@pytest.fixture
def fake_key():
    return FAKE_KEY


@pytest.fixture
def install_fake_openai(monkeypatch):
    """Replace the OpenAI client in app.llm with a fake one (no network)."""

    def _install(reply=None, error=None):
        class FakeOpenAI:
            last_init = None
            last_call = None

            def __init__(self, **kwargs):
                FakeOpenAI.last_init = kwargs
                self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

            def _create(self, **kwargs):
                FakeOpenAI.last_call = kwargs
                if error:
                    raise error
                message = SimpleNamespace(content=reply)
                return SimpleNamespace(choices=[SimpleNamespace(message=message)])

        monkeypatch.setattr(llm, "OpenAI", FakeOpenAI)
        return FakeOpenAI

    return _install