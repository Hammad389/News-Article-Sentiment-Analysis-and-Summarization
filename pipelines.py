
2025-05-26 15:09:35 [scrapy.core.scraper] ERROR: Error processing {'community_name': 'The Carriage Homes at Wyndham', 'community_address': '5600 Mulholland DriveGlen Allen, VA 23059', 'community_rent': 1499, 'community_rooms': 3, 'community_description': 'Part of the master-planned golf community of Wyndham, our townhomes are located in Richmond’s desirable West End.', 'apartment_no': '12102', 'no_of_bedrooms': 1, 'no_of_bathrooms': 1, 'area': 778, 'floor_no': 1, 'availability': True, 'deposit': 350.0, 'Max_rent': 1603.0, 'Min_rent': 1603.0, 'amenities': ['Updated interior', 'Espresso on granite finish package', 'Espresso cabinetry', 'Assigned parking space', 'Granite countertops', 'Stainless steel appliances', 'Carpet flooring', 'Smart home package', 'Patio/balcony', 'Walk-in closet', 'Soaking tub', 'Corner location', 'Tile floors in kitchen / bathroom'], 'community_amenities': ['24-hour fitness center', 'Billiards room', 'Community grilling space', 'Conference room', 'Dog park with agility equipment', 'Free weights', 'On-site maintenance', 'On-site storage', 'Outdoor Kitchen Cabana', 'Package lockers ', 'Pet friendly', 'Pickleball court', 'Playground', 'Prewired for Comcast and Verizon', 'Swimming pool', 'Walking paths']}
Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 3477, in add
    state = attributes.instance_state(instance)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'function' object has no attribute '_sa_instance_state'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\core\scraper.py", line 381, in start_itemproc
    output = await maybe_deferred_to_future(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\twisted\internet\defer.py", line 1088, in _runCallbacks
    current.result = callback(  # type: ignore[misc]
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\utils\defer.py", line 407, in f
    return deferred_from_coro(coro_f(*coro_args, **coro_kwargs))
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\urd_scraper\pipelines.py", line 94, in process_item
    session.add(udr)
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 3479, in add
    raise exc.UnmappedInstanceError(instance) from err
sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.function' is not mapped
