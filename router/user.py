from fastapi import Depends, APIRouter
from database import SessionLocal
from models import Users, AlatVerified
from sqlalchemy.orm import Session
from typing import List
from schemas.User import UserSchema
from schemas.Login import UserLogin
import datetime

from twilio.rest import Client 
 
account_sid = 'ACb32edfbfdb796892a3d2edfec162a92a' 
auth_token = 'b08f8596ef2089b493fe1e2d0941c423' 
client = Client(account_sid, auth_token) 


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=List[UserSchema], tags=["users"])
async def get_users(db:Session=Depends(get_db)):
    return db.query(Users).all()

@router.get("/users/total", tags=["users"])
async def get_total_users(db:Session=Depends(get_db)):
    return db.execute("SELECT COUNT(id) as 'jumlah' FROM users").all()
    

@router.get("/users/{id}", tags=["users"])
async def get_users_by_id(id:int, db:Session=Depends(get_db)):
    return db.execute("SELECT * FROM users WHERE id = %s" %id).fetchall()


@router.post("/users", response_model=UserSchema, tags=["users"])
def input_users(user: UserSchema, db:Session=Depends(get_db)):
    u = Users(
        namadepan = user.namadepan,
        namabelakang = user.namabelakang,
        birthdate = user.birthdate,
        gender = user.gender,
        nomor_telepon = user.nomor_telepon,
        email = user.email,
        username = user.username,
        password = user.password,
        role = "user"
    )
    db.add(u)
    db.commit()
    return u

@router.post("/users/login", tags=["users"])
async def user_login(login: UserLogin,db:Session=Depends(get_db)):
    role = db.execute("SELECT role FROM users WHERE email = '%s' AND password = '%s'" %(login.email, login.password)).fetchone()
    for hasilrole in role:
        if hasilrole == 'user':
            datenow = datetime.datetime.now()
            hasil = db.execute("SELECT id FROM users WHERE email = '%s' and password = '%s' " %(login.email, login.password)).fetchone()
            for i in hasil:
                input = AlatVerified(
                    user_id = i,
                    login_at = datenow,
                    masker = login.masker,
                )
                db.add(input)
                db.commit()
                get_scan_id = db.execute("SELECT scan_id FROM alatverified WHERE user_id = %d ORDER BY scan_id DESC" %i).fetchone()
                for j in get_scan_id:
                    getmasker = db.execute("SELECT masker FROM alatverified WHERE scan_id = %d" %j).fetchone()
                    for masker in getmasker:
                        if masker == 1:
                            db.execute("INSERT INTO dataharian VALUES (null, %d, %d, '%s')" %(j, i, datenow))
                            db.commit()
                            return "user"
                        else:
                            message = client.messages.create(from_='whatsapp:+14155238886', body='Ada yang tidak pakai masker!', to='whatsapp:+6281322195912')
                            print(message.sid)
                            return "ANDA TIDAK DAPAT MASUK"
        elif hasilrole == 'security':
            return {"role": "security"}
        elif hasilrole == 'datascientist':
            return {"role": "datascientist"}
        elif hasilrole == None:
            return "Akun Tidak Ada"

    