from fastapi import HTTPException, status
from repositories import users, search_user_by_id, search_user_by_username
from models import User, UserCreate
from utilities.auth_utilities import get_password_hash


def create_user(user_data: UserCreate) -> User:
    """Crea un nuevo usuario (valida unicidad de username y email)"""
    # Valida que el username no exista
    if search_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Valida que el email no exista
    existing_email = next((u for u in users if u.email == user_data.email), None)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Genera nuevo ID (en DB real sería auto-incremental)
    new_id = max([u.id for u in users], default=0) + 1
    
    # Hashea la password
    password_hash = get_password_hash(user_data.password)
    
    # Crea el usuario interno completo
    new_user = User(
        id=new_id,
        name=user_data.name,
        surname=user_data.surname,
        email=user_data.email,
        username=user_data.username,
        age=user_data.age,
        password_hash=password_hash
    )
    
    users.append(new_user)
    return new_user


def update_user(user: User) -> User:
    """Actualiza un usuario existente"""
    for index, saved_user in enumerate(users):
        if saved_user.id == user.id:
            users[index] = user
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user.id} not found"
    )


def delete_user_id(id: int) -> str:
    """Elimina un usuario por ID"""
    user = search_user_by_id(id)  # Lanza 404 si no existe
    users.remove(user)
    return f"User {id} deleted successfully"

