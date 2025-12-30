from sqlite3.dbapi2 import version
from fastapi import FastAPI
from src.core.config import settings
from src.db.base import Base  

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)