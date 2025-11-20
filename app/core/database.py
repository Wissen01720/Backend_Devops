from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, delete
from app.models.task import Task
from app.models.db_models import Base, TaskModel
from app.core.config import settings


class InMemoryDatabase:
    """Base de datos en memoria para almacenar tareas"""

    def __init__(self):
        self.tasks: dict[UUID, Task] = {}

    async def get_all(self) -> list[Task]:
        return list(self.tasks.values())

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        return self.tasks.get(task_id)

    async def create(self, task: Task) -> Task:
        self.tasks[task.id] = task
        return task

    async def update(self, task_id: UUID, task: Task) -> Optional[Task]:
        if task_id not in self.tasks:
            return None
        self.tasks[task_id] = task
        return task

    async def delete(self, task_id: UUID) -> bool:
        if task_id not in self.tasks:
            return False
        del self.tasks[task_id]
        return True

    async def count(self) -> int:
        return len(self.tasks)


class PostgresDatabase:
    """Adaptador para PostgreSQL usando SQLAlchemy con async"""

    def __init__(self, database_url: str):
        # Reemplazar postgresql:// por postgresql+psycopg://
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        # Configuración para Supabase pgbouncer con psycopg
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def init_db(self):
        """Crear tablas si no existen"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    def _model_to_task(self, model: TaskModel) -> Task:
        """Convertir modelo SQLAlchemy a Pydantic Task"""
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
        )
    
    async def get_all(self) -> list[Task]:
        async with self.async_session() as session:
            result = await session.execute(select(TaskModel))
            models = result.scalars().all()
            return [self._model_to_task(m) for m in models]
    
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        async with self.async_session() as session:
            result = await session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_task(model) if model else None
    
    async def create(self, task: Task) -> Task:
        async with self.async_session() as session:
            db_task = TaskModel(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
            )
            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)
            return self._model_to_task(db_task)
    
    async def update(self, task_id: UUID, task: Task) -> Optional[Task]:
        async with self.async_session() as session:
            result = await session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )
            db_task = result.scalar_one_or_none()
            if not db_task:
                return None
            
            db_task.title = task.title
            db_task.description = task.description
            db_task.completed = task.completed
            
            await session.commit()
            await session.refresh(db_task)
            return self._model_to_task(db_task)
    
    async def delete(self, task_id: UUID) -> bool:
        async with self.async_session() as session:
            result = await session.execute(
                delete(TaskModel).where(TaskModel.id == task_id)
            )
            await session.commit()
            return result.rowcount > 0
    
    async def count(self) -> int:
        async with self.async_session() as session:
            result = await session.execute(select(TaskModel))
            return len(result.scalars().all())


# Seleccionar adaptador según configuración
if settings.database_url:
    db = PostgresDatabase(settings.database_url)
else:
    db = InMemoryDatabase()
