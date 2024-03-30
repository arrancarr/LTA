import os
import pytz
import requests
import pandas as pd
from datetime import datetime

carparks = []

# Timezone conversion to Singapore Time
singapore_zone = pytz.timezone('Asia/Singapore')
sg_datetime = datetime.now(singapore_zone).strftime("%d-%m-%Y_%H")
sg_date = datetime.now(singapore_zone).strftime("%d-%m-%Y")
sg_hour = datetime.now(singapore_zone).strftime("%H")

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"

url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"

querystring = {"skip":"0"}

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "AccountKey": SOME_SECRET
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
results = response.json()

dataset = results['value']
for data in dataset:
    carpark_id = data['CarParkID']
    area = data['Area']
    development = data['Development']

    try:
        latitude = data['Location'].split(" ")[0]
        longitude = data['Location'].split(" ")[1]
    except:
        latitude = None
        longitude = None

    available_Lots = data['AvailableLots']
    lot_type = data['LotType']
    agency = data['Agency']

    record = {
        "Carpark_ID": carpark_id,
        "Area": area,
        "Development": development,
        "Date": sg_date,
        "Hour": sg_hour,
        "Latitude": latitude,
        "Longitude": longitude,
        "Available Lots": available_Lots,
        "Lot_Type": lot_type,
        "Agency": agency
    }

    carparks.append(record)

df = pd.DataFrame(carparks)

def_list = [{"Lot_Type": "C", "Lot Type": "Cars"}, {"Lot_Type": "H", "Lot Type": "Heavy Vehicles"}, {"Lot_Type": "Y", "Lot Type": "Motorcycles"}]
df_def = pd.DataFrame(def_list)

df_final = df.merge(df_def, left_on="Lot_Type", right_on="Lot_Type")
df_final = df_final[['Carpark_ID', 'Area', 'Development', 'Date', 'Hour', 'Latitude', 'Longitude', 'Available Lots', 'Lot Type', 'Agency']]

# Create the tiprank folder if it doesn't exist
if not os.path.exists('LTA'):
    os.makedirs('LTA')

# Create CSV filename with current date and time
csv_filename = f"LTA/LTA_{sg_datetime}.csv"
  
# Dump dataframe to CSV
df_final.to_csv(csv_filename, index=False)
print(f"DataFrame dumped to {csv_filename}")
