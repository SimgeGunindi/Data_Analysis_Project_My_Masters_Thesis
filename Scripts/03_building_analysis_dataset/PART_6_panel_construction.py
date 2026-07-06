# =============================================================================
# PART 6
# CALCULATING NEW WEATHER VARIABLES (MAKING NEW WEATHER COLUMNS) TO USE IN THE ANALYSIS
# AGGREGATION (weather stations -> provinces of Spain, and daily data -> monthly)
# =============================================================================


# =============================================================================
# 90TH and 95TH PERCENTILE HEAT FLAGS
# =============================================================================


import pandas as pd

df = pd.read_csv("verA_sorted_by_comunidad_2.csv")

df["fecha"] = pd.to_datetime(df["fecha"])

# COMPUTE 90th and 95th percentiles per station
percentiles = (
    df.groupby("indicativo")[["tmax", "tmed"]]
    .quantile([0.9, 0.95])
    .unstack()
)
percentiles.columns = [f"{col}_{int(p*100)}th" for col, p in percentiles.columns]
percentiles = percentiles.reset_index()

# MERGE BACK TO MAIN DATA
df = df.merge(percentiles, on="indicativo", how="left")

# FLAG HEAT DAYS (90th and 95th)
df["tmax90_flag"] = (df["tmax"] > df["tmax_90th"]).astype(int)
df["tmax95_flag"] = (df["tmax"] > df["tmax_95th"]).astype(int)

df["tmed90_flag"] = (df["tmed"] > df["tmed_90th"]).astype(int)
df["tmed95_flag"] = (df["tmed"] > df["tmed_95th"]).astype(int)

# SAVE
df.to_csv("verA_with_flags.csv", index=False)


# =============================================================================
# 2+ VE 3+ DAYS (HEATWAVE DAYS)
# =============================================================================


import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("verA_with_flags.csv", parse_dates=['fecha'])

station_col = "indicativo"

# Sort by station and date
df = df.sort_values([station_col, 'fecha'])

# Function to create consecutive-day flags
def consecutive_days_flag(series, n_days=2):
    flag = np.zeros(len(series), dtype=int)
    count = 0
    for i, val in enumerate(series):
        if val:
            count += 1
            if count >= n_days:
                flag[i] = 1
        else:
            count = 0
    return flag

# Columns that already exist as base flags
base_flags = ['tmax95_flag','tmax90_flag','tmed95_flag','tmed90_flag']

# Apply 2+ and 3+ consecutive day flags per station
for station in df[station_col].unique():
    mask = df[station_col] == station
    for col in base_flags:
        df.loc[mask, f"{col}_2plus"] = consecutive_days_flag(df.loc[mask, col], n_days=2)
        df.loc[mask, f"{col}_3plus"] = consecutive_days_flag(df.loc[mask, col], n_days=3)

# Check
print(df[[station_col,'fecha'] + [f"{col}_2plus" for col in base_flags] + [f"{col}_3plus" for col in base_flags]].head(20))

# Save
df.to_csv("verA_flags_2plus3plus.csv", index=False)


# =============================================================================
# TEMPERATURE BINS (DECILES) 
# =============================================================================


import pandas as pd

# Load
df = pd.read_csv("verA_flags_2plus3plus.csv")

# Columns in the dataset
date_col = "fecha"
station_col = "indicativo"
province_col = "provincia"
tmax_col = "tmax"
tmed_col = "tmed"

# Compute deciles per station 
#For tmax
df['tmax_decile'] = df.groupby(station_col)[tmax_col]\
                      .transform(lambda x: pd.qcut(x, 10, labels=False, duplicates='drop') + 1)
#For tmed
df['tmed_decile'] = df.groupby(station_col)[tmed_col]\
                      .transform(lambda x: pd.qcut(x, 10, labels=False, duplicates='drop') + 1)

# Create flags for each decile
#Function to create flags
def create_decile_flags(df, decile_col, prefix):
    for i in range(1, 11):
        df[f"{prefix}_decile_{i}_flag"] = (df[decile_col] == i).astype(int)
    return df

df = create_decile_flags(df, 'tmax_decile', 'tmax')
df = create_decile_flags(df, 'tmed_decile', 'tmed')

#save
df.to_csv("station_decile_flags.csv", index=False)

# check data types
print(df.dtypes)


# =============================================================================
# HUMIDITY BINS (DECILES)
# =============================================================================


# Load raw data
import pandas as pd

df = pd.read_csv("station_decile_flags.csv")

# Columns
date_col = "fecha"
station_col = "indicativo"
province_col = "provincia"
tmax_col = "tmax"
tmed_col = "tmed"
hr_col = "hrMedia"   # <-- new humidity variable

# Compute deciles per station

df['hr_decile'] = df.groupby(station_col)[hr_col]\
                    .transform(lambda x: pd.qcut(x, 10, labels=False, duplicates='drop') + 1)

# Create flags for each decile
def create_decile_flags(df, decile_col, prefix):
    for i in range(1, 11):
        df[f"{prefix}_decile_{i}_flag"] = (df[decile_col] == i).astype(int)
    return df


df = create_decile_flags(df, 'hr_decile', 'hr')

# Save
df.to_csv("station_decile_flags_humbins.csv", index=False)



# =============================================================================
# AGGREGATION 
# STATION LEVEL -> PROVINCE LEVEL
# DAILY -> MONTHLY
# aggregating all columns (except prec) -> taking  mean
# prec -> taking sum
# =============================================================================



import pandas as pd
import numpy as np

# Load station-level dataset
df = pd.read_csv("station_decile_flags_humbins.csv")

# Define column names
date_col = "fecha"
station_col = "indicativo"
province_col = "provincia"

prec_col = "prec"  

# Convert date column to datetime
df[date_col] = pd.to_datetime(df[date_col])

# Identify numeric columns (weather + flags)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Daily aggregation -> (station to province)
#Take the mean across stations (spatial aggregation) (fractions for flags, avg for temp)
prov_daily = (
    df.groupby([province_col, date_col])[numeric_cols]
    .mean()
    .reset_index()
)

# Add year-month info
prov_daily["year"] = prov_daily[date_col].dt.year
prov_daily["month"] = prov_daily[date_col].dt.month
prov_daily["year_month"] = prov_daily[date_col].dt.to_period("M").astype(str)

# Monthly aggregation -> (daily to monthly)
#Sum precipitation, mean for everything else
agg_dict = {col: "mean" for col in numeric_cols}
if prec_col in agg_dict:
    agg_dict[prec_col] = "sum"

prov_monthly = (
    prov_daily.groupby([province_col, "year_month"])
    .agg(agg_dict)
    .reset_index()
)

# Save
prov_daily.to_csv("prov_day_precsum_weather.csv", index=False)
prov_monthly.to_csv("prov_month_PRECSUM_weather.csv", index=False)

