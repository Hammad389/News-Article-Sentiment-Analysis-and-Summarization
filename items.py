from email.contentmanager import raw_data_manager

import scrapy
import json
import re


class UrdSpider(scrapy.Spider):
    name = "udr"
    allowed_domains = ["udr.com"]
    start_urls = ["https://www.udr.com/"]


    def parse(self, response):
        links = response.css("ul.cities li a::attr(href)").getall()
        states_link = [f"{response.urljoin(link)}map/" for link in links]
        for link in states_link:
            yield scrapy.Request(link, callback=self.states_data_scraper)


    def states_data_scraper(self, response):
        for tags in response.css("div[class='front card-properties']"):
            raw_community_address = tags.css("div.address-section a.prop-link> span.address::text").getall()
            community_rent = tags.css("div [class='card-property-info'] ul li span[class='rent-min']::text").get()
            community_data_dict = {'community_link':response.urljoin(tags.css("div.address-section a.prop-link::attr(href)").get()),
                                   'community_name':tags.css("div.address-section a.prop-link span.prop-name::text").get(),
                                   'community_address':('').join(s.strip() for s in raw_community_address),
                                   # added adjustments to have a clean value
                                   'community_rent':[community_rent.strip("Starting at $") if "Starting at $" in community_rent else community_rent][0],
                                   'community_rooms':tags.css("div [class='card-property-info'] ul li span[class='bed-max']::text").get().strip("Bedrooms").strip(),
                                   'community_description':tags.css("div [class='card-property-info'] p::text").get().strip()
                                   }
            yield scrapy.Request(
                url=f"{community_data_dict["community_link"]}apartments-pricing/",
                callback=self.apartments_pricing_scraper,
                meta = {'meta_data':community_data_dict}
            )

    def apartments_pricing_scraper(self, response):
        # Data from the previous function
        meta_data = response.meta['meta_data']

        scripts = response.css("script::text").getall()
        target_script = next((s for s in scripts if "window.udr.jsonObjPropertyViewModel" in s), None)

        if not target_script:
            self.logger.warning(f"No data script found in {response.url}")
            return

        start_tag = "window.udr.jsonObjPropertyViewModel ="
        end_tag = "window.udr.localization ="
        start_index = target_script.index(start_tag) + len(start_tag)
        end_index = target_script.index(end_tag)
        json_str = target_script[start_index:end_index].strip().rstrip(";")
        formatted_data = json.loads(json_str)

        for data in formatted_data.get("floorPlans", []):
            units = data.get("units", [])
            if not units:
                continue
            unit = units[0]
            amenities = unit.get("amenities", [])

            item = {
                "community_name" : meta_data["community_name"],
                "community_address" : meta_data["community_address"],
                "community_rent" : int(meta_data["community_rent"].strip("$").replace(',','')),
                "community_rooms": int(meta_data["community_rooms"]),
                "community_description": meta_data["community_description"],
                "apartment_no" : unit.get("marketingName").strip(),
                "no_of_bedrooms" : int(unit.get("bedrooms")),
                "no_of_bathrooms" : int(unit.get("bathrooms")),
                "area" : int(unit.get("sqFt")),
                "floor_no" : int(unit.get("floorNumber")),
                "availability" : unit.get("isAvailable"),
                "deposit" : float(unit.get("deposit")),
                "Max_rent" : float(unit.get("rentMax")),
                "Min_rent" : float(unit.get("rentMin")),
                "amenities" : [a.get("value") for a in amenities if "value" in a],
                "community_amenities" : None
            }

            # Visit property page to get community amenities
            base_url = f"{meta_data['community_link']}amenities/"
            # print(f"url:{base_url}")
            yield scrapy.Request(
                url=base_url,
                callback=self.parse_community_amenities,
                meta={'items': item}
            )

    def parse_community_amenities(self, response):
        item = response.meta['items']
        amenities = response.css("article[class='tab-content tab-community-content expand-wrapper body-copy'] ul li::text").extract()
        item['community_amenities'] = amenities
        yield item

# Scrapy settings for urd_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "urd_scraper"

SPIDER_MODULES = ["urd_scraper.spiders"]
NEWSPIDER_MODULE = "urd_scraper.spiders"

CONNECTION_STRING = 'mysql+mysqlconnector://root:root@localhost:3306/module_5'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "urd_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "urd_scraper.middlewares.UrdScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "urd_scraper.middlewares.UrdScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "urd_scraper.pipelines.UrdScraperPipelineCsv": 300,
      "urd_scraper.pipelines.UrdScraperPipelineJson": 301,
   "urd_scraper.pipelines.UrdScraperPipelineParquet": 302,
   "urd_scraper.pipelines.SingleTableDatabase": 303
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
from xmlrpc.client import Boolean

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
# from urd_scraper.models import create_table, Udr, db_connect
from urd_scraper.models import create_table, Udr, db_connect
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
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_parquet('data.parquet', index=False)

class SingleTableDatabase:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        udr = Udr
        udr.community_name = item['community_name']
        udr.community_address = item['community_address']
        udr.community_rent = item['community_rent']
        udr.community_rooms = item['community_rooms']
        udr.community_description = item['community_description']
        udr.apartment_no = item['apartment_no']
        udr.no_of_bedrooms = item['no_of_bedrooms']
        udr.no_of_bathrooms = item['no_of_bathrooms']
        udr.area = item['area']
        udr.floor_no = item['floor_no']
        udr.availability = item['availability']
        udr.community_rent = item['community_rent']
        udr.deposit = item['deposit']
        udr.Max_rent = item['Max_rent']
        udr.Min_rent = item['Min_rent']
        udr.amenities = str(item['amenities'])
        udr.community_amenities = str(item['community_amenities'])
        try:
            session.add(udr)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item































    # engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5', echo=True)
    # conn = engine.connect()
    #
    # meta = MetaData()
    #
    # def open_spider(self, spider, meta, engine):
    #
    #     people = Table(
    #         "udr_data",
    #         meta,
    #         Column('id', types.Integer, primary_key=True, autoincrement=True),
    #         Column('coummunity_name', types.String, nullable=False),
    #         Column('coummunity_address', types.String, nullable=False),
    #         Column('coummunity_community_rent', types.Integer, nullable=True),
    #         Column('community_rooms', types.Integer, nullable=False),
    #         Column('apartment_no', types.String, nullable=False),
    #         Column('no_of_bedrooms', types.Integer, nullable=False),
    #         Column('no_of_bathrooms', types.Integer, nullable=False),
    #         Column('area', types.Integer, nullable=False),
    #         Column('floor_no', types.Integer, nullable=False),
    #         Column('availability', types.Boolean, nullable=False),
    #         Column('deposit', types.Float, nullable=False),
    #         Column('Max_rent', types.Float, nullable=False),
    #         Column('Min_rent', types.Float, nullable=False),
    #         Column('Max_rent', types.Integer, nullable=False),
    #         Column('amenities', types.String, nullable=False),
    #         Column('community_amenities', types.String, nullable=False)
    #     )
    #     meta.create_all(engine)
from sqlalchemy import Column, create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    try:
        Base.metadata.create_all(engine)
        print("Table created!")
    except:
        print("Error while creating table.")

def Udr(Base):
    __tablename__="udr_data"

    id = Column(Integer, autoincrement=True, primary_key=True)
    coummunity_name = Column(String, nullable=False)
    coummunity_address = Column(String, nullable=False)
    coummunity_community_rent = Column(Integer, nullable=True)
    community_rooms = Column(Integer, nullable=False)
    apartment_no = Column(String, nullable=False)
    no_of_bedrooms = Column(Integer, nullable=False)
    no_of_bathrooms = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)
    floor_no = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False)
    deposit = Column(Float, nullable=False)
    Max_rent = Column(Float, nullable=False)
    Min_rent = Column(Float, nullable=False)
    Max_rent = Column(Integer, nullable=False)
    amenities = Column(String, nullable=False)
    community_amenities = Column(String, nullable=False)
