from typing import Annotated

import sqlalchemy
import sqlalchemy.orm
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker

test_db = APIRouter(prefix="/test")


@test_db.get("/")
def main():
    return {"message": "test"}


# Database config
DATABASE_FILE = "./test.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create an Engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


# Create a Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database ORM Model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, default=None, index=True)
    secret_info = Column(String, nullable=True)


# Request & Reponse Schemas
class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    secret_info: str


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    secret_info: str | None = None


class ItemPublic(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Create the Tables
Base.metadata.create_all(bind=engine)


# Create Item
@test_db.post("/items/", response_model=ItemPublic)
async def create_item(item: ItemCreate, db: Annotated[Session, Depends(get_db)]):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get all Item
@test_db.get("/items/", response_model=list[ItemPublic])
def read_items(
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return db.query(Item).offset(offset).limit(limit).all()


# Get Item by ID
@test_db.get("/items/{item_id}", response_model=ItemPublic)
async def read_item(item_id: int, db: Annotated[Session, Depends(get_db)]):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# Update Item by ID
@test_db.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(
    item_id: int, item: ItemUpdate, db: Annotated[Session, Depends(get_db)]
):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)

    for key, value in item_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Delete Item by ID
@test_db.delete("/items/{item_id}")
def delete_item(item_id: int, db: Annotated[Session, Depends(get_db)]):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
