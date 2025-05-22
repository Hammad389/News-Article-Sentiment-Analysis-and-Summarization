You're exactly right, Hammad.

If you want to avoid using `items.py` (Scrapy's `Item` class) and instead use **plain Python dictionaries** (which is often preferred for flexibility and easier integration), here's how you can modify your spider:

---

### **Modified Version of Your Spider (No items.py)**

```python
import scrapy
import json
import re


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

        try:
            start_tag = "window.udr.jsonObjPropertyViewModel ="
            end_tag = "window.udr.localization ="
            start_index = target_script.index(start_tag) + len(start_tag)
            end_index = target_script.index(end_tag)
            json_str = target_script[start_index:end_index].strip().rstrip(";")
            formatted_data = json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Failed to extract JSON: {e}")
            return

        for data in formatted_data.get("floorPlans", []):
            units = data.get("units", [])
            if not units:
                continue
            unit = units[0]
            amenities = unit.get("amenities", [])

            item = {
                "apartment_no": unit.get("marketingName"),
                "no_of_bedrooms": unit.get("bedrooms"),
                "no_of_bathrooms": unit.get("bathrooms"),
                "area": unit.get("sqFt"),
                "floor_no": unit.get("floorNumber"),
                "availability": unit.get("isAvailable"),
                "deposit": unit.get("deposit"),
                "Max_rent": unit.get("rentMin"),
                "Min_rent": unit.get("rentMax"),
                "amenities": [a.get("value") for a in amenities if "value" in a],
                "community_amenities": None
            }

            yield scrapy.Request(
                url=response.meta['property_url'],
                callback=self.parse_community_amenities,
                meta={'item': item}
            )

    def parse_community_amenities(self, response):
        item = response.meta['item']
        amenities = response.css("article.tab-community-content ul li::text").getall()
        item['community_amenities'] = [a.strip() for a in amenities if a.strip()]
        yield item
```

---

### **Why This Approach Works Well:**

* No need for `items.py` or `Item` objects.
* You can easily `json.dump()` or insert these dicts directly into a DB.
* No rigid field structure: missing keys won’t break the pipeline.
* You can dynamically add/remove fields based on scraping logic.

---

Let me know if you also want an example of how to save the yielded dictionaries into JSON or a database.
