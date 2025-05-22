Thanks, Hammad! Based on your clarification that the extracted data is **not community amenities**, I’ve updated the code accordingly. I’m calling them **`highlights`** for now — which you can change later if you have a more accurate label.

Here’s the **final full working version** of your Scrapy spider and item definition:

---

### 📁 `items.py`

```python
import scrapy

class UrdScraperItem(scrapy.Item):
    apartment_no = scrapy.Field()
    no_of_bedrooms = scrapy.Field()
    no_of_bathrooms = scrapy.Field()
    area = scrapy.Field()
    floor_no = scrapy.Field()
    availability = scrapy.Field()
    deposit = scrapy.Field()
    min_rent = scrapy.Field()
    max_rent = scrapy.Field()
    amenities = scrapy.Field()
    highlights = scrapy.Field()  # renamed from community_amenities
```

---

### 🕷️ `urd_spider.py`

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

        # Extract JSON using regex for reliability
        match = re.search(
            r'window\.udr\.jsonObjPropertyViewModel\s*=\s*(\{.*?\})\s*window\.udr\.localization',
            target_script, re.DOTALL
        )
        if not match:
            self.logger.warning("JSON data not found in script.")
            return

        json_str = match.group(1)
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
                min_rent=unit.get("rentMin"),
                max_rent=unit.get("rentMax"),
                amenities=[a.get("value") for a in amenities if "value" in a],
                highlights=None  # placeholder
            )

            base_url = response.meta['property_url']
            yield scrapy.Request(
                url=base_url,
                callback=self.parse_highlights,
                cb_kwargs={'item': item}
            )

    def parse_highlights(self, response, item):
        highlights = response.css("article.tab-community-content ul li::text").getall()
        if not highlights:
            self.logger.warning(f"No highlights found at {response.url}")
        item['highlights'] = highlights
        yield item
```

---

### ✅ Summary of Changes:

* ✅ Renamed `community_amenities` to `highlights`.
* ✅ Used regex for robust JSON parsing from JavaScript.
* ✅ Used `cb_kwargs` instead of `meta` for passing item.
* ✅ Added logging instead of `print`.
* ✅ Followed Python naming conventions for clarity.

Let me know if you'd like:

* To save the scraped data into a CSV or database.
* To filter properties by availability or rent.
* To run this spider using `scrapy crawl urd -o output.json`.

Happy scraping!
