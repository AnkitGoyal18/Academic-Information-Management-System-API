from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[int]
    firstName: str
    lastName: str
    registerNumber: str
    personalEmail: str
    officialEmail: str
    phoneNumber: str
    department: str
    yearOfJoining: int
