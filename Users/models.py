from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db_conf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    birth_date = Column(String)
    email = Column(String)
    password = Column(String(255))
    items = relationship("Post", back_populates="owner")
