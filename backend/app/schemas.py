from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Document Schemas
class DocumentBase(BaseModel):
    title: str
    category: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    filename: str
    summary: Optional[str] = None
    important_info: Optional[str] = None
    next_steps: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "mittel"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    document_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    completed: bool
    completed_at: Optional[datetime] = None
    document_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    appointment_date: datetime
    location: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    document_id: Optional[int] = None


class AppointmentResponse(AppointmentBase):
    id: int
    reminder_sent: bool
    document_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Shopping List Schemas
class ShoppingItemBase(BaseModel):
    item: str
    quantity: Optional[str] = None


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItemResponse(ShoppingItemBase):
    id: int
    checked: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ShoppingListBase(BaseModel):
    name: str = "Einkaufsliste"


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingListResponse(ShoppingListBase):
    id: int
    created_at: datetime
    items: List[ShoppingItemResponse] = []

    class Config:
        from_attributes = True


# Reminder Schemas
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: str
    reminder_time: Optional[datetime] = None
    recurring: bool = False
    recurring_pattern: Optional[str] = None


class ReminderCreate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schema
class DashboardResponse(BaseModel):
    upcoming_tasks: List[TaskResponse]
    upcoming_appointments: List[AppointmentResponse]
    daily_summary: str
    pending_tasks_count: int
    today_appointments_count: int
