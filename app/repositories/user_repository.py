from fastapi import HTTPException
from models import UserResponse, UserDB
from config import get_users_collection
from bson import ObjectId
from typing import Any

def search_user(skip: int = 0, limit: int = 10) -> list[UserDB]:
    """Devuelve una lista de usuarios con paginación"""
    try:
        collection = get_users_collection()
        users_db = collection.find().skip(skip).limit(limit)
        return [UserDB(**doc) for doc in users_db]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching users: {str(e)}"
        )

def search_user_by_id(id: str) -> UserDB:
    """Busca el usuario con el ID especificado"""
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400, detail=f"Invalid user ID: {id}"
        )
    collection = get_users_collection()
    user_doc = collection.find_one({"_id": ObjectId(id)})
    
    if user_doc is None:
        raise HTTPException(
            status_code=404, detail=f"User with ID {id} not found"
        )
    return UserDB(**user_doc)
  
def search_user_by_username(username: str) -> UserDB:
    """Busca usuario por username (para autenticación)"""
    collection = get_users_collection()
    user_doc = collection.find_one({"username": username})
    
    if not user_doc:
        raise HTTPException(
            status_code=404, detail=f"User with username '{username}' not found"
        )
    return UserDB(**user_doc)
    
def search_user_by_user_name_response(username: str) -> UserResponse | None:
    """Busca usuario por username (para respuesta)"""
    user = search_user_by_username(username)
    
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username '{username}' not found"
        )
    return UserResponse.model_validate(user)  # Devuelve solo datos no sensibles

def search_user_by_email(email: str) -> UserDB | None:
    """Busca usuario por email (para validación de unicidad)"""
    collection = get_users_collection()
    user_doc = collection.find_one({"email": email})
    
    if user_doc:
        raise HTTPException(
            status_code=400, detail=f"User with email '{email}' already registered"
        )
    return UserDB(**user_doc) if user_doc else None
  
def insert_user_db(user_doc: dict[str, Any]) -> UserDB:
    """Inserta un nuevo usuario en la base de datos"""
    collection = get_users_collection()
    
    # Inserta el documento (MongoDB genera _id automáticamente)
    result = collection.insert_one(user_doc)
    
    # Agrega el _id generado al documento
    user_doc["_id"] = result.inserted_id
    
    # Retorna UserDB con el _id generado
    return UserDB(**user_doc)
  
def update_user_db(user_id: str, update_data: dict[str, Any]) -> UserDB:
    """Actualiza un usuario existente en la base de datos (solo campos enviados)"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400, detail=f"Invalid user ID: {user_id}"
        )
    
    collection = get_users_collection()
    
    # Actualiza solo los campos enviados
    updated_doc = collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not updated_doc:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found for update"
        )
    
    return UserDB(**updated_doc)

def delete_user_db(user_id: str) -> bool:
    """Elimina un usuario de la base de datos"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400, detail=f"Invalid user ID: {user_id}"
        )
    
    collection = get_users_collection()
    result = collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found"
        )
    
    return True