from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Task
from ..schemas import TaskOut, CreateTaskIn, UpdateTaskIn

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.created_at.desc()).all()


@router.post("", response_model=TaskOut)
def create_task(body: CreateTaskIn, db: Session = Depends(get_db)):
    task = Task(**body.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: str, body: UpdateTaskIn, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Tâche introuvable")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Tâche introuvable")
    db.delete(task)
    db.commit()
    return {"ok": True}
