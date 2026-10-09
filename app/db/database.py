import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOSTNAME = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql+psycopg://{USER}:{PASSWORD}@{HOSTNAME}/{DB_NAME}", echo=True)

with engine.connect() as conn:
    