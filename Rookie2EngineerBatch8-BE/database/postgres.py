import urllib.parse
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from core.config import settings
from core.logging_config import get_logger
from services.user import UserService
logger = get_logger(__name__)

class PostgresDatabase:
    def __init__(self):
        encoded_password = urllib.parse.quote_plus(settings.POSTGRES_PASSWORD)
        self.DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{encoded_password}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
        try:
            self.engine = create_engine(self.DATABASE_URL, echo=True)
            with self.engine.connect() as connection:
                logger.info(f"Connected to the database")
                self.create_db_and_tables()
                self.create_root_user()
        except Exception as e:
            logger.error(f"Error creating engine: {e}")
            raise e

    def create_db_and_tables(self):
        # from models.<name> import <Name>
        logger.info("Creating database and tables")
        from models.asset import Asset
        from models.category import Category
        from models.user import User
        from models.assignment import Assignment
        from models.request import Request
        SQLModel.metadata.create_all(self.engine)
        logger.info("Database and tables created")
        
    def create_root_user(self):
        logger.info("Creating root user")
        with Session(self.engine) as session:
            user_service = UserService(session)
            user_service.create_root_user()
        logger.info("Root user created")

    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session