import httpx
import pytest

from app.services import contacts_client as cc


class FakeResponse:
    def __init__(self, data=None, json_error=False, status_error=False):
        self.data = data
        self.json_error = json_error
        self.status_error = status_error

    def raise_for_status(self):
        if self.status_error:
            raise httpx.HTTPStatusError(
                "bad status",
                request=httpx.Request("GET", "http://contacts.test"),
                response=httpx.Response(500),
            )

    def json(self):
        if self.json_error:
            raise ValueError("not json")
        return self.data


def test_sends_only_filters_that_have_a_value(monkeypatch):
    captured = {}

    def fake_get(url, params=None, headers=None, timeout=None):
        captured.update(url=url, params=params, headers=headers)
        return FakeResponse([{"id": 1}])

    monkeypatch.setattr(cc.httpx, "get", fake_get)

    result = cc.fetch_contacts({"name": None, "relation": "friend", "address": "hyd"}, "Bearer abc")

    assert result == [{"id": 1}]
    assert captured["url"] == "http://contacts.test/api/contacts"
    assert captured["params"] == {"relation": "friend", "address": "hyd"}
    assert captured["headers"] == {"Authorization": "Bearer abc"}


def test_no_authorization_header_when_none_given(monkeypatch):
    captured = {}

    def fake_get(url, params=None, headers=None, timeout=None):
        captured["headers"] = headers
        return FakeResponse([])

    monkeypatch.setattr(cc.httpx, "get", fake_get)

    assert cc.fetch_contacts({"name": None, "relation": None, "address": None}) == []
    assert captured["headers"] == {}


def test_connection_error_becomes_contacts_service_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise httpx.ConnectError("down")

    monkeypatch.setattr(cc.httpx, "get", fake_get)

    with pytest.raises(cc.ContactsServiceError):
        cc.fetch_contacts({"name": "sri"})


def test_bad_status_becomes_contacts_service_error(monkeypatch):
    monkeypatch.setattr(cc.httpx, "get", lambda *a, **k: FakeResponse(status_error=True))

    with pytest.raises(cc.ContactsServiceError):
        cc.fetch_contacts({"name": "sri"})


def test_invalid_json_becomes_contacts_service_error(monkeypatch):
    monkeypatch.setattr(cc.httpx, "get", lambda *a, **k: FakeResponse(json_error=True))

    with pytest.raises(cc.ContactsServiceError):
        cc.fetch_contacts({"name": "sri"})


def test_non_list_response_is_rejected(monkeypatch):
    monkeypatch.setattr(cc.httpx, "get", lambda *a, **k: FakeResponse({"message": "oops"}))

    with pytest.raises(cc.ContactsServiceError):
        cc.fetch_contacts({"name": "sri"})