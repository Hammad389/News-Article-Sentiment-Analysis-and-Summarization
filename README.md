Thanks for sharing the updated code! You're on the right track, but since you asked earlier about **adding community amenities** from a different page, and currently your spider **isn't doing that yet**, here's how to modify your code so that it:

### ✅ 1. Visits both:

* `/apartments-pricing/` (unit-specific data),
* and the **main property page** (e.g., `/property-name/`) for **community amenities**.

### ✅ 2. Adds the community amenities to your final item.

---

## 🛠 Final Updated Spider Code

```python
import scrapy
import json
import re
from urd_scraper.items import UrdScraperItem


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
        property_links = response.css("div.address-section a.prop-link::attr(href)").getall()
        complete_property_links = [response.urljoin(link) for link in property_links]
        for link in complete_property_links:
            # Save base property URL for later use
            yield scrapy.Request(
                url=f"{link}apartments-pricing/",
                callback=self.apartments_pricing_scraper,
                meta={'property_url': link}
            )

    def apartments_pricing_scraper(self, response):
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

            item = UrdScraperItem(
                apartment_no=unit.get("marketingName"),
                no_of_bedrooms=unit.get("bedrooms"),
                no_of_bathrooms=unit.get("bathrooms"),
                area=unit.get("sqFt"),
                floor_no=unit.get("floorNumber"),
                availability=unit.get("isAvailable"),
                deposit=unit.get("deposit"),
                Max_rent=unit.get("rentMin"),
                Min_rent=unit.get("rentMax"),
                amenities=[a.get("value") for a in amenities if "value" in a],
                community_amenities=None  # Placeholder, will be updated
            )

            # Visit property page to get community amenities
            base_url = response.meta['property_url']
            yield scrapy.Request(
                url=base_url,
                callback=self.parse_community_amenities,
                meta={'item': item}
            )

    def parse_community_amenities(self, response):
        item = response.meta['item']
        amenities = response.css("div.community-amenities li::text").getall()
        cleaned = [a.strip() for a in amenities if a.strip()]
        item['community_amenities'] = cleaned
        yield item
```

---

## 📝 `items.py` (Make sure it has this field too)

```python
class UrdScraperItem(scrapy.Item):
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
    community_amenities = scrapy.Field()  # New field!
```

---

## 🧪 Final Note:

Make sure the selector in `parse_community_amenities`:

```python
response.css("div.community-amenities li::text")
```

matches the **real HTML** on the UDR site. If you’re unsure, inspect the property detail page and paste the relevant snippet here — I’ll help fine-tune the selector.

Let me know if you'd like to combine the requests or optimize for performance with `cb_kwargs` or `inline_requests`.
