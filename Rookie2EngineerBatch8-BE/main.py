from fastapi import FastAPI
import uvicorn
from middleware.cors import setup_cors_middleware
from middleware.logging import LoggingMiddleware
from middleware.auth import AuthMiddleware
from dotenv import load_dotenv
from database.postgres import PostgresDatabase
from api.v1.router import router as v1_router
from core.logging_config import setup_logging, get_logger

# Configure logging
setup_logging()
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# Initialize database
logger.info("Initializing database...")
db = PostgresDatabase()

# FastAPI App
app = FastAPI(
    title="Assets Management API",
    description="API for Assets Management",
    version="1.0.0",
)

# Middleware
logger.info("Setting up middleware...")
setup_cors_middleware(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Health Check
@app.get("/health")
async def health():
    return {"message": "OK"}

# Include routers
logger.info("Including routers...")
app.include_router(v1_router)

# Run the app
if __name__ == "__main__":
    logger.info("Starting application...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
