from typing import Optional

import httpx

from app import config


class ContactsServiceError(Exception):
    """The Contacts service did not answer correctly."""


def fetch_contacts(filters: dict, auth_header: Optional[str] = None) -> list:
    """Call the Contacts service: GET /api/contacts with only the filters that have a value."""
    params = {key: value for key, value in filters.items() if value}
    headers = {"Authorization": auth_header} if auth_header else {}

    try:
        response = httpx.get(
            f"{config.CONTACTS_SERVICE_URL}/api/contacts",
            params=params,
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError):
        raise ContactsServiceError("Contacts service unavailable") from None

    if not isinstance(data, list):
        raise ContactsServiceError("Unexpected response from Contacts service")
    return data