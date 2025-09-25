from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.constants import messages
from app.core.config import get_settings
from .bison_model import BisonFrame

mongo_client = None
settings = get_settings()

async def init_db():
    global mongo_client
    db_connection_string = settings.MONGO_URI
    db_name = settings.DB_NAME

    if not db_connection_string:
        raise ValueError(messages["db_connection_error"])
    if not db_name:
        raise ValueError(messages["db_name_error"])

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
        document_models=[BisonFrame]
    )