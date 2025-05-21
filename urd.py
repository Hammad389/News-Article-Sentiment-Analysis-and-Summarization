import scrapy
import requests
from selectolax.parser import HTMLParser
import chompjs
from urd_scraper.items import UrdScraperItem
import json
import re

class UrdSpider(scrapy.Spider):
    name = "urd"
    allowed_domains = ["urd.com"]
    start_urls = ["https://www.udr.com/"]

    # we can try to merge both functions
    def parse(self, response):
        links = response.css("ul[class='cities'] > li > a::attr(href)").extract()
        states_link = [f"{response.urljoin(link)}map/" for link in links]
        for link in states_link:
            yield scrapy.Request(link, callback=self.states_data_scraper)

    def states_data_scraper(self, response):
        property_links = response.css("div[class='address-section'] > a[class='prop-link']::attr(href)").extract()
        complete_property_links = [response.urljoin(link) for link in property_links]
        for link in complete_property_links:
            print(f"link:{link}")
            yield scrapy.Request(f"{link}apartments-pricing/",callback=self.apartments_pricing_scraper )

    def apartments_pricing_scraper(self, response):
        raw_data = response.css("script[type='text/javascript']::text").extract()
        starting_extra_tag = "window.udr.jsonObjPropertyViewModel = "
        ending_extra_tag =  "window.udr.localization ="
        filter_start_point = [m.end() for m in re.finditer(starting_extra_tag,raw_data[2])][0]
        filter_end_point = [m.start() for m in re.finditer(ending_extra_tag,raw_data[2])][0]
        formatted_data = json.loads(raw_data[2][filter_start_point:filter_end_point].strip().strip(';'))

        # formatted_data = json.loads(raw_data[2].strip()[129:-591])
        for data in formatted_data["floorPlans"]:
            items = UrdScraperItem(
            apartment_no = data["units"][0]["marketingName"],
            no_of_bedrooms = data["units"][0]["bedrooms"],
            no_of_bathrooms = data["units"][0]["bathrooms"],
            area = data["units"][0]["sqFt"],
            floor_no = data["units"][0]["floorNumber"],
            availability = data["units"][0]["isAvailable"],
            deposit = data["units"][0]["deposit"],
            Max_rent = data["units"][0]["rentMin"],
            Min_rent = data["units"][0]["rentMax"],
            amenities = [line['value'] for line in data[0]["units"][0]["amenities"]]
            )
            yield items




