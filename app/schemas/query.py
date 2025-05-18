from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import Query

class PaginationParams:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

class SortParams:
    def __init__(
        self,
        sort_by: Optional[str] = Query(default=None),
        order: Optional[str] = Query(default="asc", regex="^(asc|desc)$")
    ):
        self.sort_by = sort_by
        self.order = order

class HorseFilterParams:
    def __init__(
        self,
        breed: Optional[str] = None,
        min_age: Optional[int] = Query(default=None, ge=0),
        max_age: Optional[int] = Query(default=None, le=40),
        gender: Optional[str] = None,
        min_height: Optional[float] = Query(default=None, ge=0),
        max_height: Optional[float] = Query(default=None),
        location: Optional[str] = None,
    ):
        self.breed = breed
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.min_height = min_height
        self.max_height = max_height
        self.location = location

class MarketFilterParams:
    def __init__(
        self,
        min_price: Optional[float] = Query(default=None, ge=0),
        max_price: Optional[float] = Query(default=None, ge=0),
        location: Optional[str] = None,
        is_negotiable: Optional[bool] = None,
        status: Optional[str] = None,
    ):
        self.min_price = min_price
        self.max_price = max_price
        self.location = location
        self.is_negotiable = is_negotiable
        self.status = status

class RentalFilterParams:
    def __init__(
        self,
        min_price_per_day: Optional[float] = Query(default=None, ge=0),
        max_price_per_day: Optional[float] = Query(default=None, ge=0),
        location: Optional[str] = None,
        available_from: Optional[str] = None,
        available_to: Optional[str] = None,
        duration_type: Optional[str] = None,
    ):
        self.min_price_per_day = min_price_per_day
        self.max_price_per_day = max_price_per_day
        self.location = location
        self.available_from = available_from
        self.available_to = available_to
        self.duration_type = duration_type

class SearchParams:
    def __init__(
        self,
        q: Optional[str] = Query(default=None, min_length=3),
        search_in: Optional[List[str]] = Query(default=["name", "description"])
    ):
        self.q = q
        self.search_in = search_in 