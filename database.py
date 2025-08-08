from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                           f"{settings.database_password}@"
                            f"{settings.database_hostname}:"
                            f"{settings.database_port}/"
                            f"{settings.database_name}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    