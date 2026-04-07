__all__ = ["Filter", "FilterTest"]

from typing import Optional, List
from pydantic import field_validator

from mcaddon.core.base import BaseModel, Number
from .constants import FilterTestType


class FilterTest(BaseModel):
    test: Optional[FilterTestType] = None
    value: Optional[str | bool | Number] = None
    operator: Optional[int | str] = None
    subject: Optional[int | str] = None
    domain: Optional[str] = None

    @field_validator("test", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return FilterTestType.parse(v)


class Filter(FilterTest):
    all_of: Optional[List["Filter"]] = None
    any_of: Optional[List["Filter"]] = None
    none_of: Optional[List["Filter"]] = None
    other_with_families: Optional[str] = None
    AND: Optional[List["Filter"]] = None
    OR: Optional[List["Filter"]] = None
