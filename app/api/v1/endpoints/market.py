from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import market as crud_market
from app.models.user import User
from app.schemas.market import (
    MarketListing,
    MarketListingCreate,
    MarketListingUpdate,
    Transaction,
    TransactionCreate,
)

router = APIRouter()

@router.get("/listings", response_model=List[MarketListing])
def list_listings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all active market listings.
    """
    listings = crud_market.market.get_active_listings(db, skip=skip, limit=limit)
    return listings

@router.post("/listings", response_model=MarketListing)
def create_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_in: MarketListingCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new market listing.
    """
    listing = crud_market.market.create_with_seller(
        db=db, obj_in=listing_in, seller_id=current_user.id
    )
    return listing

@router.get("/my-listings", response_model=List[MarketListing])
def list_my_listings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve listings created by current user.
    """
    listings = crud_market.market.get_by_seller(
        db=db, seller_id=current_user.id, skip=skip, limit=limit
    )
    return listings

@router.get("/listings/{listing_id}", response_model=MarketListing)
def get_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get market listing by ID.
    """
    listing = crud_market.market.get(db=db, id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Market listing not found")
    return listing

@router.put("/listings/{listing_id}", response_model=MarketListing)
def update_listing(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
    listing_in: MarketListingUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a market listing.
    """
    listing = crud_market.market.get(db=db, id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Market listing not found")
    if listing.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    listing = crud_market.market.update(db=db, db_obj=listing, obj_in=listing_in)
    return listing

@router.post("/transactions", response_model=Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: TransactionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a transaction for a market listing.
    """
    listing = crud_market.market.get(db=db, id=transaction_in.listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Market listing not found")
    if listing.seller_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot buy your own listing")
    transaction = crud_market.market.create_transaction(
        db=db, obj_in=transaction_in
    )
    return transaction

@router.get("/my-transactions", response_model=List[Transaction])
def list_my_transactions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve transactions where current user is the buyer.
    """
    transactions = crud_market.market.get_transactions_by_buyer(
        db=db, buyer_id=current_user.id, skip=skip, limit=limit
    )
    return transactions 