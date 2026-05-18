
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL URL
DATABASE_URL = "postgresql://postgres:Kittu2001@localhost:5432/ola_rapido"

# Create Engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()