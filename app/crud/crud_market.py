from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.market import MarketListing, Transaction, ListingStatus
from app.schemas.market import MarketListingCreate, MarketListingUpdate, TransactionCreate

class CRUDMarketListing(CRUDBase[MarketListing, MarketListingCreate, MarketListingUpdate]):
    def create_with_seller(
        self, db: Session, *, obj_in: MarketListingCreate, seller_id: int
    ) -> MarketListing:
        obj_in_data = obj_in.dict()
        db_obj = MarketListing(**obj_in_data, seller_id=seller_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_seller(
        self, db: Session, *, seller_id: int, skip: int = 0, limit: int = 100
    ) -> List[MarketListing]:
        return (
            db.query(self.model)
            .filter(MarketListing.seller_id == seller_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_listings(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[MarketListing]:
        return (
            db.query(self.model)
            .filter(MarketListing.status == ListingStatus.ACTIVE)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_transaction(
        self, db: Session, *, obj_in: TransactionCreate
    ) -> Transaction:
        db_obj = Transaction(**obj_in.dict())
        db.add(db_obj)
        
        # Update listing status
        listing = db.query(MarketListing).filter(MarketListing.id == obj_in.listing_id).first()
        if listing:
            listing.status = ListingStatus.SOLD
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_transactions_by_buyer(
        self, db: Session, *, buyer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.buyer_id == buyer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

market = CRUDMarketListing(MarketListing) 