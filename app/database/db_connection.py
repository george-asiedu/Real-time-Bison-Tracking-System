from beanie import init_beanie
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.constants import messages

mongo_client = None

async def init_db():
    global mongo_client
    load_dotenv()
    db_connection_string = os.getenv(messages["DB_ENV"])
    db_name = messages["MONGO_DB_NAME"]

    if not db_connection_string:
        raise ValueError(messages["db_connection_error"])

    mongo_client = AsyncIOMotorClient(
        db_connection_string,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        maxPoolSize=10,
        retryWrites=True
    )
    database = mongo_client[db_name]

    await init_beanie(
        database=database,
        document_models=[]
    )