from typing import Generator
from sqlalchemy.orm import Session
from database.postgres import PostgresDatabase

# Create a global database instance
db_instance = PostgresDatabase()

def get_db() -> Generator[Session, None, None]:
    """Get a database session"""
    # The get_session method is already a generator that yields a session
    # Just pass through the generator
    yield from db_instance.get_session() 