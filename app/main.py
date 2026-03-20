from fastapi import FastAPI
from app.routes.tickets import router
from app.db import engine, Base
from app import models
from contextlib import asynccontextmanager 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "running"}