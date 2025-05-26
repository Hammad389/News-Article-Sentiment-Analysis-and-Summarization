Great! If you want to:

* **Save data into a single table in one database**, and
* **Save data into multiple tables in a different database**,

…**in the same Scrapy project**, here's how you can do it cleanly using **SQLAlchemy** and **a custom pipeline design**.

---

## ✅ Approach Overview

You can build **a single pipeline** that:

* Initializes two SQLAlchemy engines:

  * `engine_main` → Single table (e.g., `Udr`) in Database A
  * `engine_logs` → Multiple tables (e.g., `Udr`, `AuditLog`, etc.) in Database B
* During `process_item`, insert the item into both databases — with separate logic for each.

---

## ✅ Example Setup

### `models.py`

Assume both databases use the same models:

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime

Base = declarative_base()

class Udr(Base):
    __tablename__ = 'udr'
    id = Column(Integer, primary_key=True)
    community_name = Column(String(255))
    community_address = Column(String(255))
    community_rent = Column(String(50))
    community_rooms = Column(String(50))
    apartment_no = Column(String(50))
    no_of_bedrooms = Column(String(50))
    no_of_bathrooms = Column(String(50))
    area = Column(String(50))
    floor_no = Column(String(50))
    availability = Column(String(50))
    deposit = Column(String(50))
    Max_rent = Column(String(50))
    Min_rent = Column(String(50))
    amenities = Column(Text)
    community_amenities = Column(Text)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String(255))
    user = Column(String(100))
    timestamp = Column(DateTime)
    status = Column(String(100))
```

---

### `pipelines.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urd_scraper.models import Base, Udr, AuditLog
from datetime import datetime

class MultiDBPipeline:
    def open_spider(self, spider):
        # Engine A: Single-table DB (only Udr)
        self.engine_main = create_engine("mysql+mysqlconnector://root:root@localhost:3306/single_table_db")
        Base.metadata.create_all(self.engine_main)
        self.SessionMain = sessionmaker(bind=self.engine_main)

        # Engine B: Multi-table DB (Udr + AuditLog)
        self.engine_logs = create_engine("mysql+mysqlconnector://root:root@localhost:3306/multi_table_db")
        Base.metadata.create_all(self.engine_logs)
        self.SessionLogs = sessionmaker(bind=self.engine_logs)

    def process_item(self, item, spider):
        # Save to single-table DB
        session_main = self.SessionMain()
        main_record = Udr(
            community_name=item.get('community_name'),
            community_address=item.get('community_address'),
            community_rent=item.get('community_rent'),
            community_rooms=item.get('community_rooms'),
            apartment_no=item.get('apartment_no'),
            no_of_bedrooms=item.get('no_of_bedrooms'),
            no_of_bathrooms=item.get('no_of_bathrooms'),
            area=item.get('area'),
            floor_no=item.get('floor_no'),
            availability=item.get('availability'),
            deposit=item.get('deposit'),
            Max_rent=item.get('Max_rent'),
            Min_rent=item.get('Min_rent'),
            amenities=', '.join(item.get('amenities', [])),
            community_amenities=', '.join(item.get('community_amenities', [])) if item.get('community_amenities') else ''
        )
        session_main.add(main_record)
        session_main.commit()
        session_main.close()

        # Save to multi-table DB
        session_logs = self.SessionLogs()

        # Save Udr data
        log_udr = Udr(**main_record.__dict__)
        del log_udr.__dict__['_sa_instance_state']  # Prevent SQLAlchemy warning
        session_logs.add(log_udr)

        # Log entry (optional)
        log = AuditLog(
            action='Insert UDR record',
            user='scrapy_bot',
            timestamp=datetime.now(),
            status='Success'
        )
        session_logs.add(log)

        session_logs.commit()
        session_logs.close()

        return item
```

---

### `settings.py`

```python
ITEM_PIPELINES = {
    'urd_scraper.pipelines.MultiDBPipeline': 300,
}
```

---

## ✅ Summary

| Database          | Table(s)           | Action                  |
| ----------------- | ------------------ | ----------------------- |
| `single_table_db` | `udr`              | Save only UDR data      |
| `multi_table_db`  | `udr`, `audit_log` | Save UDR and log record |

---

## Want more?

Would you like to:

* Add a switch to enable/disable either DB?
* Save CSV or Parquet alongside DB?
* Encrypt or anonymize sensitive fields (e.g., address)?

Let me know — I can help you extend this flexibly.
