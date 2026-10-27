import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey
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
    nombre = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    edad = Column(Integer)
    telefono = Column(String(20))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.now)

    addresses = relationship('Address', back_populates='user', uselist=False, lazy='joined')

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    ciudad = Column(String(50), nullable=False)
    codigo_postal = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship('User', back_populates='addresses', uselist=False)

def init_db():
    Base.metadata.create_all(engine)