# =============================================================================
# PART 3
# MORTALITY DATA FROM NATIONAL STATISTICS INSTITUTE OF SPAIN (INE)
# Includes: year-month-province-age-sex-number of deaths
# =============================================================================


# =============================================================================
# Cleaning the mortality dataset
# =============================================================================

# =============================================================================
# Cleaning basics
# =============================================================================

import pandas as pd

# Load with ; separator
df = pd.read_csv("62281.csv", sep=";")

# Drop redundant columns
df = df.drop(columns=["Total Nacional"])

# Drop redundant rows 
df = df[df["Provincias"].notna()]
df = df[df["Provincias"] != "No residente"]

# Keep only monthly base data
df = df[df["Tipo de dato"] == "Dato base"]

# Extract year and month
df["year"] = df["Periodo"].str[:4].astype(int)
df["month"] = df["Periodo"].str[-2:].astype(int)

# Final structure: province x sex x age x year x month
print(df.head())
print(df["Provincias"].unique())

# Save
df.to_csv("mortality.csv", index=False)


# Keep only 2009–2019
df = df[(df["year"] >= 2009) & (df["year"] <= 2019)]

# Rename columns
df = df.rename(columns={"Total": "Deaths"})

# Drop cols
df = df.drop(columns=["Tipo de dato"])

# Mapping from mortality to weather province names
prov_map = {
    "02 Albacete": "ALBACETE",
    "03 Alicante/Alacant": "ALICANTE",
    "04 Almería": "ALMERIA",
    "01 Araba/Álava": "ARABA/ALAVA",
    "33 Asturias": "ASTURIAS",
    "05 Ávila": "AVILA",
    "06 Badajoz": "BADAJOZ",
    "07 Balears, Illes": "ILLES BALEARS",
    "08 Barcelona": "BARCELONA",
    "48 Bizkaia": "BIZKAIA",
    "09 Burgos": "BURGOS",
    "10 Cáceres": "CACERES",
    "11 Cádiz": "CADIZ",
    "39 Cantabria": "CANTABRIA",
    "12 Castellón/Castelló": "CASTELLON",
    "13 Ciudad Real": "CIUDAD REAL",
    "14 Córdoba": "CORDOBA",
    "15 Coruña, A": "A CORUÑA",
    "16 Cuenca": "CUENCA",
    "20 Gipuzkoa": "GIPUZKOA",
    "17 Girona": "GIRONA",
    "18 Granada": "GRANADA",
    "19 Guadalajara": "GUADALAJARA",
    "21 Huelva": "HUELVA",
    "22 Huesca": "HUESCA",
    "23 Jaén": "JAEN",
    "24 León": "LEON",
    "25 Lleida": "LLEIDA",
    "27 Lugo": "LUGO",
    "28 Madrid": "MADRID",
    "29 Málaga": "MALAGA",
    "30 Murcia": "MURCIA",
    "31 Navarra": "NAVARRA",
    "32 Ourense": "OURENSE",
    "34 Palencia": "PALENCIA",
    "35 Palmas, Las": "LAS PALMAS",
    "36 Pontevedra": "PONTEVEDRA",
    "26 Rioja, La": "LA RIOJA",
    "37 Salamanca": "SALAMANCA",
    "38 Santa Cruz de Tenerife": "SANTA CRUZ DE TENERIFE",
    "40 Segovia": "SEGOVIA",
    "41 Sevilla": "SEVILLA",
    "42 Soria": "SORIA",
    "43 Tarragona": "TARRAGONA",
    "44 Teruel": "TERUEL",
    "45 Toledo": "TOLEDO",
    "46 Valencia/València": "VALENCIA",
    "47 Valladolid": "VALLADOLID",
    "49 Zamora": "ZAMORA",
    "50 Zaragoza": "ZARAGOZA",
    "51 Ceuta": "CEUTA",
    "52 Melilla": "MELILLA"
}

# Apply mapping
df["Provincias"] = df["Provincias"].map(prov_map)

df.to_csv("mortality2.csv", index=False)

'''
<class 'pandas.core.frame.DataFrame'>
Index: 432432 entries, 65 to 645371
Data columns (total 7 columns):
 #   Column                      Non-Null Count   Dtype 
---  ------                      --------------   ----- 
 0   Provincias                  432432 non-null  object
 1   Sexo                        432432 non-null  object
 2   Edad (grupos quinquenales)  432432 non-null  object
 3   Periodo                     432432 non-null  object
 4   Deaths                      432432 non-null  object
 5   year                        432432 non-null  int64 
 6   month                       432432 non-null  int64 
dtypes: int64(2), object(5)
'''

# =============================================================================
# Cleaning Deaths column (mortality numbers)
# =============================================================================

import pandas as pd
import numpy as np

df = pd.read_csv("mortality2.csv")

# Peek at raw values of Deaths
print(df["Deaths"].head(20).tolist())

#more:
suspicious = df[df["Deaths"].str.len() > 3]["Deaths"].unique()
print(suspicious[:50])  


#Only keep rows that are numeric looking with . or , inside
suspicious_rows = df[df["Deaths"].str.match(r"^\d+[.,]\d+$")]
print(suspicious_rows.head(30))


# Find any values that contain a comma
comma_values = df[df["Deaths"].str.contains(",", na=False)]["Deaths"].unique()
print(comma_values[:50])

'''
[]
'''


df["Deaths"] = df["Deaths"].replace(["..", ""], np.nan)        # replace missing indicators
df["Deaths"] = df["Deaths"].str.strip()                        # remove extra spaces
df["Deaths"] = df["Deaths"].str.replace(".", "", regex=False)  # remove thousands separator
df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce")    # convert to numbers

print(df["Deaths"].describe())

# Save to CSV
df.to_csv("mortality3.csv", index=False)

'''
count    304754.000000
mean         58.077623
std         182.188136
min           1.000000
25%           3.000000
50%          12.000000
75%          44.000000
max        5757.000000
Name: Deaths, dtype: float64
'''


# Drop rows where Edad is "No consta"
df = df[df["Edad (grupos quinquenales)"] != "No consta"]

# =============================================================================
# Missing Values
# =============================================================================

missing_percent = df["Deaths"].isna().mean() * 100
print(f"Percentage of missing Deaths: {missing_percent:.2f}%")

'''
Percentage of missing Deaths: 26.00%
'''

df["Deaths"].isna().sum()

'''
107090
'''


import pandas as pd
import numpy as np

# date
df["Periodo"] = df["Periodo"].str.replace("M", "-")
df["Periodo"] = pd.PeriodIndex(df["Periodo"], freq="M")

df["Periodo"] = pd.to_datetime(df["Periodo"], format="%Y-%m")

print(df["Periodo"].dtype)


# Summarize missing deaths by province
missing_by_province = df[df["Deaths"].isna()].groupby("Provincias").size().sort_values(ascending=False)
print("Missing Deaths by province:\n", missing_by_province)


# Summarize missing deaths by month (Periodo)
missing_by_month = df[df["Deaths"].isna()].groupby("Periodo").size().sort_values(ascending=False)
print("\nMissing Deaths by month:\n", missing_by_month)


# and : Total missing Deaths: 26.00%


# Create a table of missing Deaths by Province × Sex × Age
missing_detailed = df[df["Deaths"].isna()].groupby(
    ["Provincias", "Sexo", "Edad (grupos quinquenales)"]
).size().reset_index(name="MissingCount")

# Sort by highest missing counts first
missing_detailed = missing_detailed.sort_values(by="MissingCount", ascending=False)

print(missing_detailed)

missing_detailed.to_csv("missing_deaths_detailed.csv", index=False)

# =============================================================================
# Duplicates
# Standardization
# Outliers
# Inconsistency
# Matching names/values to weather dataset
# =============================================================================

# Shows number of duplicate rows
print(df.duplicated().sum())

'''
0 
'''

import numpy as np

# Outliers
Q1 = df["Deaths"].quantile(0.25)
Q3 = df["Deaths"].quantile(0.75)
IQR = Q3 - Q1

# Typical threshold for extreme high values
upper_limit = Q3 + 3 * IQR
extreme_outliers = df[df["Deaths"] > upper_limit]
print("Extreme numeric outliers:\n", extreme_outliers.head(20))

# Suspicious non-numeric entries--should be NaN after cleaning!
suspicious_entries = df[df["Deaths"].isna()]
print("Suspicious or missing entries:\n", suspicious_entries.head(20))

# Extreme numeric outliers
num_extreme = extreme_outliers.shape[0]
perc_extreme = num_extreme / len(df) * 100
print(f"Extreme numeric outliers: {num_extreme} rows ({perc_extreme:.2f}%)")

# Suspicious/missing entries
num_missing = suspicious_entries.shape[0]
perc_missing = num_missing / len(df) * 100
print(f"Suspicious/missing Deaths entries: {num_missing} rows ({perc_missing:.2f}%)")

'''
Extreme numeric outliers: 23401 rows (5.68%)
Suspicious/missing Deaths entries: 107090 rows (26.00%)
'''

# inconsistency
# Categorical columns
categorical_cols = ["Provincias", "Sexo", "Edad (grupos quinquenales)"]
for col in categorical_cols:
    print(f"Unique values in {col} (excluding NaNs):")
    print(df[col].dropna().unique())
    print("\n")

# Numeric columns
numeric_cols = ["Deaths"]
for col in numeric_cols:
    print(f"Extreme or suspicious values in {col}:")
    print(df.loc[df[col].notna() & (df[col] < 0), col])  # negative deaths



# Rename columns
df = df.rename(columns={
    'Periodo': 'year_month',
    'Provincias': 'Province',
    'Sexo': 'Sex',
    'Edad (grupos quinquenales)': 'Age'
})

sex_mapping = {
    'Total': 'Both sexes',
    'Hombres': 'Male',
    'Mujeres': 'Female'
}

# Rename values
age_mapping = {
    'Todas las edades': 'All ages',
    'De 0 a 4 años': '0-4',
    'De 5 a 9 años': '5-9',
    'De 10 a 14 años': '10-14',
    'De 15 a 19 años': '15-19',
    'De 20 a 24 años': '20-24',
    'De 25 a 29 años': '25-29',
    'De 30 a 34 años': '30-34',
    'De 35 a 39 años': '35-39',
    'De 40 a 44 años': '40-44',
    'De 45 a 49 años': '45-49',
    'De 50 a 54 años': '50-54',
    'De 55 a 59 años': '55-59',
    'De 60 a 64 años': '60-64',
    'De 65 a 69 años': '65-69',
    'De 70 a 74 años': '70-74',
    'De 75 a 79 años': '75-79',
    'De 80 a 84 años': '80-84',
    'De 85 a 89 años': '85-89',
    '90 y más años': '90+'
}


df['Age'] = df['Age'].replace(age_mapping)
df['Sex'] = df['Sex'].replace(sex_mapping)



# Save to CSV
df.to_csv("mortality7.csv", index=False)
