import json
from collections import defaultdict
from tinydb import TinyDB

db = TinyDB("../../services_db.json")
flat_services = db.all()

grouped = defaultdict(lambda: defaultdict(list))

for item in flat_services:
    category = item.get("category")
    sub_category = item.get("sub-category")
    name = item.get("name")
    price = item.get("price")

    if category and sub_category and name:
        grouped[category][sub_category].append({
            "name": name,
            "price": price
        })

nested_services = []
for category, sub_map in grouped.items():
    catalog = []
    for sub_category, services in sub_map.items():
        catalog.append({"sub-category": sub_category, "services": services})
    nested_services.append({"category": category,"catalog": catalog})

nested_db = TinyDB("../../catalog_db.json")
nested_db.insert_multiple(nested_services)
    