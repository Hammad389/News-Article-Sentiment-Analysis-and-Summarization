from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Float, Boolean, Text)
from sqlalchemy.orm import relationship
from scrapy.utils.project import get_project_settings

Base_single_table = declarative_base()
Base_multiple_table = declarative_base()



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

# Multiple Tables implementation

class CommunityData(Base_multiple_table):
    __tablename__ = "community_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    community_name = Column(String(100), primary_key=True, nullable=False)
    community_address = Column(String(200), nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    community_description = Column(Text, nullable=True)

class ApartmentData(Base_multiple_table):
    __tablename__ = "apartment_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    community = Column(String(100), ForeignKey('community_data.community_name'))
    # CommunityData = relationship(CommunityData)
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



"C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\mysql\connector\connection_cext.py", line 781, in cmd_query
    raise get_mysql_exception(
sqlalchemy.exc.DatabaseError: (mysql.connector.errors.DatabaseError) 1822 (HY000): Failed to add the foreign key constraint. Missing index for constraint 'apartment_data_ibfk_1' in the referenced table 'community_data'
[SQL:
CREATE TABLE apartment_data (
        id INTEGER NOT NULL AUTO_INCREMENT,
        community VARCHAR(100),
        apartment_no VARCHAR(50),
        no_of_bedrooms INTEGER,
        no_of_bathrooms INTEGER,
        area INTEGER,
        floor_no INTEGER,
        availability BOOL,
        deposit FLOAT,
        `Max_rent` FLOAT,
        `Min_rent` FLOAT,
        amenities TEXT,
        community_amenities TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY(community) REFERENCES community_data (community_name)
)

]
(Background on this error at: https://sqlalche.me/e/20/4xp6)
