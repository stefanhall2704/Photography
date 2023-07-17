import urllib

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_url = config("DATABASE_URL")

if "sqlite" in database_url:
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
elif "SQL Server" in database_url:
    params = urllib.parse.quote_plus(database_url)
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        pool_size=20,
        max_overflow=20,
        pool_pre_ping=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
