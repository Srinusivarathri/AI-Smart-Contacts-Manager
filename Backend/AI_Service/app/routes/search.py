from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from app.llm import LLMConfigError, LLMError
from app.schemas import ParseResponse, SearchRequest, SearchResponse
from app.services.contacts_client import ContactsServiceError, fetch_contacts
from app.services.query_parser import InvalidQueryError, QueryParseError, parse_query

router = APIRouter()


def _filters_or_http_error(query: str) -> dict:
    try:
        return parse_query(query)
    except InvalidQueryError:
        raise HTTPException(status_code=422, detail="Query is empty or too long") from None
    except LLMConfigError:
        raise HTTPException(status_code=503, detail="AI service is not configured") from None
    except (LLMError, QueryParseError):
        raise HTTPException(status_code=502, detail="Could not understand the query right now") from None


@router.post("/parse-query", response_model=ParseResponse)
def parse_query_endpoint(body: SearchRequest):
    """AISCM-4: natural language -> filters (no Contacts service call)."""
    filters = _filters_or_http_error(body.query)
    return {"query": body.query, "filters": filters}


@router.post("/search", response_model=SearchResponse)
def search_contacts(body: SearchRequest, authorization: Optional[str] = Header(default=None)):
    """AISCM-5: natural language -> filters -> Contacts service -> contacts."""
    filters = _filters_or_http_error(body.query)
    try:
        results = fetch_contacts(filters, authorization)
    except ContactsServiceError:
        raise HTTPException(status_code=502, detail="Contacts service unavailable") from None
    return {
        "query": body.query,
        "filters": filters,
        "count": len(results),
        "results": results,
    }