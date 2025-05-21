# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UrdScraperItem(scrapy.Item):
    # define the fields for your item here like:
    apartment_no = scrapy.Field()
    no_of_bedrooms = scrapy.Field()
    no_of_bathrooms = scrapy.Field()
    area = scrapy.Field()
    floor_no = scrapy.Field()
    availability = scrapy.Field()
    deposit = scrapy.Field()
    Max_rent = scrapy.Field()
    Min_rent = scrapy.Field()
    amenities = scrapy.Field()
