from pydantic import BaseModel

class UserLogin(BaseModel):
    email:str
    password:str
    masker:bool
    class Config:
        orm_mode=True