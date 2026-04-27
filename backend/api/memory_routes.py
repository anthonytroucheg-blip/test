from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MemoryItem
from ..schemas import MemoryItemOut, CreateMemoryIn, UpdateMemoryIn

router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("", response_model=list[MemoryItemOut])
def list_memory(db: Session = Depends(get_db)):
    return db.query(MemoryItem).order_by(MemoryItem.category, MemoryItem.updated_at.desc()).all()


@router.post("", response_model=MemoryItemOut)
def create_memory(body: CreateMemoryIn, db: Session = Depends(get_db)):
    item = MemoryItem(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=MemoryItemOut)
def update_memory(item_id: str, body: UpdateMemoryIn, db: Session = Depends(get_db)):
    item = db.query(MemoryItem).filter(MemoryItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Élément introuvable")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_memory(item_id: str, db: Session = Depends(get_db)):
    item = db.query(MemoryItem).filter(MemoryItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Élément introuvable")
    db.delete(item)
    db.commit()
    return {"ok": True}
