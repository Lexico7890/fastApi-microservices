from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings as config

DATABASE_USER = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME
DATABASE_URL = config.DATABASE_URL

initial_database_url = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgres/{DATABASE_NAME}"
)

print(f"🔗 Connecting to: {initial_database_url}")

engine = create_engine(initial_database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()