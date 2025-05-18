from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import horse as crud_horse
from app.models.user import User
from app.models.horse import HorseBreed, HorseGender
from app.schemas.horse import (
    Horse,
    HorseCreate,
    HorseUpdate,
    HorseImage,
    HorseImageCreate
)
from app.schemas.query import (
    PaginationParams,
    SortParams,
    HorseFilterParams,
    SearchParams
)

router = APIRouter()

@router.get("/", response_model=List[Horse])
def list_horses(
    db: Session = Depends(deps.get_db),
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(),
    filters: HorseFilterParams = Depends(),
    search: SearchParams = Depends(),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all horses with filtering, sorting, and search capabilities.
    """
    # Prepare filters
    filter_dict = {}
    if filters.breed:
        filter_dict["breed"] = HorseBreed(filters.breed)
    if filters.gender:
        filter_dict["gender"] = HorseGender(filters.gender)
    if filters.min_age is not None or filters.max_age is not None:
        filter_dict["age"] = {
            "min": filters.min_age,
            "max": filters.max_age
        }
    if filters.min_height is not None or filters.max_height is not None:
        filter_dict["height"] = {
            "min": filters.min_height,
            "max": filters.max_height
        }
    if filters.location:
        filter_dict["location"] = filters.location

    horses = crud_horse.horse.get_multi(
        db=db,
        skip=pagination.skip,
        limit=pagination.limit,
        filters=filter_dict,
        sort_by=sort.sort_by,
        order=sort.order,
        search_query=search.q,
        search_fields=search.search_in
    )
    return horses

@router.post("/", response_model=Horse)
def create_horse(
    *,
    db: Session = Depends(deps.get_db),
    horse_in: HorseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new horse.
    """
    horse = crud_horse.horse.create_with_owner(
        db=db, obj_in=horse_in, owner_id=current_user.id
    )
    return horse

@router.get("/my-horses", response_model=List[Horse])
def list_my_horses(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve horses owned by current user.
    """
    horses = crud_horse.horse.get_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return horses

@router.get("/{horse_id}", response_model=Horse)
def get_horse(
    *,
    db: Session = Depends(deps.get_db),
    horse_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get horse by ID.
    """
    horse = crud_horse.horse.get(db=db, id=horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    return horse

@router.put("/{horse_id}", response_model=Horse)
def update_horse(
    *,
    db: Session = Depends(deps.get_db),
    horse_id: int,
    horse_in: HorseUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a horse.
    """
    horse = crud_horse.horse.get(db=db, id=horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    if horse.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    horse = crud_horse.horse.update(db=db, db_obj=horse, obj_in=horse_in)
    return horse

@router.post("/{horse_id}/images", response_model=HorseImage)
def add_horse_image(
    *,
    db: Session = Depends(deps.get_db),
    horse_id: int,
    image_in: HorseImageCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add an image to a horse.
    """
    horse = crud_horse.horse.get(db=db, id=horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    if horse.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image = crud_horse.horse.add_image(db=db, horse_id=horse_id, image=image_in)
    return image

@router.get("/{horse_id}/images", response_model=List[HorseImage])
def list_horse_images(
    *,
    db: Session = Depends(deps.get_db),
    horse_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all images for a horse.
    """
    horse = crud_horse.horse.get(db=db, id=horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    images = crud_horse.horse.get_images(db=db, horse_id=horse_id)
    return images 