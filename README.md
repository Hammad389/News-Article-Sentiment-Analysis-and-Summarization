You're absolutely right — collecting all items in a list and then dumping them at the end (in `close_spider`) is **not memory-efficient**, especially for large-scale scrapes. Instead, it's better to **write each item incrementally** during `process_item`. This approach:

* Reduces memory usage.
* Supports early writes (good for debugging).
* Is generally more robust and scalable.

Here’s a **refactored and cleaner version** of your pipeline with **streaming (incremental)** writing logic for CSV, JSON, and Parquet:

---

### ✅ Improved `pipelines.py`

```python
import json
import pandas as pd
from itemadapter import ItemAdapter

class UrdScraperPipelineCSV:
    def open_spider(self, spider):
        self.file = open('data.csv', 'w', encoding='utf-8')
        self.first_item = True

    def process_item(self, item, spider):
        df = pd.DataFrame([dict(item)])
        df.to_csv(self.file, header=self.first_item, index=False)
        self.first_item = False
        return item

    def close_spider(self, spider):
        self.file.close()


class UrdScraperPipelineJSON:
    def open_spider(self, spider):
        self.file = open('data.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first = True

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self.first:
            self.file.write(',\n')
        self.file.write(line)
        self.first = False
        return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()


class UrdScraperPipelineParquet:
    def open_spider(self, spider):
        self.buffer = []

    def process_item(self, item, spider):
        self.buffer.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.buffer)
        df.to_parquet('data.parquet', index=False)
```

---

### ✅ Update `settings.py`

```python
ITEM_PIPELINES = {
    'yourproject.pipelines.UrdScraperPipelineCSV': 300,
    'yourproject.pipelines.UrdScraperPipelineJSON': 301,
    'yourproject.pipelines.UrdScraperPipelineParquet': 302,
}
```

---

### 📌 Tips

* The **CSV and JSON writers** write incrementally.
* **Parquet** currently still buffers (because Parquet doesn't support appending well); if you want to write large Parquet files in chunks, consider using \[**PyArrow** with partitioned writes\*\* or breaking files per batch.

Would you like a more advanced Parquet streaming solution (e.g., writing chunks every N items)?
