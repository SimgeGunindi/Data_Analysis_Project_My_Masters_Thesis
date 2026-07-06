# =============================================================================
# PART 2
# CLEANING THE DAILY WEATHER STATION DATA
# THERE ARE IN TOTAL 5208 CSV FILES FETCHED WITH THE API KEY
# =============================================================================


# =============================================================================
# Merging all the meteorological files
# Checking the data and performing initial basic cleaning 
# =============================================================================


import os
import pandas as pd

path = 'not sharing here'
# dir_data = '2017_part_1/868'
# dir_data = '2017_part_2/868'
# dir_data = '2018_part_1/864'
# dir_data = '2018_part_2/866'
# dir_data = '2019_part_1/868'
dir_data = '2019_part_2/874'

list_csv = [f for f in os.listdir('%s/%s'%(path,dir_data)) if f.endswith('.csv')]
df = pd.DataFrame()

for i, csv in enumerate(list_csv):
    print('%d/%d'%(i, len(list_csv)))
    tmp = pd.read_csv('%s/%s/%s'%(path,dir_data,csv))
    df = pd.concat([df, tmp]).reset_index(drop=True)
    

# 'prec' has sometimes have 'Ip' 'Acum'.
df = df[~df['prec'].isin(['Ip', 'Acum'])].reset_index(drop=True)

#column transformation
comma_cols = ['tmed', 'prec', 'tmin', 'tmax', 'velmedia', 'racha', 'presMax', 'presMin']
for col in comma_cols:
    df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
df[comma_cols] = df[comma_cols].astype('float32')

df['fecha'] = pd.to_datetime(df['fecha'])

df.to_csv('%s/%s.csv'%(path, dir_data.split('/')[0]), index=False)
# df.memory_usage(deep=True).sum() / (1024**2)
# np.float64(153.77209281921387)
# df.memory_usage(deep=True).sum() / (1024**2)
# Out[52]: np.float64(94.01651096343994)



list_csv = ['2017_part_1.csv',
             '2017_part_2.csv',
             '2018_part_1.csv',
             '2018_part_2.csv',
             '2019_part_1.csv',
             '2019_part_2.csv',
             ]
df = pd.DataFrame()

for i, csv in enumerate(list_csv):
    print('%d/%d'%(i, len(list_csv)))
    tmp = pd.read_csv('%s/%s'%(path,csv))
    df = pd.concat([df, tmp]).reset_index(drop=True)



# data & location
# temperature
# wind
# humidity
# pressure
# precipitation & sunshine

new_order = [
    'fecha', 'indicativo', 'nombre', 'provincia', 'altitud',
    'tmed', 'tmin', 'horatmin', 'tmax', 'horatmax',
    'dir', 'velmedia', 'racha', 'horaracha',
    'hrMedia', 'hrMax', 'horaHrMax', 'hrMin', 'horaHrMin',
    'presMax', 'horaPresMax', 'presMin', 'horaPresMin',
    'prec', 'sol'
]

df = df[new_order]


missing_ratio = df.isna().mean().sort_values(ascending=False)
print(missing_ratio)
print(missing_ratio)
'''
sol            0.831165
horaPresMin    0.762405
horaPresMax    0.762401
presMax        0.762395
presMin        0.762395
horaracha      0.209065
dir            0.209050
racha          0.208996
velmedia       0.204930
hrMedia        0.050681
horaHrMax      0.047673
horaHrMin      0.047598
hrMax          0.047321
hrMin          0.047282
prec           0.025345
horatmin       0.024494
horatmax       0.024064
tmed           0.018184
tmin           0.017920
tmax           0.017734
indicativo     0.000000
fecha          0.000000
nombre         0.000000
provincia      0.000000
altitud        0.000000
'''


# Making sure 'fecha' is datetime type and transform it
df['fecha'] = pd.to_datetime(df['fecha'])

df['year'] = df['fecha'].dt.year
df['month'] = df['fecha'].dt.month
df['day'] = df['fecha'].dt.day

df.drop(columns=['fecha'], inplace=True)

new_order = [
    'year', 'month', 'day', 
    'indicativo', 'nombre', 'provincia', 'altitud',
    'tmed', 'tmin', 'horatmin', 'tmax', 'horatmax',
    'dir', 'velmedia', 'racha', 'horaracha',
    'hrMedia', 'hrMax', 'horaHrMax', 'hrMin', 'horaHrMin',
    'presMax', 'horaPresMax', 'presMin', 'horaPresMin',
    'prec', 'sol'
]
df = df[new_order]
df.to_csv('%s/S0.csv'%(path), index=False)


# more cleaning:
all_year_month = set(df[['year', 'month']].drop_duplicates().itertuples(index=False, name=None))
station_year_month = df.groupby('indicativo')[['year', 'month']].apply(lambda x: set(x.itertuples(index=False, name=None)))
stations_with_all = station_year_month[station_year_month.apply(lambda x: all_year_month.issubset(x))].index.tolist()

print(f"Stations with complete data: {len(stations_with_all)}")
print(stations_with_all)



# changed the file name, continuing:
df = pd.read_csv('merged.csv')

#drop the ones that won't be used for the analysis
df.drop(['altitud', 'horatmin', 'horatmax', 'dir', 'horaracha',
         'horaHrMax', 'horaHrMin', 'presMax', 'horaPresMax', 'presMin', 'horaPresMin', 'sol'],
        axis=1, inplace=True)

#dates again
df['fecha'] = pd.to_datetime(df[['year', 'month', 'day']])
df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')

#save intermediate csv files as backup
df.to_csv('merged2.csv', index=False)

# unify the province names (of Spain)

merged2 = pd.read_csv("merged2.csv")

name_map = {
    "BALEARES": "ILLES BALEARS",
    "STA. CRUZ DE TENERIFE": "SANTA CRUZ DE TENERIFE"
}

merged2["provincia"] = merged2["provincia"].replace(name_map)

merged2["provincia"].nunique()

merged2.to_excel("merged2_cleaned.xlsx", index=False)


# =============================================================================
# Duplicates 
# Missing values
# Dates
# Data types
# =============================================================================


import pandas as pd

merged2_cleaned = pd.read_excel("merged2_cleaned.xlsx") 

# Remove duplicates
merged2_cleaned = merged2_cleaned.drop_duplicates(subset=["indicativo", "fecha"])  # station + date


merged2_cleaned.to_csv("merged2_cleaned_1.csv", index=False)


merged2_cleaned_1 = pd.read_csv("merged2_cleaned_1.csv")  

#Check missing values
print("\nMissing values per column:")
print(merged2_cleaned_1.isna().sum())

# Convert date column to datetime
merged2_cleaned_1['fecha'] = pd.to_datetime(merged2_cleaned_1['fecha'], errors='coerce')

# Ensure numeric variables are numeric
numeric_cols = ['tmed', 'tmax', 'tmin','velmedia','racha','hrMedia','hrMax','hrMin','prec']
for col in numeric_cols:
    merged2_cleaned_1[col] = pd.to_numeric(merged2_cleaned_1[col], errors='coerce')

print("\nData types after cleaning:")
print(merged2_cleaned_1.dtypes)

merged2_cleaned_1.to_csv("merged2_cleaned_2.csv", index=False)  

'''
Missing values per column:
year               0
month              0
day                0
indicativo         0
nombre             0
provincia          0
tmed           16829
tmin           16585
tmax           16413
velmedia      189663
racha         193426
hrMedia        46905
hrMax          43796
hrMin          43760
prec           23457
fecha              0
dtype: int64

Data types after cleaning:
year                   int64
month                  int64
day                    int64
indicativo            object
nombre                object
provincia             object
tmed                 float64
tmin                 float64
tmax                 float64
velmedia             float64
racha                float64
hrMedia              float64
hrMax                float64
hrMin                float64
prec                 float64
fecha         datetime64[ns]
dtype: object

'''


# =============================================================================
# Checking outliers
# Inconsistent values
# =============================================================================


merged2_cleaned_2 = pd.read_csv("merged2_cleaned_2.csv")

#drop unnecessary columns
merged2_cleaned_2 = merged2_cleaned_2.drop(columns=["year", "month", "day"])

# Outliers

# List of numeric columns to check
num_cols = ["tmed", "tmin", "tmax", "velmedia", "racha", "hrMedia", "hrMax", "hrMin", "prec"]

# Function to detect outliers
def find_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    return outliers

# Apply for each column
for col in num_cols:
    outliers = find_outliers_iqr(merged2_cleaned_2, col)
    print(f"{col}: {len(outliers)} outliers")

# save
merged2_cleaned_2.to_csv("merged2_cleaned_2_incostoncesi.csv", index=False)

'''
tmed: 150 outliers
tmin: 272 outliers
tmax: 335 outliers
velmedia: 34796 outliers
racha: 23437 outliers
hrMedia: 516 outliers
hrMax: 36007 outliers
hrMin: 0 outliers
prec: 189230 outliers
'''



merged2_cleaned_2_incostoncesi = pd.read_csv("merged2_cleaned_2_incostoncesi.csv")

# Check tmax >= tmed >= tmin (ignoring NaNs)
temp_inconsistent = (
    (merged2_cleaned_2_incostoncesi["tmax"] < merged2_cleaned_2_incostoncesi["tmed"]) |
    (merged2_cleaned_2_incostoncesi["tmed"] < merged2_cleaned_2_incostoncesi["tmin"])
) & merged2_cleaned_2_incostoncesi[["tmax", "tmed", "tmin"]].notna().all(axis=1)

# Humidity check
hum_inconsistent = (
    (merged2_cleaned_2_incostoncesi["hrMedia"] < 0) |
    (merged2_cleaned_2_incostoncesi["hrMedia"] > 100) |
    (merged2_cleaned_2_incostoncesi["hrMax"] < 0) |
    (merged2_cleaned_2_incostoncesi["hrMax"] > 100) |
    (merged2_cleaned_2_incostoncesi["hrMin"] < 0) |
    (merged2_cleaned_2_incostoncesi["hrMin"] > 100)
) & merged2_cleaned_2_incostoncesi[["hrMedia", "hrMax", "hrMin"]].notna().all(axis=1)

# Rainfall check
rain_inconsistent = (merged2_cleaned_2_incostoncesi["prec"] < 0) & merged2_cleaned_2_incostoncesi["prec"].notna()

# Wind check (>=0)
wind_inconsistent = (
    (merged2_cleaned_2_incostoncesi["velmedia"] < 0) |
    (merged2_cleaned_2_incostoncesi["racha"] < 0)
) & merged2_cleaned_2_incostoncesi[["velmedia", "racha"]].notna().all(axis=1)

# Summary
summary = {
    "Temperature inconsistencies": temp_inconsistent.sum(),
    "Humidity inconsistencies": hum_inconsistent.sum(),
    "Rainfall inconsistencies": rain_inconsistent.sum(),
    "Wind inconsistencies": wind_inconsistent.sum()
}

print(summary)

'''
{'Temperature inconsistencies': 0, 'Humidity inconsistencies': 0, 'Rainfall inconsistencies': 0, 'Wind inconsistencies': 0}
'''


# =============================================================================
# Made 3 different versions of the clean data to decide which CSV is the most useful for the analysis
# 1st one includes every row (missing included), other 2 drops some missing rows,
# =============================================================================

# VERSION A: Keep all cleaned data
verA_all = merged2_cleaned_2_incostoncesi.copy()
verA_all.to_csv("verA_all_cleaned_with_flags.csv", index=False)

# VERSION B: Drop rows with any missing values in all main numeric columns
numeric_cols_all = ["tmed", "tmin", "tmax", "velmedia", "racha", "hrMedia", "hrMax", "hrMin", "prec"]
verB_noNaN_all = verA_all.dropna(subset=numeric_cols_all)
verB_noNaN_all.to_csv("verB_noNaN_all.csv", index=False)

# VERSION C: Drop rows only if temperature or humidity data is missing
# because the study focuses on temperature and humidity
numeric_cols_temp_hum = ["tmed", "tmin", "tmax", "hrMedia", "hrMax", "hrMin"]
verC_noNaN_temp_hum = verA_all.dropna(subset=numeric_cols_temp_hum)
verC_noNaN_temp_hum.to_csv("verC_noNaN_temp_hum.csv", index=False)


import pandas as pd

verA = pd.read_csv("verA_all_cleaned_with_flags.csv")
verB = pd.read_csv("verB_noNaN_all.csv")
verC = pd.read_csv("verC_noNaN_temp_hum.csv")

# Print row counts
print("Version A rows:", len(verA))
print("Version B rows:", len(verB))
print("Version C rows:", len(verC))

# rows dropped from A
print("Dropped A to B:", len(verA) - len(verB))
print("Dropped A to C:", len(verA) - len(verC))

'''
Version A rows: 925501
Version B rows: 693055
Version C rows: 854927
Dropped A to B: 232446
Dropped A to C: 70574
'''


# =============================================================================
# Sorting the dataset
# Matching/unifying all the location names
# =============================================================================


import pandas as pd

verA = pd.read_csv("verA_all_cleaned_with_flags.csv")

# Sort by province (alphabetical)
verA_sorted = verA.sort_values(by=['provincia', 'fecha']).reset_index(drop=True)

verA_sorted.to_csv("verA_sorted_by_provincia.csv", index=False)


import pandas as pd

verA_sorted_by_provincia = pd.read_csv("verA_sorted_by_provincia.csv")

set(verA_sorted_by_provincia.provincia)

'''
{'A CORUÑA',
 'ALBACETE',
 'ALICANTE',
 'ALMERIA',
 'ARABA/ALAVA',
 'ASTURIAS',
 'AVILA',
 'BADAJOZ',
 'BARCELONA',
 'BIZKAIA',
 'BURGOS',
 'CACERES',
 'CADIZ',
 'CANTABRIA',
 'CASTELLON',
 'CEUTA',
 'CIUDAD REAL',
 'CORDOBA',
 'CUENCA',
 'GIPUZKOA',
 'GIRONA',
 'GRANADA',
 'GUADALAJARA',
 'HUELVA',
 'HUESCA',
 'ILLES BALEARS',
 'JAEN',
 'LA RIOJA',
 'LAS PALMAS',
 'LEON',
 'LLEIDA',
 'LUGO',
 'MADRID',
 'MALAGA',
 'MELILLA',
 'MURCIA',
 'NAVARRA',
 'OURENSE',
 'PALENCIA',
 'PONTEVEDRA',
 'SALAMANCA',
 'SANTA CRUZ DE TENERIFE',
 'SEGOVIA',
 'SEVILLA',
 'SORIA',
 'TARRAGONA',
 'TERUEL',
 'TOLEDO',
 'VALENCIA',
 'VALLADOLID',
 'ZAMORA',
 'ZARAGOZA'}
'''


# Mapping provinces (above) to their autonomous communities (regions in Spain)

prov_to_comm = {
    # Andalucía
    "ALMERIA": "Andalucía",
    "CADIZ": "Andalucía",
    "CORDOBA": "Andalucía",
    "GRANADA": "Andalucía",
    "HUELVA": "Andalucía",
    "JAEN": "Andalucía",
    "MALAGA": "Andalucía",
    "SEVILLA": "Andalucía",

    # Aragón
    "HUESCA": "Aragón",
    "TERUEL": "Aragón",
    "ZARAGOZA": "Aragón",

    # Asturias
    "ASTURIAS": "Asturias (Comunidad)",

    # Baleares
    "ILLES BALEARS": "Islas Baleares",

    # Canarias
    "LAS PALMAS": "Canarias",
    "SANTA CRUZ DE TENERIFE": "Canarias",

    # Cantabria
    "CANTABRIA": "Cantabria (Comunidad)",

    # Castilla y León
    "AVILA": "Castilla y León",
    "BURGOS": "Castilla y León",
    "LEON": "Castilla y León",
    "PALENCIA": "Castilla y León",
    "SALAMANCA": "Castilla y León",
    "SEGOVIA": "Castilla y León",
    "SORIA": "Castilla y León",
    "VALLADOLID": "Castilla y León",
    "ZAMORA": "Castilla y León",

    # Castilla-La Mancha
    "ALBACETE": "Castilla-La Mancha",
    "CIUDAD REAL": "Castilla-La Mancha",
    "CUENCA": "Castilla-La Mancha",
    "GUADALAJARA": "Castilla-La Mancha",
    "TOLEDO": "Castilla-La Mancha",

    # Cataluña
    "BARCELONA": "Cataluña",
    "GIRONA": "Cataluña",
    "LLEIDA": "Cataluña",
    "TARRAGONA": "Cataluña",

    # Comunidad Valenciana
    "ALICANTE": "Comunidad Valenciana",
    "CASTELLON": "Comunidad Valenciana",
    "VALENCIA": "Comunidad Valenciana",

    # Extremadura
    "BADAJOZ": "Extremadura",
    "CACERES": "Extremadura",

    # Galicia
    "A CORUÑA": "Galicia",
    "LUGO": "Galicia",
    "OURENSE": "Galicia",
    "PONTEVEDRA": "Galicia",

    # Madrid
    "MADRID": "Comunidad de Madrid",

    # Murcia
    "MURCIA": "Región de Murcia",

    # Navarra
    "NAVARRA": "Navarra (Comunidad)",

    # País Vasco
    "ARABA/ALAVA": "País Vasco",
    "BIZKAIA": "País Vasco",
    "GIPUZKOA": "País Vasco",

    # La Rioja
    "LA RIOJA": "La Rioja (Comunidad)",

    # Ceuta
    "CEUTA": "Ceuta",

    # Melilla
    "MELILLA": "Melilla"
}

# Add Autonomous Community column
verA['comunidad'] = verA['provincia'].map(prov_to_comm)

# Check for any unmapped provinces
unmapped = verA[verA['comunidad'].isna()]['provincia'].unique()
if len(unmapped) > 0:
    print(" Unmapped provinces found:", unmapped)
else:
    print(" All provinces successfully mapped.")

# Sort by community + province + date
verA_sorted = verA.sort_values(by=['comunidad', 'provincia', 'fecha']).reset_index(drop=True)

# Save
verA_sorted.to_csv("verA_sorted_by_comunidad.csv", index=False)
