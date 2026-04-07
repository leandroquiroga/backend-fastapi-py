from fastapi import FastAPI

app = FastAPI(
    title="Backend API",
    description="API for the backend of the application",
    version="1.0.0",
)


@app.get("/")
async def home():
    return {"message": "Welcome to the Backend API!"}


@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
