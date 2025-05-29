# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
from xmlrpc.client import Boolean

import pandas as pd
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, insert
from urd_scraper.models import Udr, Base_multiple_table, Base_single_table, ApartmentData, CommunityData, RentMatrixData, Base_post_scraping_table, PostScraping
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
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




class UrdMultipleTablePipeline:
    def open_spider(self, spider):
        # multiple column implementation
        engine_multiple = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5_multiple')
        Base_multiple_table.metadata.create_all(engine_multiple)
        self.Session_multiple = sessionmaker(bind=engine_multiple)


    def process_item(self, item, spider):

        session_mutiple = self.Session_multiple()
        try:
            community = session_mutiple.query(CommunityData).filter_by(community_name=item['community_name']).first()
            if community:
                community.community_address = item.get('community_address')
                community.community_rent = item.get('community_rent')
                community.community_rooms = item.get('community_rooms')
                community.community_description = item.get('community_description')
                community.community_amenities = ', '.join(item.get('community_amenities', [])) if item.get(
                    'community_amenities') else ''
                community.updated_datetime = func.now()    ######

            else:
                community = CommunityData(
                    community_name=item.get('community_name'),
                    community_address=item.get('community_address'),
                    community_rent=item.get('community_rent'),
                    community_rooms=item.get('community_rooms'),
                    community_description=item.get('community_description'),
                    community_amenities=', '.join(item.get('community_amenities', [])) if item.get(
                        'community_amenities') else ''
                )
                session_mutiple.add(community)
                session_mutiple.commit()


            apartment = session_mutiple.query(ApartmentData).filter_by(apartment_no=item['apartment_no']).first()
            if apartment:
                apartment.community = community.community_name
                apartment.no_of_bedrooms = item.get('no_of_bedrooms')
                apartment.no_of_bathrooms = item.get('no_of_bathrooms')
                apartment.area = item.get('area')
                apartment.floor_no = item.get('floor_no')
                apartment.availability = item.get('availability')
                apartment.deposit = item.get('deposit')
                apartment.Max_rent = item.get('Max_rent')
                apartment.Min_rent = item.get('Min_rent')
                apartment.amenities = ', '.join(item.get('amenities', []))
                apartment.updated_datetime = func.now() #######
            # insert(ApartmentData).values
            else:
                apartment = ApartmentData(
                    apartment_no=item.get('apartment_no'),
                    community=community.community_name,
                    no_of_bedrooms=item.get('no_of_bedrooms'),
                    no_of_bathrooms=item.get('no_of_bathrooms'),
                    area=item.get('area'),
                    floor_no=item.get('floor_no'),
                    availability=item.get('availability'),
                    deposit=item.get('deposit'),
                    Max_rent=item.get('Max_rent'),
                    Min_rent=item.get('Min_rent'),
                    amenities=', '.join(item.get('amenities', []))
                )
                session_mutiple.add(apartment)
                session_mutiple.commit()


            for i in item['raw_rent_matrix']:
                rent = session_mutiple.query(RentMatrixData).filter_by(
                    apartement=apartment.apartment_no,
                    move_in_date=i.get('MoveInDate'),
                    lease_term=i.get('LeaseTerm')
                ).first()
                if rent:
                    rent.rent = i.get('Rent')
                    rent.corporate_rent = i.get('CorporateRent')
                    rent.furnished_rent = i.get('FurnishedRent')
                    rent.updated_datetime = func.now() #########
                else:
                    rent_matrix_record = RentMatrixData(
                        apartement=apartment.apartment_no,
                        move_in_date=i.get('MoveInDate'),
                        lease_term=i.get('LeaseTerm'),
                        rent=i.get('Rent'),
                        corporate_rent=i.get('CorporateRent'),
                        furnished_rent=i.get('FurnishedRent')
                    )
                    session_mutiple.add(rent_matrix_record)
                session_mutiple.commit()

            session_mutiple.commit()
            session_mutiple.close()
            return item

        except Exception as e:
            session_mutiple.rollback()
            raise DropItem(f"Database error: {e}")

        finally:
            session_mutiple.close()


    def close_spider(self, spider):
        self.Session_multiple().close()




class UrdSingleTablePipeline:
    def open_spider(self, spider):
        # single column implementation
        engine_single = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module5_single')
        Base_single_table.metadata.create_all(engine_single)
        self.Session_single = sessionmaker(bind=engine_single)

    def process_item(self, item, spider):

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

        self.Session_single().add(single_record)
        self.Session_single().commit()
        self.Session_single().close()
        return item

    def close_spider(self, spider):
        self.Session_single().close()




class PostScrapeMySQLPipeline:
    def __init__(self):
        self.file_path = "data.json"  # adjust as needed

    def open_spider(self, spider):
        # Set up the DB connection
        self.engine_post_scraping = create_engine("mysql+mysqlconnector://root:root@localhost:3306/module_5_post_scraping_db")
        Base_post_scraping_table.metadata.create_all(self.engine_post_scraping)
        self.Session_post_scraing = sessionmaker(bind=self.engine_post_scraping)


    def close_spider(self, spider):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            spider.logger.error(f"Failed to read JSON file: {e}")
            return

        session = self.Session_post_scraing()
        for row in data:
            print(f"row----> : {row}")
            try:
                post_scraping = PostScraping(
                    community_name=row.get('community_name'),
                    community_address=row.get('community_address'),
                    community_rent=row.get('community_rent'),
                    community_rooms=row.get('community_rooms'),
                    community_description=row.get('community_description'),
                    apartment_no=row.get('apartment_no'),
                    no_of_bedrooms=row.get('no_of_bedrooms'),
                    no_of_bathrooms=row.get('no_of_bathrooms'),
                    area=row.get('area'),
                    floor_no=row.get('floor_no'),
                    availability=row.get('availability'),
                    deposit=row.get('deposit'),
                    Max_rent=row.get('Max_rent'),
                    Min_rent=row.get('Min_rent'),
                    amenities=', '.join(row.get('amenities', [])),
                    community_amenities=', '.join(row.get('community_amenities', [])) if row.get(
                        'community_amenities') else '',
                    move_in_date=row.get('move_in_date'),
                    lease_term=row.get('lease_term'),
                    rent=row.get('rent'),
                    corporate_rent=row.get('corporate_rent'),
                    furnished_rent=row.get('furnished_rent'),
                )
                session.add(post_scraping)
            except Exception as e:
                spider.logger.error(f"Failed to insert item: {row}\nError: {e}")
        session.commit()
        session.close()
