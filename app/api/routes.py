from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID, uuid4
from datetime import datetime

from app.models.task import Task, TaskCreate, TaskUpdate
from app.core.database import db

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "backend-api",
        "version": "1.0.0",
        "tasks_count": await db.count()
    }


@router.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_tasks():
    """Obtener todas las tareas"""
    return await db.get_all()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Crear una nueva tarea"""
    new_task = Task(
        id=uuid4(),
        title=task.title,
        description=task.description,
        completed=False,
        created_at=datetime.now()
    )
    return await db.create(new_task)


@router.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: UUID):
    """Obtener una tarea específica por ID"""
    task = await db.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task


@router.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: UUID, task_update: TaskUpdate):
    """Actualizar una tarea existente"""
    task = await db.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    # Actualizar solo los campos proporcionados
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    
    return await db.update(task_id, task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: UUID):
    """Eliminar una tarea"""
    if not await db.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return None
