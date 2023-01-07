from fastapi import Depends, APIRouter, HTTPException, status
from database import SessionLocal
from models import Users, AlatVerified
from sqlalchemy.orm import Session
from typing import List
from schemas.User import UserSchema
from schemas.Login import UserLogin
from schemas.Email import UserEmail

from datetime import datetime
from pytz import timezone

# from twilio.rest import Client 


# account_sid = 'ACb32edfbfdb796892a3d2edfec162a92a' 
# auth_token = '9f2a22270e35239e12150fcbef752ba8' 
# client = Client(account_sid, auth_token) 


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


@router.post("/users", response_model=UserSchema, tags=["users"], status_code=status.HTTP_201_CREATED)
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
    try:

        db.add(u)
        db.commit()
        return u
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    

@router.post("/users/check", response_model=UserEmail, tags=["users"], status_code=201)
async def valid_email(email: UserEmail, db:Session=Depends(get_db)):
    hasil = db.execute("SELECT email FROM users WHERE email = '%s'"%email.email).fetchone()
    try:
        email = email.email
        for i in hasil:
            if i == email:
                return {"email" : "%s"%i}
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail= f'{email} tidak tersedia')


# @router.post("/users", response_model=UserSchema, tags=["users"])
# def input_users(user: UserSchema, db:Session=Depends(get_db)):
#     try:
#         hasil = db.execute("SELECT email FROM users WHERE email = '%s'" %user.email).fetchone()
#         for i in hasil:
#             emailterdaftar = i

#             if emailterdaftar == user.email:
#                 return "Sudah ada"
#     except:
#         return {"msg" : "email sudah ada"}

@router.post("/users/login", tags=["users"])
def user_login(login: UserLogin,db:Session=Depends(get_db)):
    role = db.execute("SELECT role, id FROM users WHERE email = '%s' AND password = '%s'" %(login.email, login.password)).fetchall()
    # try:
    for hasilrole in role:
        if hasilrole[0] == 'user':
            x = datetime.now(timezone('Asia/Jakarta'))
            hasil = db.execute("SELECT id FROM users WHERE email = '%s' and password = '%s' " %(login.email, login.password)).fetchone()
            for i in hasil:
                input = AlatVerified(
                    user_id = i,
                    login_at = x,
                    masker = login.masker,
                )
                db.add(input)
                db.commit()
                get_scan_id = db.execute("SELECT scan_id FROM alatverified WHERE user_id = %d ORDER BY scan_id DESC" %i).fetchone()
                for j in get_scan_id:
                    getmasker = db.execute("SELECT masker FROM alatverified WHERE scan_id = %d" %j).fetchone()
                    for masker in getmasker:
                        if masker == 1:
                            db.execute("INSERT INTO dataharian VALUES (null, %d, %d, '%s')" %(j, i, x))
                            db.commit()
                            return "user"
                        else:
                            # message = client.messages.create(from_='whatsapp:+14155238886', body='Ada yang tidak pakai masker! dengan user id : %d'%i, to='whatsapp:+6289531049418')
                            # print(message.sid)
                            return "ANDA TIDAK DAPAT MASUK"
        elif hasilrole[0] == 'security':
            return {"role": "security"}
        elif hasilrole[0] == 'datascientist':
            return {"role": "datascientist"}
        else:
            return {"msg" : "akun tidak ada"}
    # except:
    #     return {"msg" : "akun tidak ada"}


    