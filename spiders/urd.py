from email.contentmanager import raw_data_manager

import scrapy
import json
import re
# from urd_scraper.items import UrdScraperItem


class UrdSpider(scrapy.Spider):
    name = "urd"
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
                                   'community_rent':[community_rent.strip("Starting at ") if "Starting at " in community_rent else community_rent][0],
                                   'community_rooms':tags.css("div [class='card-property-info'] ul li span[class='bed-max']::text").get(),
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
                "community_rent" : meta_data["community_rent"],
                "community_rooms": meta_data["community_rooms"],
                "community_description": meta_data["community_description"],
                "apartment_no" : unit.get("marketingName"),
                "no_of_bedrooms" : unit.get("bedrooms"),
                "no_of_bathrooms" : unit.get("bathrooms"),
                "area" : unit.get("sqFt"),
                "floor_no" : unit.get("floorNumber"),
                "availability" : unit.get("isAvailable"),
                "deposit" : unit.get("deposit"),
                "Max_rent" : unit.get("rentMax"),
                "Min_rent" : unit.get("rentMin"),
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

