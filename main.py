from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    return {"Hello :":"World"}

@app.get("/users")
async def index():
    return {"Hello :":"Users"}