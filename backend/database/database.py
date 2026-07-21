from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:sonu1234@localhost:5432/nexus"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
from models.user import Base

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")