from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import db, PostgresDatabase
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializar base de datos al arrancar la app"""
    if isinstance(db, PostgresDatabase):
        await db.init_db()
        print("✅ Base de datos PostgreSQL inicializada")
    else:
        print("⚠️  Usando base de datos en memoria")
    yield


def create_application() -> FastAPI:
    """Crear y configurar la aplicación FastAPI"""
    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        lifespan=lifespan,
    )

    # Configurar CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )

    # Incluir rutas
    application.include_router(router)
    
    # Ruta raíz
    @application.get("/")
    async def root():
        return {
            "message": "Bienvenido a la API de Tareas",
            "docs": "/docs",
            "health": "/health"
        }

    return application


app = create_application()
