from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Backend API",
    description="API for the backend of the application",
    version="1.0.0",
)


# Entidad Users
class Users(BaseModel):
    name: str
    surname: str
    email: str
    username: str
    age: int


users = [
    Users(name="Leandro", surname="Quiriga", email="leandro@example.com", username="leandroq", age=30),
    Users(name="Maria", surname="Gomez", email="maria@example.com", username="mariag", age=25),
    Users(name="Carlos", surname="Perez", email="carlos@example.com", username="carlosp", age=28),
]

@app.get("/")
async def home():
    return {"message": "Welcome to the Backend API!"}


@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users")
async def get_users():
    return users