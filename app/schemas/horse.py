from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import datetime
from app.models.horse import HorseBreed, HorseGender

class HorseImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class HorseImageCreate(HorseImageBase):
    pass

class HorseImage(HorseImageBase):
    id: int
    horse_id: int

    class Config:
        from_attributes = True

class HorseBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    breed: HorseBreed
    age: Annotated[int, Field(ge=0, le=40)]
    gender: HorseGender
    color: str
    height: Optional[Annotated[float, Field(ge=0)]] = None  # in hands
    weight: Optional[Annotated[float, Field(ge=0)]] = None  # in kg
    description: Optional[str] = None
    training_level: Optional[str] = None
    health_records: Optional[str] = None

class HorseCreate(HorseBase):
    pass

class HorseUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    breed: Optional[HorseBreed] = None
    age: Optional[Annotated[int, Field(ge=0, le=40)]] = None
    gender: Optional[HorseGender] = None
    color: Optional[str] = None
    height: Optional[Annotated[float, Field(ge=0)]] = None
    weight: Optional[Annotated[float, Field(ge=0)]] = None
    description: Optional[str] = None
    training_level: Optional[str] = None
    health_records: Optional[str] = None

class Horse(HorseBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    images: List[HorseImage] = []

    class Config:
        from_attributes = True 