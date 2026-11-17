from typing import Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=300)


class Filters(BaseModel):
    name: Optional[str] = None
    relation: Optional[str] = None
    address: Optional[str] = None


class ParseResponse(BaseModel):
    query: str
    filters: Filters


class SearchResponse(BaseModel):
    query: str
    filters: Filters
    count: int
    results: list[dict]