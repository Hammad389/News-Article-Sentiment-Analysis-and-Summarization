# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
from xmlrpc.client import Boolean

import pandas as pd
from sqlalchemy import create_engine
from urd_scraper.models import Udr, Base, ApartmentData, CommunityData
from sqlalchemy.orm import sessionmaker, Session
from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UrdScraperPipelineCsv:
    def open_spider(self,spider):
        self.file = open('data.csv', 'w', encoding='utf-8')
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
        if len (self.items) >= 10:
            self.save_to_parquet()
        return item

    def save_to_parquet(self):
        df = pd.DataFrame(self.items)
        df.to_parquet('data.parquet', index=False)
        self.items.clear()

    def close_spider(self, spider):
        if self.items:
            self.save_to_parquet()

class SingleTableDatabase:
    # engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5')
    # def open_spider(self, spider):
        # Base.metadata.create_all(self.engine)
        # self.Session = sessionmaker(bind=self.engine)

    def open_spider(self, spider):
        # single column implementation
        engine_single = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5_single')
        Base.metadata.create_all(engine_single)
        self.Session_single = sessionmaker(bind=engine_single)

        # multiple column implementation
        engine_multiple = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5_mutiple')
        Base.metadata.create_all(engine_multiple)
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
                'community_amenities') else ''
        )
        session_single.add(single_record)
        session_single.commit()
        session_single.close()
        # return item

        session_mutiple = self.Session_multiple()
        multiple_record_community = CommunityData(
            community_name=item.get('community_name'),
            community_address=item.get('community_address'),
            community_rent=item.get('community_rent'),
            community_rooms=item.get('community_rooms'),
            community_description=item.get('community_description')
        )
        multiple_record_apartment = ApartmentData(
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
                'community_amenities') else ''
        )
        session_mutiple.add(multiple_record_community)
        session_mutiple.add(multiple_record_apartment)
        session_mutiple.commit()
        session_mutiple.close()
        return item

    # def close_spider(self, spider):
    #     self.engine.dispose()



# # Starting to add multiple tables
# class MultipleTableDatabase:
#     engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/Module_5_MutipleTables")
#     def open_spider(self, spider):
#         # engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/Module_5_MutipleTables")
#         Base.metadata.create_all( self.engine)
#         self.Session = sessionmaker(bind= self.engine)
#
#     def process_item(self, item, spider):
#         session = self.Session()
#         community_record = CommunityData(
#             community_name=item.get('community_name'),
#             community_address=item.get('community_address'),
#             community_rent=item.get('community_rent'),
#             community_rooms=item.get('community_rooms'),
#             community_description=item.get('community_description')
#         )
#
#         apartment_record = ApartmentData(
#             apartment_no=item.get('apartment_no'),
#             no_of_bedrooms=item.get('no_of_bedrooms'),
#             no_of_bathrooms=item.get('no_of_bathrooms'),
#             area=item.get('area'),
#             floor_no=item.get('floor_no'),
#             availability=item.get('availability'),
#             deposit=item.get('deposit'),
#             Max_rent=item.get('Max_rent'),
#             Min_rent=item.get('Min_rent'),
#             amenities=', '.join(item.get('amenities', [])),
#             community_amenities=', '.join(item.get('community_amenities', [])) if item.get(
#                 'community_amenities') else ''
#         )
#         session.add(community_record)
#         session.add(apartment_record)
#         session.commit()
#         session.close()
#         session.close()
#         return item
#
#     def close_spider(self, spider):
#         self.engine.dispose()


