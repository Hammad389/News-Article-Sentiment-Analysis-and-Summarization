# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
import pandas as pd
from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UrdScraperPipeline_csv:
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


class UrdScraperPipeline_json:
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

class UrdScraperPipeline_parquet:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_parquet('data.parquet', index=False)


