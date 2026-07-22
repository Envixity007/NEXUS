from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:sonu1234@localhost:5432/nexus"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

from models.user import Base

Base.metadata.create_all(bind=engine)