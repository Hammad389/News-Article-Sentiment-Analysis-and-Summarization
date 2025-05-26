To save your Scrapy `urd` data to a **MySQL database using SQLAlchemy**, you'll need to:

1. **Fix and structure your SQLAlchemy table correctly.**
2. **Define a pipeline in `pipelines.py` to insert each item.**
3. **Enable the pipeline in your `settings.py`.**

---

### ✅ Step 1: Correct SQLAlchemy Table Setup (Use This in a Separate File e.g., `db_model.py`)

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UDRData(Base):
    __tablename__ = "udr_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    community_name = Column(String, nullable=False)
    community_address = Column(String, nullable=False)
    community_rent = Column(Float, nullable=True)
    community_rooms = Column(Integer, nullable=True)
    apartment_no = Column(String, nullable=True)
    no_of_bedrooms = Column(Integer, nullable=True)
    no_of_bathrooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    floor_no = Column(Integer, nullable=True)
    availability = Column(Boolean, nullable=True)
    deposit = Column(Float, nullable=True)
    Max_rent = Column(Float, nullable=True)
    Min_rent = Column(Float, nullable=True)
    amenities = Column(String, nullable=True)
    community_amenities = Column(String, nullable=True)
```

---

### ✅ Step 2: Pipeline to Save Scrapy Item

Create or edit `pipelines.py`:

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from yourproject.db_model import UDRData, Base  # Replace 'yourproject' with your actual project folder

class MySQLAlchemyPipeline:
    def open_spider(self, spider):
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        record = UDRData(
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
        session.add(record)
        session.commit()
        session.close()
        return item
```

---

### ✅ Step 3: Enable the Pipeline in `settings.py`

Add this:

```python
ITEM_PIPELINES = {
    'yourproject.pipelines.MySQLAlchemyPipeline': 300,
}
```

Replace `yourproject` with your actual Scrapy project name.

---

### Optional Tips:

* Make sure your MySQL server is running.
* Ensure that your `module_5` database exists before running.
* Install dependencies if missing:

```bash
pip install sqlalchemy mysql-connector-python
```

Let me know if you want to also save into **CSV or Parquet** along with SQL — I can help set up multiple pipelines.
