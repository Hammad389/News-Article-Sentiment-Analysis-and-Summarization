from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Float, Boolean, Text, DateTime, Date)
from datetime import datetime
from sqlalchemy.orm import relationship

Base_single_table = declarative_base()
Base_multiple_table = declarative_base()

class Udr(Base_single_table):
    __tablename__ = "udr_data"

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
    move_in_date = Column(Date, nullable=True)
    lease_term = Column(Integer, nullable=True)
    rent = Column(Integer, nullable=True)
    corporate_rent = Column(Integer, nullable=True)
    furnished_rent = Column(Integer, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)

class CommunityData(Base_multiple_table):
    __tablename__ = "community_data"

    community_sr = Column(Integer, primary_key=True, autoincrement=True)
    community_name = Column(String(100), unique=True, nullable=False)
    community_address = Column(String(200), nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    community_description = Column(Text, nullable=True)
    community_amenities = Column(Text, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)
    child = relationship("ApartmentData", back_populates="parent")

class ApartmentData(Base_multiple_table):
    __tablename__ = "apartment_data"

    apartment_sr = Column(Integer, primary_key=True, autoincrement=True)
    community = Column(String(100), ForeignKey('community_data.community_name'))
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
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)
    parent = relationship("CommunityData", back_populates="child")

class RentMatrixData(Base_multiple_table):
    __tablename__ = "rent_matrix"

    id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_sr = Column(Integer, ForeignKey('apartment_data.apartment_sr'))
    move_in_date = Column(Date, nullable=True)
    lease_term = Column(Integer, nullable=True)
    rent = Column(Integer, nullable=True)
    corporate_rent = Column(Integer, nullable=True)
    furnished_rent = Column(Integer, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)
