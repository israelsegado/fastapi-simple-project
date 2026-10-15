import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

load_dotenv()
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOSTNAME = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOSTNAME}/{DB_NAME}", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

def init_db():
    Base.metadata.create_all(engine)