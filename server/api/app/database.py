import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy_utils import database_exists, create_database

dotenv_path = Path('server/.env')
load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

user = os.getenv("PSQL_USER")
password = os.getenv("PSQL_PSW")
host = os.getenv("PSQL_HOST")
port = os.getenv("PSQL_PORT")
database = os.getenv("PSQL_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        
        yield db
    finally: 
        db.close()
    