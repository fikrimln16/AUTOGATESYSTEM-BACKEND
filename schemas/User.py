from pydantic import BaseModel

class UserSchema(BaseModel):
    namadepan:str
    namabelakang:str 
    birthdate:str
    gender:bool
    nomor_telepon:str
    email:str
    username:str
    password:str
    
    class Config:
        orm_mode=True
        
# class UserSchema(BaseModel):
#     namadepan:str
#     namabelakang:str 
#     class Config:
#         orm_mode=True