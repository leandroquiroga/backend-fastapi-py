from fastapi import FastAPI
from routes import user_routes

app = FastAPI(
    title="Backend API",
    description="API for the backend of the application",
    version="1.0.0",
)
app.include_router(user_routes.router)