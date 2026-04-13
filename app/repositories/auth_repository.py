
from models import LoginRequest
from typing import List

# Lista de 10 usuarios de ejemplo
users_db: List[LoginRequest] = [
    LoginRequest(
        username="johndoe",
        password="password123"
    ),
    LoginRequest(
        username="janedoe",
        password="password456"
    ),
]


