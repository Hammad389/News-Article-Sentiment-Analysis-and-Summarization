# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UrdScraperPipeline_csv:
    def open_spider(self,spider):
        self.file = open('data.csv', 'w', encoding='utf-8')
        self.first_item = True

    def process_item(self, item, spider):
        df = pd.DataFrame(item)
        df.to_csv(self.file, header=self.first_item, index=False)
        self.first_item=False
        return item

    def close_spider(self, spider):
        self.file.close()


class UrdScraperPipeline_json:
    def open_spider(self,spider):
        self.file = open('data.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first = True

    def process_item(self, item, spider):
        line = json.dump(item)
        if not self.first:
            self.file.write(',\n')
            self.file.write(line)
            self.first = False
            return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

class UrdScraperPipeline_parquet:
    def open_spider(self, spider):
        self.file = []

    def process_item(self, item, spider):
        self.file.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.file)
        df.to_parquet('data.parquet', index=False)


