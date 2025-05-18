from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import rental_listing, rental_booking
from app.models.user import User
from app.schemas.rental import (
    RentalListing,
    RentalListingCreate,
    RentalListingUpdate,
    RentalBooking,
    RentalBookingCreate,
    RentalBookingUpdate,
)

router = APIRouter()

@router.get("/listings", response_model=List[RentalListing])
def list_listings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all available rental listings.
    """
    listings = rental_listing.get_available_listings(db, skip=skip, limit=limit)
    return listings

@router.post("/listings", response_model=RentalListing)
def create_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_in: RentalListingCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new rental listing.
    """
    listing = rental_listing.create_with_owner(
        db=db, obj_in=listing_in, owner_id=current_user.id
    )
    return listing

@router.get("/my-listings", response_model=List[RentalListing])
def list_my_listings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve rental listings created by current user.
    """
    listings = rental_listing.get_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return listings

@router.get("/listings/{listing_id}", response_model=RentalListing)
def get_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get rental listing by ID.
    """
    listing = rental_listing.get(db=db, id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Rental listing not found")
    return listing

@router.put("/listings/{listing_id}", response_model=RentalListing)
def update_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
    listing_in: RentalListingUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a rental listing.
    """
    listing = rental_listing.get(db=db, id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Rental listing not found")
    if listing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    listing = rental_listing.update(db=db, db_obj=listing, obj_in=listing_in)
    return listing

@router.post("/bookings", response_model=RentalBooking)
def create_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_in: RentalBookingCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a booking for a rental listing.
    """
    listing = rental_listing.get(db=db, id=booking_in.rental_listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Rental listing not found")
    if listing.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot book your own listing")
    booking = rental_booking.create_with_renter(
        db=db, obj_in=booking_in, renter_id=current_user.id
    )
    return booking

@router.get("/my-bookings", response_model=List[RentalBooking])
def list_my_bookings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve bookings made by current user.
    """
    bookings = rental_booking.get_by_renter(
        db=db, renter_id=current_user.id, skip=skip, limit=limit
    )
    return bookings

@router.put("/bookings/{booking_id}", response_model=RentalBooking)
def update_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_id: int,
    booking_in: RentalBookingUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a booking.
    """
    booking = rental_booking.get(db=db, id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.renter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    booking = rental_booking.update(db=db, db_obj=booking, obj_in=booking_in)
    return booking 