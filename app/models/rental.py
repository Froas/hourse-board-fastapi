from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, Text, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class RentalDuration(enum.Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"

class RentalStatus(enum.Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
    UNAVAILABLE = "Unavailable"

class BookingStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class RentalListing(Base, TimestampMixin):
    __tablename__ = "rental_listings"

    id = Column(Integer, primary_key=True, index=True)
    horse_id = Column(Integer, ForeignKey("horses.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price_per_hour = Column(Float)
    price_per_day = Column(Float)
    price_per_week = Column(Float)
    price_per_month = Column(Float)
    description = Column(Text)
    status = Column(Enum(RentalStatus), default=RentalStatus.AVAILABLE)
    location = Column(String)
    requirements = Column(Text)
    available_durations = Column(String)  # Stored as comma-separated RentalDuration values
    
    # Relationships
    horse = relationship("Horse", back_populates="rental_listing")
    owner = relationship("User", back_populates="rental_listings")
    bookings = relationship("RentalBooking", back_populates="rental_listing")

class RentalBooking(Base, TimestampMixin):
    __tablename__ = "rental_bookings"

    id = Column(Integer, primary_key=True, index=True)
    rental_listing_id = Column(Integer, ForeignKey("rental_listings.id"), nullable=False)
    renter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration_type = Column(Enum(RentalDuration), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = Column(Text)
    payment_status = Column(String)
    
    # Relationships
    rental_listing = relationship("RentalListing", back_populates="bookings")
    renter = relationship("User", back_populates="rental_bookings") 