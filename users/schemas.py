from pydantic import BaseModel


class User(BaseModel):
    firstName: str
    lastName: str
    registerNumber: str
    personalEmail: str
    officialEmail: str
    phoneNumber: str
    department: str
    yearOfJoining: int
