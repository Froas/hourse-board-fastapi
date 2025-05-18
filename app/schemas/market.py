from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import datetime
from app.models.market import ListingStatus
from .horse import Horse
from .user import User

class MarketListingBase(BaseModel):
    price: Annotated[float, Field(gt=0)]
    description: Optional[str] = None
    is_negotiable: bool = True
    location: str

class MarketListingCreate(MarketListingBase):
    horse_id: int

class MarketListingUpdate(BaseModel):
    price: Optional[Annotated[float, Field(gt=0)]] = None
    description: Optional[str] = None
    is_negotiable: Optional[bool] = None
    location: Optional[str] = None
    status: Optional[ListingStatus] = None

class MarketListing(MarketListingBase):
    id: int
    horse_id: int
    seller_id: int
    status: ListingStatus
    created_at: datetime
    updated_at: datetime
    horse: Optional[Horse] = None
    seller: Optional[User] = None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    final_price: Annotated[float, Field(gt=0)]
    payment_method: str
    payment_status: str
    transaction_notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    listing_id: int
    buyer_id: int

class Transaction(TransactionBase):
    id: int
    listing_id: int
    buyer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 