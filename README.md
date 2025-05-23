Thanks for sharing your full code, Hammad! You're on the right track, but there are some bugs and memory issues in your pipeline implementations. Here's how you can fix and simplify your CSV, JSON, and Parquet pipelines:

---

### ✅ CSV Pipeline (Write row-by-row with header once)

```python
import csv

class UrdScraperPipeline_csv:
    def open_spider(self, spider):
        self.file = open('data.csv', 'w', newline='', encoding='utf-8')
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
```

---

### ✅ JSON Pipeline (Write as a valid JSON array without loading all in memory)

```python
import json

class UrdScraperPipeline_json:
    def open_spider(self, spider):
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
```

---

### ✅ Parquet Pipeline (Buffered, use only if memory is sufficient)

```python
import pandas as pd

class UrdScraperPipeline_parquet:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_parquet('data.parquet', index=False)
```

---

### 📌 `settings.py` (Enable the pipelines)

```python
ITEM_PIPELINES = {
    'your_project_name.pipelines.UrdScraperPipeline_csv': 300,
    'your_project_name.pipelines.UrdScraperPipeline_json': 301,
    'your_project_name.pipelines.UrdScraperPipeline_parquet': 302,
}
```

Replace `'your_project_name'` with the actual Scrapy project folder name.

---

Let me know if you want to:

* Save only one format at a time via a setting
* Upload to cloud (like S3 or GCS)
* Automatically timestamp filenames (`data_2025-05-23.json`)

Happy scraping!
