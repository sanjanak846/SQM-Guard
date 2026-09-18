from fastapi import FastAPI
from app.database import engine, Base
from app.routers import alerts, campaigns
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQM-Guard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts.router)
app.include_router(campaigns.router)

@app.get("/")
def read_root():
    logger.info("SQM-Guard API accessed")
    return {"message": "SQM-Guard backend is running"}
