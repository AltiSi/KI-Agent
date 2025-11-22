from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class PriorityLevel(enum.Enum):
    LOW = "niedrig"
    MEDIUM = "mittel"
    HIGH = "hoch"
    URGENT = "dringend"


class DocumentCategory(enum.Enum):
    LETTER = "Brief"
    INVOICE = "Rechnung"
    CONTRACT = "Vertrag"
    INSURANCE = "Versicherung"
    AUTHORITY = "Behörde"
    MEDICAL = "Gesundheit"
    OTHER = "Sonstiges"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    category = Column(String(50), nullable=True)

    # KI-Analyse Ergebnisse
    summary = Column(Text, nullable=True)  # Einfache Zusammenfassung
    important_info = Column(Text, nullable=True)  # Wichtige Informationen
    next_steps = Column(Text, nullable=True)  # Empfohlene nächste Schritte

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Beziehungen
    tasks = relationship("Task", back_populates="document", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="document", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="mittel")
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Optional: Verknüpfung zu Dokument
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    document = relationship("Document", back_populates="tasks")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    appointment_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    reminder_sent = Column(Boolean, default=False)

    # Optional: Verknüpfung zu Dokument
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    document = relationship("Document", back_populates="appointments")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, default="Einkaufsliste")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("ShoppingItem", back_populates="shopping_list", cascade="all, delete-orphan")


class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String(255), nullable=False)
    quantity = Column(String(50), nullable=True)
    checked = Column(Boolean, default=False)

    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    shopping_list = relationship("ShoppingList", back_populates="items")

    created_at = Column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    reminder_type = Column(String(50), nullable=False)  # "trinken", "medikamente", "müll", etc.
    reminder_time = Column(DateTime, nullable=True)
    recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String(50), nullable=True)  # "täglich", "wöchentlich", etc.
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
