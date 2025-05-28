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


    # __tabl_args__=(
    #     PrimaryKeyConstraint('id', 'community_name')
    # )



class ApartmentData(Base_multiple_table):
    __tablename__ = "apartment_data"

    apartment_sr = Column(Integer,primary_key=True, autoincrement=True)
    community = Column(String(100), ForeignKey('community_data.community_name'))
    parent = relationship("CommunityData", back_populates="child")
    apartment_no = Column(String(50), nullable=True) # Fix--
    no_of_bedrooms = Column(Integer, nullable=True)
    no_of_bathrooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    floor_no = Column(Integer, nullable=True)
    availability = Column(Boolean, nullable=True)
    deposit = Column(Float, nullable=True)
    Max_rent = Column(Float, nullable=True)
    Min_rent = Column(Float, nullable=True)
    amenities = Column(Text, nullable=True)

    # rent_matrix_data = relationship("RentMatrixData")
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)



class RentMatrixData(Base_multiple_table):
    __tablename__ = "rent_matrix"

    id = Column(Integer, primary_key=True , autoincrement=True)
    # apartement_sr = Column(Integer, ForeignKey('apartment_data.apartment_sr'))
    move_in_date = Column(Date, nullable=True)
    lease_term = Column(Integer, nullable=True)
    rent = Column(Integer, nullable=True)
    corporate_rent = Column(Integer, nullable=True)
    furnished_rent = Column(Integer, nullable=True)
    updated_datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    created_datetime = Column(DateTime(), default=datetime.now)





import csv
import json
from xmlrpc.client import Boolean

import pandas as pd
from sqlalchemy import create_engine, insert
from urd_scraper.models import Udr, Base_multiple_table, Base_single_table, ApartmentData, CommunityData, RentMatrixData, Base_post_scraping_table
from sqlalchemy.orm import sessionmaker, Session
from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UrdScraperPipelineCsv:
    def open_spider(self,spider):
        self.file = open('data.csv', 'w', encoding='utf-8', newline='')
        self.writer = None

    def process_item(self, item, spider):
        item = dict(item)
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
            self.writer.writeheader()
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()


class UrdScraperPipelineJson:
    def open_spider(self,spider):
        self.file = open('data.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first = True

    def process_item(self, item, spider):
        if not self.first:
            self.file.write(',\n')
        self.first = False
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

class UrdScraperPipelineParquet:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        if len (self.items) >= 100:
            self.save_to_parquet()
        return item

    def save_to_parquet(self):
        df = pd.DataFrame(self.items)
        df.to_parquet('data.parquet', index=False)
        self.items.clear()

    def close_spider(self, spider):
        if self.items:
            self.save_to_parquet()


class UrdScraperDatabase:

    def open_spider(self, spider):
        # single column implementation
        engine_single = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module5_single')
        Base_single_table.metadata.create_all(engine_single)
        self.Session_single = sessionmaker(bind=engine_single)

        # multiple column implementation
        engine_multiple = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5_multiple')
        Base_multiple_table.metadata.create_all(engine_multiple)
        self.Session_multiple = sessionmaker(bind=engine_multiple)


    def process_item(self, item, spider):
        session_single = self.Session_single()
        single_record = Udr(
            community_name=item.get('community_name'),
            community_address=item.get('community_address'),
            community_rent=item.get('community_rent'),
            community_rooms=item.get('community_rooms'),
            community_description=item.get('community_description'),
            apartment_no=item.get('apartment_no'),
            no_of_bedrooms=item.get('no_of_bedrooms'),
            no_of_bathrooms=item.get('no_of_bathrooms'),
            area=item.get('area'),
            floor_no=item.get('floor_no'),
            availability=item.get('availability'),
            deposit=item.get('deposit'),
            Max_rent=item.get('Max_rent'),
            Min_rent=item.get('Min_rent'),
            amenities=', '.join(item.get('amenities', [])),
            community_amenities=', '.join(item.get('community_amenities', [])) if item.get(
                'community_amenities') else '',
            move_in_date = item.get('move_in_date'),
            lease_term = item.get('lease_term'),
            rent = item.get('rent'),
            corporate_rent = item.get('corporate_rent'),
            furnished_rent = item.get('furnished_rent'),
        )
        # # ---
        # stmt = insert(Udr).prefix_with("IGNORE").values(single_record)
        # session_single.execute(stmt)

        session_single.add(single_record)
        session_single.commit()
        session_single.close()
        # return item

        session_mutiple = self.Session_multiple()
        multiple_record_community = insert(CommunityData).values(
            community_name=item.get('community_name'),
            community_address=item.get('community_address'),
            community_rent=item.get('community_rent'),
            community_rooms=item.get('community_rooms'),
            community_description=item.get('community_description'),
            community_amenities = ', '.join(item.get('community_amenities', [])) if item.get('community_amenities') else ''
        )
        # insert(ApartmentData).values
        multiple_record_apartment = ApartmentData(
            apartment_no =item.get('apartment_no'),
            no_of_bedrooms=item.get('no_of_bedrooms'),
            no_of_bathrooms=item.get('no_of_bathrooms'),
            area=item.get('area'),
            floor_no=item.get('floor_no'),
            availability=item.get('availability'),
            deposit=item.get('deposit'),
            Max_rent=item.get('Max_rent'),
            Min_rent=item.get('Min_rent'),
            amenities=', '.join(item.get('amenities', [])),

        )

        # Implemented Insert Ignore for community data
        stmt = multiple_record_community.prefix_with('IGNORE')
        session_mutiple.execute(stmt)

        # Implemented Insert Ignore for apartment data
        session_mutiple.add(multiple_record_apartment)
        # stmt_a = multiple_record_apartment.prefix_with('IGNORE')
        # session_mutiple.execute(stmt_a)

        for i in item['raw_rent_matrix']:
            rent_matrix_record = RentMatrixData(
            move_in_date = i.get('MoveInDate'),
            lease_term = i.get('LeaseTerm'),
            rent = i.get('Rent'),
            corporate_rent = i.get('CorporateRent'),
            furnished_rent = i.get('FurnishedRent'))
            session_mutiple.add(rent_matrix_record)
        session_mutiple.commit()



        # session_mutiple.add(multiple_record_community)
        # session_mutiple.add(multiple_record_apartment)
        # session_mutiple.add(rent_matrix_record)
        session_mutiple.commit()
        session_mutiple.close()
        return item
