from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import uuid

class Letter(Base):
    __tablename__ = "letters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    content = Column(Text)
    password_hash = Column(String, nullable=True)
    style_theme = Column(String, default="base")
    image_url = Column(String, nullable=True)