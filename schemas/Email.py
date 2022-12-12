from pydantic import BaseModel

class UserEmail(BaseModel):
    email:str
