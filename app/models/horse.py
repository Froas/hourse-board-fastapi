from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base

class Horse(Base):
    __tablename__ = "horses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    breed = Column(String(100))
    age = Column(Integer)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="horses")
    images = relationship("HorseImage", back_populates="horse", cascade="all, delete-orphan")
    market_listings = relationship("MarketListing", back_populates="horse")
    rental_listings = relationship("RentalListing", back_populates="horse")


class HorseImage(Base):
    __tablename__ = "horse_images"

    id = Column(Integer, primary_key=True, index=True)
    horse_id = Column(Integer, ForeignKey("horses.id"))
    image_url = Column(String(255), nullable=False)
    
    # Relationships
    horse = relationship("Horse", back_populates="images") 