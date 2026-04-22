# config/database.py
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Any  # ← Importar Any
from config.setting import URL_MONGO_DB, DATABASE_NAME
from utilities.helper import logging

# Variables privadas
_client: MongoClient[dict[str, Any]] | None = None
_db: Database[dict[str, Any]] | None = None


def get_database() -> Database[dict[str, Any]]:  # ← Tipo completo
    """Obtiene la base de datos (crea conexión si no existe)"""
    global _client, _db
    
    if _db is None:  # Verificar _db directamente (más lógico)
        _client = MongoClient(URL_MONGO_DB)
        _db = _client[DATABASE_NAME]
        logging(f"✅ Connected to MongoDB: {DATABASE_NAME}", context="DATABASE")
    
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
        logging("✅ Connection to MongoDB closed", context="DATABASE")
        
def create_indexes():
    """Crea indices unicos en la coleccion de usuarios"""
    collection = get_users_collection()
    # collection.create_index([("email", ASCENDING), ("username", ASCENDING)])
    collection.create_index("email", unique=True)
    collection.create_index("username", unique=True)