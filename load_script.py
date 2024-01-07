from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from auth import *
from dbprocess import DBProcess

# Создание базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

Auth.add_user(SessionLocal(), "user1", "pass1")
Auth.add_user(SessionLocal(), "user2", "pass2")
Auth.add_user(SessionLocal(), "user3", "pass3")

DBProcess.load_purchase(SessionLocal(), 'purchases.pickle')
