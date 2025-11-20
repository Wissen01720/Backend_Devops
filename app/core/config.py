from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    app_name: str = "Backend API - Gestión de Tareas"
    app_version: str = "1.0.0"
    app_description: str = "API REST para gestionar tareas con FastAPI"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str | None = None
    
    # CORS
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
