from pydantic import BaseModel


# User model
class User(BaseModel):
    name: str
    email: str
