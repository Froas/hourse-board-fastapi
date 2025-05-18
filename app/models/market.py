from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, Text, Boolean, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class ListingStatus(enum.Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"
    CANCELLED = "Cancelled"

class MarketListing(Base, TimestampMixin):
    __tablename__ = "market_listings"

    id = Column(Integer, primary_key=True, index=True)
    horse_id = Column(Integer, ForeignKey("horses.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE)
    is_negotiable = Column(Boolean, default=True)
    location = Column(String)
    
    # Relationships
    horse = relationship("Horse", back_populates="market_listing")
    seller = relationship("User", back_populates="market_listings")

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("market_listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    final_price = Column(Float, nullable=False)
    payment_status = Column(String)
    payment_method = Column(String)
    transaction_notes = Column(Text) 