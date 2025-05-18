from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
from app.models.base import Base

# Explicitly define generic type variables
ModelType = TypeVar("ModelType")  # Type for SQLAlchemy models
CreateSchemaType = TypeVar("CreateSchemaType")  # Type for creation schemas
UpdateSchemaType = TypeVar("UpdateSchemaType")  # Type for update schemas

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        search_query: Optional[str] = None,
        search_fields: Optional[List[str]] = None
    ) -> List[ModelType]:
        query = db.query(self.model)

        # Apply search if provided
        if search_query and search_fields:
            search_filters = []
            for field in search_fields:
                if hasattr(self.model, field):
                    search_filters.append(
                        getattr(self.model, field).ilike(f"%{search_query}%")
                    )
            if search_filters:
                query = query.filter(or_(*search_filters))

        # Apply filters if provided
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if value is not None:
                    if isinstance(value, dict):
                        # Handle range filters
                        if "min" in value and hasattr(self.model, key):
                            filter_conditions.append(
                                getattr(self.model, key) >= value["min"]
                            )
                        if "max" in value and hasattr(self.model, key):
                            filter_conditions.append(
                                getattr(self.model, key) <= value["max"]
                            )
                    elif hasattr(self.model, key):
                        filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        # Apply sorting if provided
        if sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            if order == "desc":
                sort_column = desc(sort_column)
            else:
                sort_column = asc(sort_column)
            query = query.order_by(sort_column)

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj 