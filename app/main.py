from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.constants import messages
from app.database.db_connection import init_db
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info(messages["db_connection"])

    try:
        yield
    finally:
        logger.info(messages["shutdown"])

app = FastAPI(
    title=messages["app_title"],
    description=messages["app_description"],
    version=messages["app_version"],
    lifespan=lifespan,
)

@app.get(
    "/",
    tags=["App"],
    summary="Application base route"
)
async def root():
    return {"message": messages["welcome"]}