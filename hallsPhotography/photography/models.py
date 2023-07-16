from django.db import models
from django.contrib.auth.models import AbstractUser
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
# Create your models here.

Base = declarative_base()

class User(AbstractUser):
    pass

class Package(Base):
    __tablename__ = "Package"
    ID = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False, name="ID")
    name = sa.Column(sa.String(100), nullable=False, name="Name")
    time_frame = sa.Column(sa.String(50), nullable=False, name="TimeFrame")
    price = sa.Column(sa.Float, nullable=False, name="Price")
    
class PortfolioPhotograph(Base):
    __tablename__ = "PortfolioPhotograph"
    ID = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False, name="ID")
    file_name = sa.Column(sa.String(length=150), name="FileName", nullable=False)
    bucket_name = sa.Column(sa.String(length=100), name="BucketName", nullable=False)
    