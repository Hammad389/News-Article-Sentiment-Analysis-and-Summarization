from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Float, Boolean, Text, DateTime, Date)
from datetime import datetime
from sqlalchemy.orm import relationship
from scrapy.utils.project import get_project_settings

Base_single_table = declarative_base()
Base_multiple_table = declarative_base()
# Base_post_scraping_table = declarative_base()


class Udr(Base_single_table):
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

    move_in_date = Column(Date, nullable=True)
    lease_term = Column(Integer, nullable=True)
    rent = Column(Integer, nullable=True)
    corporate_rent = Column(Integer, nullable=True)
    furnished_rent = Column(Integer, nullable=True)

    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)


# Multiple Tables implementation
# One-to-Many Relationship

# Now as we have implemented insert ignore on community data we use it as a foreign key in apartment data
class CommunityData(Base_multiple_table):
    __tablename__ = "community_data"

    community_sr = Column(Integer,primary_key=True, autoincrement=True)
    community_name = Column(String(100), unique=True, nullable=False)
    community_address = Column(String(200), nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    community_description = Column(Text, nullable=True)
    child = relationship("ApartmentData", back_populates="parent")
    # apartment_data = relationship("ApartmentData")  # To create foreign in Apartement data
    community_amenities = Column(Text, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)



class ApartmentData(Base_multiple_table):
    __tablename__ = "apartment_data"

    apartment_sr = Column(Integer,primary_key=True ,autoincrement=True)   #--------- changing it a little bit
    community = Column(String(100), ForeignKey('community_data.community_name'))
    parent = relationship("CommunityData", back_populates="child")
    apartment_no = Column(String(50),unique=True, nullable=True) # Fix----------
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



class RentMatrixData(Base_multiple_table):
    __tablename__ = "rent_matrix"

    id = Column(Integer, primary_key=True , autoincrement=True)
    apartement = Column(String(50), ForeignKey('apartment_data.apartment_no'))
    move_in_date = Column(Date, nullable=True)
    lease_term = Column(Integer, nullable=True)
    rent = Column(Integer, nullable=True)
    corporate_rent = Column(Integer, nullable=True)
    furnished_rent = Column(Integer, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)


