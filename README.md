Sure, Hammad! Below are **three separate Scrapy pipelines** that store your scraped dictionary data into:

1. **JSON**
2. **CSV**
3. **Parquet**

You can plug all of these into your `pipelines.py` file.

---

### **1. JSON Pipeline**

```python
import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("output_data.json", "w", encoding="utf-8")
        self.file.write("[")  # Start of list
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("]")  # End of list
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(",\n")
        self.file.write(json.dumps(item, ensure_ascii=False))
        self.first_item = False
        return item
```

---

### **2. CSV Pipeline**

```python
import csv

class CsvWriterPipeline:
    def open_spider(self, spider):
        self.file = open("output_data.csv", "w", newline="", encoding="utf-8")
        self.writer = None

    def process_item(self, item, spider):
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
            self.writer.writeheader()
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
```

---

### **3. Parquet Pipeline**

```python
import pandas as pd

class ParquetWriterPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))  # Ensure it's a plain dict
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_parquet("output_data.parquet", index=False)
```

> **Note:** You need to install `pyarrow` or `fastparquet` for Parquet:

```bash
pip install pyarrow
```

---

### **Enable Pipelines in `settings.py`**

```python
ITEM_PIPELINES = {
    'yourproject.pipelines.JsonWriterPipeline': 300,
    'yourproject.pipelines.CsvWriterPipeline': 301,
    'yourproject.pipelines.ParquetWriterPipeline': 302,
}
```

Replace `'yourproject'` with your Scrapy project name or correct Python path.

---

Let me know if you want to conditionally activate only one based on a flag or argument.
