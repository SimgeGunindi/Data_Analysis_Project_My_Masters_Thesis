# #############################################################################
# ########### THE CODE OF MY APPLIED ECONOMICS MASTER THESIS ##################
# #############################################################################


# =============================================================================
# PART 1
# FETCHING 3 YEARS OF DAILY WEATHER STATION DATA USING THE API KEY FROM THE NATIONAL WEATHER AGENCY OF SPAIN (AEMET)
# =============================================================================


# =============================================================================
# Getting the list of weather stations to download the station-level datasets
# =============================================================================

import requests
import pandas as pd

api_key = "not sharing the real api key here"

inventory_url ="not sharing the real url here"

response = requests.get(inventory_url)
response.raise_for_status()
inventory_data = response.json()

stations_url = inventory_data['datos']

stations_response = requests.get(stations_url)
stations_response.raise_for_status()
stations_list = stations_response.json()

df_stations = pd.DataFrame(stations_list)
print(df_stations.head())

df_stations.to_excel("stations_list.xlsx", index=False)


# =============================================================================
# Fetching daily weather station data of Spain for 3 years (2017-2019)
# (due to the API restrictions, fetching can only happen with 6-month intervals)
# =============================================================================


# =============================================================================
# 2017 First 6 months
# =============================================================================

import os 
import time
import requests
import pandas as pd
from tqdm import tqdm


api_key = "not sharing the real api key here"

start_date = "2017-01-01T00:00:00UTC"
end_date = "2017-06-30T23:59:59UTC"

station_list_path = "stations_list.xlsx"
output_dir = "daily_weather_2017_first_half"
os.makedirs(output_dir, exist_ok=True)

# Load station list

stations_df = pd.read_excel(station_list_path)

if 'indicativo' not in stations_df.columns:
    raise ValueError("Excel file must contain a column named 'indicativo' (station code)")

station_codes = stations_df['indicativo'].dropna().unique()

#Fetch and save data for each station

for code in tqdm(station_codes, desc="Fetching station data"):
    try:
        output_file = os.path.join(output_dir, f"daily_{code}.csv")
        
     
        # Request data access URL
        url = (
            f"not sharing the real url here"
            f"fechaini/{start_date}/fechafin/{end_date}/estacion/{code}/?api_key={api_key}"
        )
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        response_json = response.json()

        data_url = response_json.get("datos")
        if not data_url:
            print(f"No 'datos' URL for {code}. Skipping.")
            continue

        #Download actual data
        data_response = requests.get(data_url, timeout=20)
        data_response.raise_for_status()
        data = data_response.json()

        # Save to CSV
        df = pd.DataFrame(data)
        if not df.empty:
            df.to_csv(output_file, index=False)
            print(f"Saved {code} to CSV.")
        else:
            print(f"Empty data for {code}. Skipped saving.")

        time.sleep(1)

    except Exception as e:
        print(f"Error with station {code}: {e}")
        continue

#512 out of 947 stations saved


# =============================================================================
# Retry fetching the remainig ones
# =============================================================================

import os
import time
import random
import requests
import pandas as pd
from tqdm import tqdm

api_key = "not sharing the real api key here"
start_date = "2017-01-01T00:00:00UTC"
end_date = "2017-06-30T23:59:59UTC"
station_list_path = "stations_list.xlsx"
output_dir = "daily_weather_2017_first_half"
os.makedirs(output_dir, exist_ok=True)

# Load station list
stations_df = pd.read_excel(station_list_path)
station_codes = stations_df['indicativo'].dropna().unique()

#Identify stations that are cannot yet downloaded
existing_files = set(f.replace("daily_", "").replace(".csv", "") for f in os.listdir(output_dir))
stations_to_retry = [code for code in station_codes if code not in existing_files]

#track ones that truly have no data:
no_data_list = []
still_failed = []


print(f"\nRetrying {len(stations_to_retry)} stations...\n")

for code in tqdm(stations_to_retry, desc="Retrying failed stations"):
    try:
        url = (
            f"not sharing the real url here"
            f"fechaini/{start_date}/fechafin/{end_date}/estacion/{code}/?api_key={api_key}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response_json = response.json()

        data_url = response_json.get("datos")
        if not data_url:
            print(f" No 'datos' for {code}. Logging and skipping.")
            no_data_list.append(code)
            continue

        data_response = requests.get(data_url, timeout=30)
        data_response.raise_for_status()
        data = data_response.json()

        df = pd.DataFrame(data)
        if not df.empty:
            output_file = os.path.join(output_dir, f"daily_{code}.csv")
            df.to_csv(output_file, index=False)
            print(f" Retried and saved {code}.")
        else:
            print(f" Empty data for {code}.")
            no_data_list.append(code)

        time.sleep(random.uniform(1.5, 4))

    except Exception as e:
        print(f" Still failed: {code}: {e}")
        still_failed.append(code)
        continue

# Optionally:
if no_data_list:
    with open("no_data_stations_8.txt", "w") as f:
        for code in no_data_list:
            f.write(f"{code}\n")
    print(f"\n Logged {len(no_data_list)} stations with no available data.")

#Log stations that still failed:
if still_failed:
    with open("still_failed_17.txt", "w") as f:
        for code in still_failed:
            f.write(f"{code}\n")
    print(f"\n {len(still_failed)} stations still failed. Logged to still_failed_17.txt")
else:
    print("\n All remaining stations successfully downloaded")

#667 stations are fetched so far.
#Logged 34 stations with no available data.
#246 stations still failed. Logged to still_failed_17.txt


# =============================================================================
# Retry
# =============================================================================

import os
import time
import random
import requests
import pandas as pd
from tqdm import tqdm


api_key = "..."
start_date = "2017-01-01T00:00:00UTC"
end_date = "2017-06-30T23:59:59UTC"
output_dir = "daily_weather_2017_first_half"
station_codes_file = "still_failed_17.txt"  

# Load station codes
with open(station_codes_file, "r") as f:
    station_codes = [line.strip() for line in f if line.strip()]

still_failed = []

print(f"\n Retrying final {len(station_codes)} stations with retries...\n")

for code in tqdm(station_codes, desc="Final retry pass"):
    success = False

    for attempt in range(3):
        try:
            url = (
                f"..."
                f"fechaini/{start_date}/fechafin/{end_date}/estacion/{code}/?api_key={api_key}"
            )
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data_url = response.json().get("datos")

            if not data_url:
                print(f" No 'datos' for {code}. Skipping.")
                break

            data_response = requests.get(data_url, timeout=60)
            data_response.raise_for_status()
            data = data_response.json()

            df = pd.DataFrame(data)
            if not df.empty:
                output_file = os.path.join(output_dir, f"daily_{code}.csv")
                df.to_csv(output_file, index=False)
                print(f" Done: {code}")
                success = True
                break
            else:
                print(f" Empty data for {code}. Skipping.")
                break

        except Exception as e:
            print(f" Attempt {attempt+1}/3 failed for {code}: {e}")
            time.sleep(random.uniform(2, 5))

    if not success:
        still_failed.append(code)

#Log stations that still failed
if still_failed:
    with open("still_failed_18.txt", "w") as f:
        for code in still_failed:
            f.write(f"{code}\n")
    print(f"\n {len(still_failed)} stations still failed. Logged to still_failed_18.txt")
else:
    print("\n All remaining stations successfully downloaded")

#857 stations are fetched so far
#56 stations still failed. Logged to still_failed_18.txt


# =============================================================================
# Retry
# =============================================================================
import os
import time
import random
import requests
import pandas as pd
from tqdm import tqdm


api_key = "..."
start_date = "2017-01-01T00:00:00UTC"
end_date = "2017-06-30T23:59:59UTC"
output_dir = "daily_weather_2017_first_half"
station_codes_file = "still_failed_18.txt"


with open(station_codes_file, "r") as f:
    station_codes = [line.strip() for line in f if line.strip()]

still_failed = []

print(f"\n Retrying final {len(station_codes)} stations with retries...\n")

for code in tqdm(station_codes, desc="Final retry pass"):
    success = False

    for attempt in range(3):
        try:
            url = (
                f"..."
                f"fechaini/{start_date}/fechafin/{end_date}/estacion/{code}/?api_key={api_key}"
            )
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data_url = response.json().get("datos")

            if not data_url:
                print(f" No 'datos' for {code}. Skipping.")
                break

            data_response = requests.get(data_url, timeout=60)
            data_response.raise_for_status()
            data = data_response.json()

            df = pd.DataFrame(data)
            if not df.empty:
                output_file = os.path.join(output_dir, f"daily_{code}.csv")
                df.to_csv(output_file, index=False)
                print(f" Done: {code}")
                success = True
                break
            else:
                print(f" Empty data for {code}. Skipping.")
                break

        except Exception as e:
            print(f" Attempt {attempt+1}/3 failed for {code}: {e}")
            time.sleep(random.uniform(2, 5))

    if not success:
        still_failed.append(code)

#Log stations that still failed 
if still_failed:
    with open("still_failed_19.txt", "w") as f:
        for code in still_failed:
            f.write(f"{code}\n")
    print(f"\n {len(still_failed)} stations still failed. Logged to still_failed_19.txt")
else:
    print("\n All remaining stations successfully downloaded")

#867 are fetched 


# =============================================================================
# The last try
# =============================================================================

import os
import time
import random
import requests
import pandas as pd
from tqdm import tqdm

api_key = "..."
start_date = "2017-01-01T00:00:00UTC"
end_date = "2017-06-30T23:59:59UTC"
output_dir = "daily_weather_2017_first_half"
station_codes_file = "still_failed_19.txt"

with open(station_codes_file, "r") as f:
    station_codes = [line.strip() for line in f if line.strip()]

still_failed = []

print(f"\n Retrying final {len(station_codes)} stations with retries...\n")

for code in tqdm(station_codes, desc="Final retry pass"):
    success = False

    for attempt in range(3):
        try:
            url = (
                f"..."
                f"fechaini/{start_date}/fechafin/{end_date}/estacion/{code}/?api_key={api_key}"
            )
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data_url = response.json().get("datos")

            if not data_url:
                print(f" No 'datos' for {code}. Skipping.")
                break

            data_response = requests.get(data_url, timeout=60)
            data_response.raise_for_status()
            data = data_response.json()

            df = pd.DataFrame(data)
            if not df.empty:
                output_file = os.path.join(output_dir, f"daily_{code}.csv")
                df.to_csv(output_file, index=False)
                print(f" Done: {code}")
                success = True
                break
            else:
                print(f" Empty data for {code}. Skipping.")
                break

        except Exception as e:
            print(f" Attempt {attempt+1}/3 failed for {code}: {e}")
            time.sleep(random.uniform(2, 5))

    if not success:
        still_failed.append(code)


if still_failed:
    with open("still_failed_20.txt", "w") as f:
        for code in still_failed:
            f.write(f"{code}\n")
    print(f"\n {len(still_failed)} stations still failed. Logged to still_failed_20.txt")
else:
    print("\n All remaining stations successfully downloaded") 

#868 out of 947 stations are available.
#This is the final number for the daily station data for 2017-01 to 2017-06. 
#Other remaining stations continously give errors or have empty data.


# =============================================================================
# The other remaning codes (2017-07 to 2019-12) are excluded from here due to being repetitive.
# =============================================================================