from fastapi import FastAPI
from routes import user_routes

app = FastAPI(
    title="Backend API",
    description="API for the backend of the application",
    version="1.0.0",
)

@app.get("/")
async def home():
    return {"message": "Welcome to the Backend API!"}

app.include_router(user_routes.router)