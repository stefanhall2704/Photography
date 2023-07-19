from photography.database import SessionLocal


def get_database():
    database = SessionLocal()
    return database
