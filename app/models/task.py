from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskBase(BaseModel):
    """Modelo base para tareas"""
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200, 
        description="Título de la tarea",
        examples=["Completar el proyecto de DevOps"]
    )
    description: Optional[str] = Field(
        None, 
        description="Descripción detallada de la tarea",
        examples=["Implementar API REST con FastAPI y desplegar en Docker"]
    )


class TaskCreate(TaskBase):
    """Modelo para crear una nueva tarea"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Aprender FastAPI",
                    "description": "Completar el tutorial oficial de FastAPI y crear una API"
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """Modelo para actualizar una tarea existente"""
    title: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=200,
        examples=["Título actualizado de la tarea"]
    )
    description: Optional[str] = Field(
        None,
        examples=["Nueva descripción de la tarea"]
    )
    completed: Optional[bool] = Field(
        None,
        examples=[True]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Tarea actualizada",
                    "description": "Descripción modificada",
                    "completed": True
                }
            ]
        }
    }


class Task(TaskBase):
    """Modelo completo de tarea con todos los campos"""
    id: UUID
    completed: bool = False
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "title": "Implementar OpenTelemetry",
                    "description": "Configurar trazas con Axiom para monitoreo",
                    "completed": False,
                    "created_at": "2025-11-19T20:15:30.123456"
                }
            ]
        }
    }
