import pytest

from app import config, llm


def test_ask_llm_returns_the_text(install_fake_openai):
    fake = install_fake_openai(reply="hello")

    assert llm.ask_llm("system text", "user text") == "hello"
    assert fake.last_init["base_url"] == "https://gateway.test/v1"
    assert fake.last_call["model"] == "test/model"
    assert fake.last_call["messages"] == [
        {"role": "system", "content": "system text"},
        {"role": "user", "content": "user text"},
    ]


def test_missing_key_raises_config_error(monkeypatch, install_fake_openai):
    install_fake_openai(reply="x")
    monkeypatch.setattr(config, "AI_GATEWAY_API_KEY", None)

    with pytest.raises(llm.LLMConfigError):
        llm.ask_llm("s", "u")


def test_missing_model_raises_config_error(monkeypatch, install_fake_openai):
    install_fake_openai(reply="x")
    monkeypatch.setattr(config, "LLM_MODEL", None)

    with pytest.raises(llm.LLMConfigError):
        llm.ask_llm("s", "u")


def test_provider_error_is_generic_and_hides_the_key(install_fake_openai, fake_key, caplog):
    install_fake_openai(error=RuntimeError(f"Incorrect API key provided: {fake_key}"))

    with pytest.raises(llm.LLMError) as exc_info:
        llm.ask_llm("s", "u")

    assert fake_key not in str(exc_info.value)
    assert exc_info.value.__cause__ is None
    assert exc_info.value.__suppress_context__ is True
    assert fake_key not in caplog.text
    assert "RuntimeError" in caplog.text


def test_empty_reply_raises_llm_error(install_fake_openai):
    install_fake_openai(reply="")

    with pytest.raises(llm.LLMError):
        llm.ask_llm("s", "u")