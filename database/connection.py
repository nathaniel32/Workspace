from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends
import config
from database.models import model_base
from database.trigger import create_triggers 

database_engine = create_engine(config.URL_DATABASE)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)

# Create all tables
model_base.metadata.create_all(bind=database_engine)

create_triggers(database_engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]