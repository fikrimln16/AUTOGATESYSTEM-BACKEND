from fastapi import APIRouter
from database import Base, SessionLocal, engine
from schemas.Tanggal import Tanggal
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

@router.get("/security/today/jumlah/{tanggal}", tags=["security"])
async def get_dataharian(tanggal, db:Session=Depends(get_db)):
    return db.execute("SELECT COUNT(alatverified.scan_id) as 'Jumlah' FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE login_at BETWEEN '%s 00:00:00' AND '%s 23:59:59'" %(tanggal, tanggal)).fetchall()      

@router.get("/security/nomask", tags=["security"])
async def get_dataharian(db:Session=Depends(get_db)):
    return db.execute("SELECT users.id, users.namadepan, users.namabelakang, alatverified.scan_id, alatverified.masker, alatverified.login_at FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 0").fetchall()

@router.post("/security/nomask/{tanggal}", tags=["security"])
async def get_dataharian(tanggal, db:Session=Depends(get_db)):
    return db.execute("SELECT users.id, users.namadepan, users.namabelakang, alatverified.scan_id, alatverified.masker, alatverified.login_at FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 0 and login_at BETWEEN '%s 00:00:00' AND '%s 23:59:59'" %(tanggal, tanggal)).fetchall()

@router.get("/security/nomask/jumlah/", tags=["security"])
async def get_dataharian(db:Session=Depends(get_db)):
    return db.execute("SELECT COUNT(alatverified.scan_id) as 'Jumlah' FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 0").fetchall()

@router.get("/security/nomask/jumlah/{tanggal}", tags=["security"])
async def get_dataharian(tanggal, db:Session=Depends(get_db)):
    return db.execute("SELECT COUNT(alatverified.scan_id) as 'Jumlah' FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 0 and login_at BETWEEN '%s 00:00:00' AND '%s 23:59:59'" %(tanggal, tanggal)).fetchall()

@router.get("/security/withmask", tags=["security"])
async def get_dataharian(db:Session=Depends(get_db)):
    return db.execute("SELECT users.id, users.namadepan, users.namabelakang, alatverified.scan_id, alatverified.masker, alatverified.login_at FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 1").fetchall()

@router.post("/security/withmask/{tanggal}", tags=["security"])
async def get_dataharian(tanggal, db:Session=Depends(get_db)):
    return db.execute("SELECT users.id, users.namadepan, users.namabelakang, alatverified.scan_id, alatverified.masker, alatverified.login_at FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 1 and login_at BETWEEN '%s 00:00:00' AND '%s 23:59:59'" %(tanggal, tanggal)).fetchall()

@router.get("/security/withmask/jumlah/{tanggal}", tags=["security"])
async def get_dataharian(tanggal, db:Session=Depends(get_db)):
    return db.execute("SELECT COUNT(alatverified.scan_id) as 'Jumlah' FROM users INNER JOIN alatverified ON users.id = alatverified.user_id WHERE masker = 1 and login_at BETWEEN '%s 00:00:00' AND '%s 23:59:59'" %(tanggal, tanggal)).fetchall()
