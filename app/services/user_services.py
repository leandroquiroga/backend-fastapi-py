from fastapi import HTTPException, status
from datetime import datetime, timezone
from repositories import search_user_by_id, insert_user_db, update_user_db, delete_user_db
from models import UserDB, UserCreate, UserUpdate, ChangePasswordRequest
from utilities.auth_utilities import get_password_hash, verify_password
from typing import Any
from pymongo.errors import DuplicateKeyError

def create_user(user_data: UserCreate) -> UserDB:
    """Crea un nuevo usuario (valida unicidad de email)"""

    # Preparar documento SIN _id (MongoDB lo genera automáticamente)
    user_doc: dict[str, Any] = {
        "username": user_data.username,
        "age": user_data.age,
        "name": user_data.name,
        "password_hash": get_password_hash(user_data.password),
        "surname": user_data.surname,
        "email": user_data.email,
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    try:
        # Insertar y obtener UserDB con _id generado
        new_user = insert_user_db(user_doc)
        return new_user
    except DuplicateKeyError as e:
        error = str(e)
        
        if "email" in error or "dup key: { email" in error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        elif "username" in error or "dup key: { username" in error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        else: 
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

def update_user(user_id: str, update_data: UserUpdate) -> UserDB:
    """Actualiza un usuario existente (solo campos enviados)"""
    # Validar que el usuario exista (lanza 404 si no)
    existing_user = search_user_by_id(user_id)
    
    # Convertir UserUpdate a dict y eliminar campos None (no enviados)
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Si no hay campos para actualizar, retornar usuario actual
    if not update_dict:
        return existing_user
    
    # Agregar updated_at automáticamente
    update_dict["updated_at"] = datetime.now(timezone.utc)
    
    # Actualizar en BD
    updated_user = update_user_db(user_id, update_dict)
    return updated_user

def delete_user_id(id: str) -> str:
    """Elimina un usuario por ID"""
    search_user_by_id(id)
    # Eliminar en BD
    if delete_user_db(id):
        return f"User with ID {id} deleted successfully"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user with ID {id}"
        )
