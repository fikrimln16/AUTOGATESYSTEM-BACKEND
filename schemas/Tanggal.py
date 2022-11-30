from pydantic import BaseModel

class Tanggal(BaseModel):
    tanggal: str
    class Config:
        orm_mode=True