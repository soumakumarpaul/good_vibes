import pandas as pd
from tinydb import TinyDB
from datetime import datetime

file_path = "/Users/priya/Library/CloudStorage/OneDrive-S&PBeautyVentures/Automation/"

df = pd.read_excel(file_path + "PriceList.xlsx", sheet_name="WeddingMakeup")

db = TinyDB(file_path + 'services_db.json')
for index, row in df.iterrows():
    service = {}
    service['id'] = f"MK-WDNG-{str(index+1).zfill(3)}"
    service['name'] = row['Service Name']
    service['category'] = "Makeup"
    service['sub-category'] = "Wedding"
    service['price'] = row['Service Price'] 
    db.insert(service)
