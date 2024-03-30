import os
import pytz
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Timezone conversion to Singapore Time
singapore_zone = pytz.timezone('Asia/Singapore')
sg_datetime = datetime.now(singapore_zone).strftime("%d-%m-%Y_%H")
sg_date = datetime.now(singapore_zone).strftime("%d-%m-%Y")
sg_hour = datetime.now(singapore_zone).strftime("%H")

legend = [
    {"Code": "BPlus", "Name": "Bugis +"},
    {"Code": "CQ", "Name": "Clarke Quay"},
    {"Code": "FN", "Name": "Funan"},
    {"Code": "PS", "Name": "Plaza Singapura"},
    {"Code": "RCS", "Name": "Raffles City"},
    {"Code": "TAO", "Name": "The Atrium@Orchard"},
    {"Code": "BM", "Name": "Bedok Mall"},
    {"Code": "TM", "Name": "Tampines Mall"},
    {"Code": "BPP", "Name": "Bukit Panjang Plaza"},
    {"Code": "J8", "Name": "Junction 8"},
    {"Code": "LO", "Name": "Lot One"},
    {"Code": "IMM", "Name": "IMM"},
    {"Code": "WG", "Name": "Westgate"},
    {"Code": "CG", "Name": "CapitaGreen"},
    {"Code": "CT", "Name": "Capital Tower"},
    {"Code": "SBR", "Name": "Six Battery Road"},
    {"Code": "CS", "Name": "CapitaSpring"},
]

locations = []

url = "https://justpark.capitaland.com/LotsAvail"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, "html.parser")

section = soup.find("div", attrs={"class": "lots-form"})
boxes = section.find_all("div", attrs={"class": "listing-item"})

for box in boxes:
    div = box.find("div", attrs={"class": "lotscount"})
    name = div['id'].split("onClickSeason")[1]
    available_lots = div.find("span").text
    
    record = {
        "Code": name,
        "Date": sg_date,
        "Hour": sg_hour,
        "Available Lots": available_lots
    }

    locations.append(record)

df_legend = pd.DataFrame(legend)
df = pd.DataFrame(locations)
df_final = df_legend.merge(df, left_on="Code", right_on="Code")

# Create the tiprank folder if it doesn't exist
if not os.path.exists('JustPark'):
    os.makedirs('JustPark')

# Create CSV filename with current date and time
csv_filename = f"JustPark/JustPark_{sg_datetime}.csv"
  
# Dump dataframe to CSV
df_final.to_csv(csv_filename, index=False)
print(f"DataFrame dumped to {csv_filename}")
