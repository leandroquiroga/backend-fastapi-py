from fastapi import FastAPI
from routes import user_router, auth_router
from contextlib import asynccontextmanager
from config import close_connection, get_database, create_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida del servidor"""
    # Startup: se ejecuta al iniciar
    print("🚀 Servidor iniciando...")
    get_database()  # Inicializa la conexión a la base de datos
    create_indexes()  # Asegura que los índices estén creados
    yield
    # Shutdown: se ejecuta al apagar
    print("🛑 Servidor apagándose...")
    close_connection()

app = FastAPI(
    title="Backend API",
    description="API con FastAPI y MongoDB",
    version="1.0.0",
    lifespan=lifespan  # Manejo de ciclo de vida
)

app.include_router(user_router)
app.include_router(auth_router)