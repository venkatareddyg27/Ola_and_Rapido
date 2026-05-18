
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL URL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/ola_rapido_db"

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