from fastapi import FastAPI
from app.database import engine, Base
from app.routers import alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQM-Guard API")

app.include_router(alerts.router)

@app.get("/")
def read_root():
    return {"message": "SQM-Guard backend is running"}