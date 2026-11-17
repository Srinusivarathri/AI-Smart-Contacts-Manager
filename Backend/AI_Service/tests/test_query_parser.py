import pytest

from app.services import query_parser as qp


def test_extract_json_plain():
    assert qp.extract_json('{"name": "sri"}') == {"name": "sri"}


def test_extract_json_inside_code_fence():
    text = '```json\n{"relation": "friend"}\n```'
    assert qp.extract_json(text) == {"relation": "friend"}


def test_extract_json_with_words_around():
    text = 'Sure! Here you go: {"address": "Hyderabad"} Hope this helps.'
    assert qp.extract_json(text) == {"address": "Hyderabad"}


def test_extract_json_without_json_raises():
    with pytest.raises(qp.QueryParseError):
        qp.extract_json("no json here")


def test_extract_json_not_an_object_raises():
    with pytest.raises(qp.QueryParseError):
        qp.extract_json("[1, 2, 3]")


def test_validate_filters_cleans_values():
    raw = {"name": "  Sri ", "relation": "FRIEND", "address": "", "extra": "ignored"}
    assert qp.validate_filters(raw) == {"name": "Sri", "relation": "friend", "address": None}


def test_validate_filters_drops_null_like_and_wrong_types():
    raw = {"name": "null", "relation": 5, "address": ["Hyderabad"]}
    assert qp.validate_filters(raw) == {"name": None, "relation": None, "address": None}


def test_validate_filters_drops_very_long_values():
    raw = {"name": "x" * 500, "relation": None, "address": None}
    assert qp.validate_filters(raw)["name"] is None


def test_validate_filters_missing_keys_become_none():
    assert qp.validate_filters({}) == {"name": None, "relation": None, "address": None}


def test_parse_query_happy_path(monkeypatch):
    calls = {}

    def fake_ask(system_prompt, user_prompt):
        calls["user"] = user_prompt
        return '{"name": null, "relation": "friend", "address": "Hyderabad"}'

    monkeypatch.setattr(qp, "ask_llm", fake_ask)

    result = qp.parse_query("friends in Hyderabad")

    assert result == {"name": None, "relation": "friend", "address": "Hyderabad"}
    assert calls["user"] == "<query>friends in Hyderabad</query>"


def test_parse_query_ignores_extra_keys_from_the_llm(monkeypatch):
    monkeypatch.setattr(
        qp, "ask_llm", lambda s, u: '{"name": "sri", "relation": null, "address": null, "drop": "table"}'
    )
    assert qp.parse_query("sri") == {"name": "sri", "relation": None, "address": None}


@pytest.mark.parametrize("query", ["", "   ", "a" * 301])
def test_parse_query_rejects_empty_or_too_long(monkeypatch, query):
    monkeypatch.setattr(qp, "ask_llm", lambda s, u: "{}")
    with pytest.raises(qp.InvalidQueryError):
        qp.parse_query(query)