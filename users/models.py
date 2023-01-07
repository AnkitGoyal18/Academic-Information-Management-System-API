from users.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    personalEmail = Column(String)
    officialEmail = Column(String)
    registerNumber = Column(String)
    phoneNumber = Column(String)
    department = Column(String)
    yearOfJoining = Column(Integer)

