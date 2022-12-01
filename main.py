from fastapi import FastAPI
from database import Base, SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from router import dataharian
from router import user
from router import security

import uvicorn

Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["https://autogatesystem.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(dataharian.router)
app.include_router(user.router)
app.include_router(security.router)

