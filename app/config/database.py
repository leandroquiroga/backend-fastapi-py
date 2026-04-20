# config/database.py
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Any  # ← Importar Any
from config.setting import URL_MONGO_DB, DATABASE_NAME

# Variables privadas
_client: MongoClient[dict[str, Any]] | None = None
_db: Database[dict[str, Any]] | None = None


def get_database() -> Database[dict[str, Any]]:  # ← Tipo completo
    """Obtiene la base de datos (crea conexión si no existe)"""
    global _client, _db
    
    if _db is None:  # Verificar _db directamente (más lógico)
        _client = MongoClient(URL_MONGO_DB)
        _db = _client[DATABASE_NAME]
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    
    return _db  # PyLance sabe que _db NO es None aquí


def get_users_collection() -> Collection[dict[str, Any]]:  # ← Tipo completo
    """Obtiene la colección de usuarios"""
    db = get_database()
    return db["users"]


def close_connection():
    """Cierra la conexión"""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("✅ Connection to MongoDB closed")