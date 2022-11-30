from pydantic import BaseModel

class AlatVerified(BaseModel):
    scan_id : int
    user_id : int
    login_at : str
    masker : bool