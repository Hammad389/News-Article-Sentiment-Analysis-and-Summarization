Thanks, Hammad — here is the **complete Scrapy pipeline code** that matches your SQLAlchemy `model.py` design, including:

* Deduplication logic (`INSERT IGNORE` behavior)
* Handling foreign key relationships
* Clean insertion into the three tables:

  * `CommunityData`
  * `ApartmentData`
  * `RentMatrixData`

---

### ✅ `pipelines.py` (SQLAlchemy-based Scrapy pipeline)

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from .model import Base, CommunityData, ApartmentData, RentMatrixData

class MySQLStorePipeline:
    def __init__(self):
        # Replace with your credentials
        self.engine = create_engine("mysql+mysqlconnector://username:password@localhost/dbname")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            # 1. Handle Community
            community = session.query(CommunityData).filter_by(name=item['community_name']).first()
            if not community:
                community = CommunityData(
                    name=item['community_name'],
                    address=item['address'],
                    phone=item.get('phone'),
                    email=item.get('email'),
                    website=item.get('website'),
                    amenities=",".join(item.get('amenities', []))
                )
                session.add(community)
                session.commit()  # Commit so it gets an ID

            # 2. Handle Apartment
            apartment = session.query(ApartmentData).filter_by(
                community_id=community.id,
                floor_plan=item['apartment_floor_plan']
            ).first()

            if not apartment:
                apartment = ApartmentData(
                    community_id=community.id,
                    floor_plan=item['apartment_floor_plan'],
                    beds=item.get('beds'),
                    baths=item.get('baths'),
                    square_feet=item.get('square_feet'),
                    availability=item.get('availability'),
                    amenities=",".join(item.get('apartment_amenities', []))
                )
                session.add(apartment)
                session.commit()

            # 3. Handle Rent Matrix
            rent_key = {
                'apartment_id': apartment.id,
                'unit_number': item.get('unit_number'),
                'available_from': item.get('available_from'),
                'lease_length': item.get('lease_length'),
            }
            rent_matrix = session.query(RentMatrixData).filter_by(**rent_key).first()
            if not rent_matrix:
                rent_matrix = RentMatrixData(
                    apartment_id=apartment.id,
                    unit_number=item.get('unit_number'),
                    rent=item.get('rent'),
                    available_from=item.get('available_from'),
                    lease_length=item.get('lease_length')
                )
                session.add(rent_matrix)

            session.commit()
            return item

        except Exception as e:
            session.rollback()
            raise DropItem(f"Failed to insert due to error: {e}")
        finally:
            session.close()
```

---

### 🧩 Integration into `settings.py`

Make sure you enable the pipeline:

```python
ITEM_PIPELINES = {
   'yourproject.pipelines.MySQLStorePipeline': 300,
}
```

---

Let me know if you're also exporting to JSON/CSV/Parquet in parallel or want to cache relationships to reduce DB hits for speed.
