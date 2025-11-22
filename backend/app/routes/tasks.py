from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """Erstellt eine neue Aufgabe."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    completed: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Holt alle Aufgaben, optional gefiltert nach Status."""
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    tasks = query.order_by(Task.due_date.asc(), Task.priority.desc()).offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Holt eine spezifische Aufgabe."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Aufgabe nicht gefunden")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Aktualisiert eine Aufgabe."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Aufgabe nicht gefunden")

    update_data = task_update.model_dump(exclude_unset=True)

    # Wenn als erledigt markiert, Timestamp setzen
    if update_data.get("completed") and not task.completed:
        update_data["completed_at"] = datetime.utcnow()
    elif update_data.get("completed") == False:
        update_data["completed_at"] = None

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Löscht eine Aufgabe."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Aufgabe nicht gefunden")

    db.delete(task)
    db.commit()
    return {"message": "Aufgabe gelöscht"}
