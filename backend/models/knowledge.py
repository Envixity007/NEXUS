from sqlalchemy import Column, Integer, String, Text, ForeignKey
from models.user import Base

class Knowledge(Base):
    __tablename__ = "Knowledge"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    Source = Column(String(225), nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )