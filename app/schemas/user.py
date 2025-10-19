from pydantic import BaseModel
from datetime import date

class UserOut(BaseModel):
    id: int
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    birth_date: date
    phone: str
    email: str

    class Config:
        from_attributes = True

