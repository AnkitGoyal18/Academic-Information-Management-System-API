from users.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    personalEmail = Column(String, unique=True)
    officialEmail = Column(String, unique=True)
    registerNumber = Column(String, unique=True)
    phoneNumber = Column(String)
    department = Column(String)
    yearOfJoining = Column(Integer)

