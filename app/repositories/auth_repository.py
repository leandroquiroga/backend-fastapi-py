from models import User
from typing import List
from utilities.auth_utilities import get_password_hash

users_db: List[User] = [
    User(
        id=1,
        username="johndoe",
        name="John",
        surname="Doe",
        email="johndoe@example.com",
        age=30,
        password_hash=get_password_hash("password123")
    ),
    User(
        id=2,
        username="janedoe",
        name="Jane",
        surname="Doe",
        email="janedoe@example.com",
        age=25,
        password_hash=get_password_hash("password456")
    ),
    User(
        id=3,
        username="alice",
        name="Alice",
        surname="Smith",
        email="alice@example.com",
        age=28,
        password_hash=get_password_hash("password789")
    ),
]

def search_user_by_username(username: str) -> User | None:
    return next((u for u in users_db if u.username == username), None)