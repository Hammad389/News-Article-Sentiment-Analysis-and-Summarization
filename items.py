Perfect. You want to **update existing records using unique fields** like:

* `community_name` → for identifying & updating `CommunityData`
* `floor_plan` + `community_id` → for identifying & updating `ApartmentData`
* `unit_number` + `apartment_id` → for identifying & updating `RentMatrixData`

Here's the complete revised code to meet all of these requirements.

---

## ✅ `model.py` (with `created` and `updated` columns)

```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class CommunityData(Base):
    __tablename__ = 'community_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    address = Column(String(255))
    phone = Column(String(100))
    email = Column(String(100))
    website = Column(String(255))
    amenities = Column(String(500))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    apartments = relationship("ApartmentData", back_populates="community")

class ApartmentData(Base):
    __tablename__ = 'apartment_data'

    id = Column(Integer, primary_key=True)
    community_id = Column(Integer, ForeignKey('community_data.id'))
    floor_plan = Column(String(255))  # Treated as unique within the same community
    beds = Column(Integer)
    baths = Column(Float)
    square_feet = Column(Integer)
    availability = Column(String(100))
    amenities = Column(String(500))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    community = relationship("CommunityData", back_populates="apartments")
    rents = relationship("RentMatrixData", back_populates="apartment")

class RentMatrixData(Base):
    __tablename__ = 'rent_matrix_data'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment_data.id'))
    unit_number = Column(String(50))  # Considered unique within an apartment
    rent = Column(Float)
    available_from = Column(String(100))
    lease_length = Column(String(100))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    apartment = relationship("ApartmentData", back_populates="rents")
```

---

## ✅ `pipelines.py`

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from .model import Base, CommunityData, ApartmentData, RentMatrixData
from datetime import datetime

class MySQLStorePipeline:
    def __init__(self):
        self.engine = create_engine("mysql+mysqlconnector://username:password@localhost/dbname")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            # === 1. Handle CommunityData ===
            community = session.query(CommunityData).filter_by(name=item['community_name']).first()
            if community:
                community.address = item['address']
                community.phone = item.get('phone')
                community.email = item.get('email')
                community.website = item.get('website')
                community.amenities = ",".join(item.get('amenities', []))
                community.updated = datetime.utcnow()
            else:
                community = CommunityData(
                    name=item['community_name'],
                    address=item['address'],
                    phone=item.get('phone'),
                    email=item.get('email'),
                    website=item.get('website'),
                    amenities=",".join(item.get('amenities', [])),
                )
                session.add(community)
                session.flush()  # So we can get community.id

            # === 2. Handle ApartmentData (using floor_plan + community_id) ===
            apartment = session.query(ApartmentData).filter_by(
                community_id=community.id,
                floor_plan=item['apartment_floor_plan']
            ).first()

            if apartment:
                apartment.beds = item.get('beds')
                apartment.baths = item.get('baths')
                apartment.square_feet = item.get('square_feet')
                apartment.availability = item.get('availability')
                apartment.amenities = ",".join(item.get('apartment_amenities', []))
                apartment.updated = datetime.utcnow()
            else:
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
                session.flush()

            # === 3. Handle RentMatrixData (using unit_number + apartment_id) ===
            rent = session.query(RentMatrixData).filter_by(
                apartment_id=apartment.id,
                unit_number=item.get('unit_number')
            ).first()

            if rent:
                rent.rent = item.get('rent')
                rent.available_from = item.get('available_from')
                rent.lease_length = item.get('lease_length')
                rent.updated = datetime.utcnow()
            else:
                rent = RentMatrixData(
                    apartment_id=apartment.id,
                    unit_number=item.get('unit_number'),
                    rent=item.get('rent'),
                    available_from=item.get('available_from'),
                    lease_length=item.get('lease_length')
                )
                session.add(rent)

            session.commit()
            return item

        except Exception as e:
            session.rollback()
            raise DropItem(f"Database error: {e}")
        finally:
            session.close()
```

---

## 🔄 Summary

| Table          | Unique Key Used for Update   | Update Logic                 |
| -------------- | ---------------------------- | ---------------------------- |
| CommunityData  | `name`                       | Uses `.filter_by(name=...)`  |
| ApartmentData  | `floor_plan + community_id`  | Unique within each community |
| RentMatrixData | `unit_number + apartment_id` | Unique within apartment      |

Let me know if you want to add logging or deduplication logic for JSON/CSV too.
