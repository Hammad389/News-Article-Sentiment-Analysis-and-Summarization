from sqlalchemy import Column, create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()

# def db_connect():
#     return create_engine(get_project_settings().get("CONNECTION_STRING"))
#
# def create_table(engine):
#     try:
#         Base.metadata.create_all(engine)
#         print("Table created!")
#     except:
#         print("Error while creating table.")

# Single Table implementation

class Udr(Base):
    __tablename__="udr_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    community_name = Column(String(100), nullable=False)
    community_address = Column(String(200), nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    community_description = Column(Text, nullable=True)
    apartment_no = Column(String(50), nullable=True)
    no_of_bedrooms = Column(Integer, nullable=True)
    no_of_bathrooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    floor_no = Column(Integer, nullable=True)
    availability = Column(Boolean, nullable=True)
    deposit = Column(Float, nullable=True)
    Max_rent = Column(Float, nullable=True)
    Min_rent = Column(Float, nullable=True)
    amenities = Column(Text, nullable=True)
    community_amenities = Column(Text, nullable=True)

# Multiple Tables implementation

class CommunityData(Base):
    __tablename__ = "community_data"

    id = Column(Integer, autoincrement=True)
    community_name = Column(String(100), primary_key=True, nullable=False)
    community_address = Column(String(200), nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    community_description = Column(Text, nullable=True)

class ApartmentData(Base):
    __tablename__ = "apartment_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_no = Column(String(50), nullable=True)
    no_of_bedrooms = Column(Integer, nullable=True)
    no_of_bathrooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    floor_no = Column(Integer, nullable=True)
    availability = Column(Boolean, nullable=True)
    deposit = Column(Float, nullable=True)
    Max_rent = Column(Float, nullable=True)
    Min_rent = Column(Float, nullable=True)
    amenities = Column(Text, nullable=True)
    community_amenities = Column(Text, nullable=True)