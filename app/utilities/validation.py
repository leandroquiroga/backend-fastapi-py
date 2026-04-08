from models.user_models import users

def exist_id(id: int) -> bool:
    # Verifica si el ID existe en la lista de usuarios
    userAlreadyExists = any(user.id == id for user in users)
    return userAlreadyExists