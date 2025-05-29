class UrdScraperDatabase:
    def open_spider(self, spider):
        # single column implementation
        engine_single = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module5_single')
        Base_single_table.metadata.create_all(engine_single)
        self.Session_single = sessionmaker(bind=engine_single)

        # multiple column implementation
        engine_multiple = create_engine('mysql+mysqlconnector://root:root@localhost:3306/module_5_multiple')
        Base_multiple_table.metadata.create_all(engine_multiple)
        self.Session_multiple = sessionmaker(bind=engine_multiple)


    def process_item(self, item, spider):


        session_single = self.Session_single()

        single_record = Udr(
            community_name=item.get('community_name'),
            community_address=item.get('community_address'),
            community_rent=item.get('community_rent'),
            community_rooms=item.get('community_rooms'),
            community_description=item.get('community_description'),
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
            community_amenities=', '.join(item.get('community_amenities', [])) if item.get(
                'community_amenities') else '',
            move_in_date = item.get('move_in_date'),
            lease_term = item.get('lease_term'),
            rent = item.get('rent'),
            corporate_rent = item.get('corporate_rent'),
            furnished_rent = item.get('furnished_rent'),
        )

        session_single.add(single_record)
        session_single.commit()
        session_single.close()


        session_mutiple = self.Session_multiple()
        try:
            community = session_mutiple.query(CommunityData).filter_by(name=item['community_name']).first()
            if community:
                community.community_name = item.get('community_name'),
                community.community_address = item.get('community_address'),
                community.community_rent = item.get('community_rent'),
                community.community_rooms = item.get('community_rooms'),
                community.community_description = item.get('community_description'),
                community.community_amenities = ', '.join(item.get('community_amenities', [])) if item.get(
                    'community_amenities') else ''

            else:
                community = insert(CommunityData).values(
                    community_name=item.get('community_name'),
                    community_address=item.get('community_address'),
                    community_rent=item.get('community_rent'),
                    community_rooms=item.get('community_rooms'),
                    community_description=item.get('community_description'),
                    community_amenities = ', '.join(item.get('community_amenities', [])) if item.get('community_amenities') else ''
                )
                session_mutiple.add(community)
                session_mutiple.commit()


            apartment = session_mutiple.query(ApartmentData).filter_by(
                community=community.community_name,
                apartment_no=item['apartment_no']
            ).first()
            if apartment:
                apartment.apartment_no = item.get('apartment_no'),
                apartment.community = item.get('community_name'),
                apartment.no_of_bedrooms = item.get('no_of_bedrooms'),
                apartment.no_of_bathrooms = item.get('no_of_bathrooms'),
                apartment.area = item.get('area'),
                apartment.floor_no = item.get('floor_no'),
                apartment.availability = item.get('availability'),
                apartment.deposit = item.get('deposit'),
                apartment.Max_rent = item.get('Max_rent'),
                apartment.Min_rent = item.get('Min_rent'),
                apartment.amenities = ', '.join(item.get('amenities', []))
            # insert(ApartmentData).values
            else:
                apartment = ApartmentData(
                apartment_no =item.get('apartment_no'),
                community = item.get('community_name'),
                no_of_bedrooms=item.get('no_of_bedrooms'),
                no_of_bathrooms=item.get('no_of_bathrooms'),
                area=item.get('area'),
                floor_no=item.get('floor_no'),
                availability=item.get('availability'),
                deposit=item.get('deposit'),
                Max_rent=item.get('Max_rent'),
                Min_rent=item.get('Min_rent'),
                amenities=', '.join(item.get('amenities', []))
                )
                # session_mutiple.add(community)
                # session_mutiple.commit()

            # Implemented Insert Ignore for community data
            stmt = apartment.prefix_with('IGNORE')
            session_mutiple.execute(stmt)

            # Implemented Insert Ignore for apartment data
            session_mutiple.add(apartment)
            session_mutiple.commit()

            for i in item['raw_rent_matrix']:
                rent = session_mutiple.query(i).filter_by(
                    apartment_id=apartment.id,
                ).first()
                if rent:
                    rent.apartement = item.get('apartment_no')
                    rent.move_in_date = i.get('MoveInDate')
                    rent.lease_term = i.get('LeaseTerm')
                    rent.rent = i.get('Rent')
                    rent.corporate_rent = i.get('CorporateRent')
                    rent.session_mutiple.add(rent_matrix_record)
                else:
                    rent_matrix_record = RentMatrixData(
                    apartement = item.get('apartment_no'),
                    move_in_date = i.get('MoveInDate'),
                    lease_term = i.get('LeaseTerm'),
                    rent = i.get('Rent'),
                    corporate_rent = i.get('CorporateRent'),
                    furnished_rent = i.get('FurnishedRent'))
                    session_mutiple.add(rent_matrix_record)
                session_mutiple.commit()

            session_mutiple.commit()
            session_mutiple.close()
            return item

        except Exception as e:
            session_mutiple.rollback()
            raise DropItem(f"Database error: {e}")

        finally:
            session_mutiple.close()


    def close_spider(self, spider):
        self.Session_single.dispose()
        self.Session_multiple.dispose()
