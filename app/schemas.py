from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # Don't store plain text; hash in code

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models