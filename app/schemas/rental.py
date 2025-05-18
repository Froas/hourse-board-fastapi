from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import datetime
from app.models.rental import RentalDuration, RentalStatus, BookingStatus
from .horse import Horse
from .user import User

class RentalListingBase(BaseModel):
    price_per_hour: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_day: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_week: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_month: Optional[Annotated[float, Field(gt=0)]] = None
    description: Optional[str] = None
    location: str
    requirements: Optional[str] = None
    available_durations: str  # Comma-separated RentalDuration values

class RentalListingCreate(RentalListingBase):
    horse_id: int

class RentalListingUpdate(BaseModel):
    price_per_hour: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_day: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_week: Optional[Annotated[float, Field(gt=0)]] = None
    price_per_month: Optional[Annotated[float, Field(gt=0)]] = None
    description: Optional[str] = None
    location: Optional[str] = None
    requirements: Optional[str] = None
    available_durations: Optional[str] = None
    status: Optional[RentalStatus] = None

class RentalListing(RentalListingBase):
    id: int
    horse_id: int
    owner_id: int
    status: RentalStatus
    created_at: datetime
    updated_at: datetime
    horse: Optional[Horse] = None
    owner: Optional[User] = None

    class Config:
        from_attributes = True

class RentalBookingBase(BaseModel):
    start_date: datetime
    end_date: datetime
    duration_type: RentalDuration
    special_requests: Optional[str] = None

class RentalBookingCreate(RentalBookingBase):
    rental_listing_id: int

class RentalBookingUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    special_requests: Optional[str] = None
    status: Optional[BookingStatus] = None
    payment_status: Optional[str] = None

class RentalBooking(RentalBookingBase):
    id: int
    rental_listing_id: int
    renter_id: int
    total_price: float
    status: BookingStatus
    payment_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    rental_listing: Optional[RentalListing] = None
    renter: Optional[User] = None

    class Config:
        from_attributes = True 