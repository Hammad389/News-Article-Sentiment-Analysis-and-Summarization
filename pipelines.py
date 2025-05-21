# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UrdScraperPipeline:
    def open_spider(self,spider):
        self.items = []


    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open ("data.json", "w") as file:
            json.dump(self.items, file)

        df = pd.DataFrame(self.items)
        df.to_csv('data.csv', index=False)
        df.to_parquet('data.parquet', index=False)

