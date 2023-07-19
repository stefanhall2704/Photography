from sqlalchemy.orm import Session
from photography import models


def create_database_package(
    database: Session, name: str, time_frame: str, price: float, file_name: str
):
    database_package = models.Package()
    database_package.name = name
    database_package.time_frame = time_frame
    database_package.price = price
    database_package.file_name = file_name
    database.add(database_package)
    database.commit()
    return database_package


def get_all_database_packages(database: Session):
    return database.query(models.Package).all()
