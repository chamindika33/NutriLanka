from pydantic_settings import BaseSettings
from typing import ClassVar
# from pydantic import BaseSettings
from typing import Annotated
import psycopg2
import multiprocessing
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

pg_username = os.getenv('DB_USERNAME')
pg_password = os.getenv('DB_PASSWORD')
pg_database = os.getenv('DB_NUTRILANKA')
pg_port = os.getenv('DB_PORT')
pg_connection = os.getenv('DB_CONNECTION')
pg_host = os.getenv('DB_HOST')


class Settings(BaseSettings):
    print('hi')
    PG_URL: Annotated[str, ...] = f"{pg_connection}://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    print('pg_url-->',PG_URL)

# global instance
settings = Settings()



# class LogConfig(BaseModel):
#     LOGGER_NAME: str = "nutriLanka"
#     LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
#     LOG_LEVEL: str = "DEBUG"

#     # Logging config (marked as ClassVar to ignore validation)
#     version: ClassVar[int] = 1
#     disable_existing_loggers: ClassVar[bool] = False
#     formatters: ClassVar[dict] = {
#         "default": {
#             "()": "uvicorn.logging.DefaultFormatter",
#             "fmt": "%(levelprefix)s | %(asctime)s | %(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     }
#     handlers: ClassVar[dict] = {
#         "default": {
#             "formatter": "default",
#             "class": "logging.StreamHandler",
#             "stream": "ext://sys.stderr",
#         },
#     }
#     loggers: ClassVar[dict] = {
#         "nutriLanka": {"handlers": ["default"], "level": LOG_LEVEL},
#     }





# # global instance
# logConfig = LogConfig()