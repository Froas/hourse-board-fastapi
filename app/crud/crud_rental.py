from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rental import RentalListing, RentalBooking, RentalStatus, BookingStatus
from app.schemas.rental import (
    RentalListingCreate,
    RentalListingUpdate,
    RentalBookingCreate,
    RentalBookingUpdate,
)

class CRUDRentalListing(CRUDBase[RentalListing, RentalListingCreate, RentalListingUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: RentalListingCreate, owner_id: int
    ) -> RentalListing:
        obj_in_data = obj_in.dict()
        db_obj = RentalListing(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[RentalListing]:
        return (
            db.query(self.model)
            .filter(RentalListing.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_available_listings(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[RentalListing]:
        return (
            db.query(self.model)
            .filter(RentalListing.status == RentalStatus.AVAILABLE)
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDRentalBooking(CRUDBase[RentalBooking, RentalBookingCreate, RentalBookingUpdate]):
    def create_with_renter(
        self, db: Session, *, obj_in: RentalBookingCreate, renter_id: int
    ) -> RentalBooking:
        # Get the rental listing to calculate total price
        listing = db.query(RentalListing).filter(RentalListing.id == obj_in.rental_listing_id).first()
        if not listing:
            raise ValueError("Rental listing not found")

        # Calculate total price based on duration type
        duration_type = obj_in.duration_type
        if duration_type.value == "Hourly" and listing.price_per_hour:
            total_price = listing.price_per_hour
        elif duration_type.value == "Daily" and listing.price_per_day:
            total_price = listing.price_per_day
        elif duration_type.value == "Weekly" and listing.price_per_week:
            total_price = listing.price_per_week
        elif duration_type.value == "Monthly" and listing.price_per_month:
            total_price = listing.price_per_month
        else:
            raise ValueError(f"Price not available for {duration_type.value} rentals")

        # Create booking
        obj_in_data = obj_in.dict()
        db_obj = RentalBooking(
            **obj_in_data,
            renter_id=renter_id,
            total_price=total_price,
            status=BookingStatus.PENDING
        )
        db.add(db_obj)
        
        # Update listing status
        listing.status = RentalStatus.BOOKED
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_renter(
        self, db: Session, *, renter_id: int, skip: int = 0, limit: int = 100
    ) -> List[RentalBooking]:
        return (
            db.query(self.model)
            .filter(RentalBooking.renter_id == renter_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_listing(
        self, db: Session, *, listing_id: int, skip: int = 0, limit: int = 100
    ) -> List[RentalBooking]:
        return (
            db.query(self.model)
            .filter(RentalBooking.rental_listing_id == listing_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

rental_listing = CRUDRentalListing(RentalListing)
rental_booking = CRUDRentalBooking(RentalBooking) 