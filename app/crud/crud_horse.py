from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.horse import Horse, HorseImage
from app.schemas.horse import HorseCreate, HorseUpdate, HorseImageCreate

class CRUDHorse(CRUDBase[Horse, HorseCreate, HorseUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: HorseCreate, owner_id: int
    ) -> Horse:
        obj_in_data = obj_in.dict()
        db_obj = Horse(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Horse]:
        return (
            db.query(self.model)
            .filter(Horse.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add_image(
        self, db: Session, *, horse_id: int, image: HorseImageCreate
    ) -> HorseImage:
        db_obj = HorseImage(**image.dict(), horse_id=horse_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_images(self, db: Session, *, horse_id: int) -> List[HorseImage]:
        return db.query(HorseImage).filter(HorseImage.horse_id == horse_id).all()

    def get_primary_image(self, db: Session, *, horse_id: int) -> Optional[HorseImage]:
        return (
            db.query(HorseImage)
            .filter(HorseImage.horse_id == horse_id, HorseImage.is_primary == True)
            .first()
        )

horse = CRUDHorse(Horse) 