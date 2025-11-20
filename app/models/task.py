from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskBase(BaseModel):
    """Modelo base para tareas"""
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción detallada de la tarea")


class TaskCreate(TaskBase):
    """Modelo para crear una nueva tarea"""
    pass


class TaskUpdate(BaseModel):
    """Modelo para actualizar una tarea existente"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    """Modelo completo de tarea con todos los campos"""
    id: UUID
    completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
