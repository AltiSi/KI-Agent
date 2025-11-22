from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import ShoppingList, ShoppingItem
from ..schemas import (
    ShoppingListCreate,
    ShoppingListResponse,
    ShoppingItemCreate,
    ShoppingItemResponse
)

router = APIRouter(prefix="/api/shopping", tags=["shopping"])


# Shopping Lists
@router.post("/lists", response_model=ShoppingListResponse)
def create_shopping_list(
    shopping_list: ShoppingListCreate,
    db: Session = Depends(get_db)
):
    """Erstellt eine neue Einkaufsliste."""
    db_list = ShoppingList(**shopping_list.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


@router.get("/lists", response_model=List[ShoppingListResponse])
def get_shopping_lists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Holt alle Einkaufslisten."""
    lists = db.query(ShoppingList).order_by(ShoppingList.created_at.desc()).offset(skip).limit(limit).all()
    return lists


@router.get("/lists/{list_id}", response_model=ShoppingListResponse)
def get_shopping_list(
    list_id: int,
    db: Session = Depends(get_db)
):
    """Holt eine spezifische Einkaufsliste."""
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Einkaufsliste nicht gefunden")
    return shopping_list


@router.delete("/lists/{list_id}")
def delete_shopping_list(
    list_id: int,
    db: Session = Depends(get_db)
):
    """Löscht eine Einkaufsliste."""
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Einkaufsliste nicht gefunden")

    db.delete(shopping_list)
    db.commit()
    return {"message": "Einkaufsliste gelöscht"}


# Shopping Items
@router.post("/lists/{list_id}/items", response_model=ShoppingItemResponse)
def add_shopping_item(
    list_id: int,
    item: ShoppingItemCreate,
    db: Session = Depends(get_db)
):
    """Fügt ein Item zur Einkaufsliste hinzu."""
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Einkaufsliste nicht gefunden")

    db_item = ShoppingItem(**item.model_dump(), shopping_list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/items/{item_id}/check")
def toggle_shopping_item(
    item_id: int,
    checked: bool,
    db: Session = Depends(get_db)
):
    """Markiert ein Item als erledigt/nicht erledigt."""
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item nicht gefunden")

    item.checked = checked
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}")
def delete_shopping_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Löscht ein Item von der Einkaufsliste."""
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item nicht gefunden")

    db.delete(item)
    db.commit()
    return {"message": "Item gelöscht"}
