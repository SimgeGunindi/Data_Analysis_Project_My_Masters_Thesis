# =============================================================================
# PART 4
# POPULATION DATA FROM NATIONAL STATISTICS INSTITUTE OF SPAIN (INE)
# Includes: year-province-age-sex-number of population
# =============================================================================


# =============================================================================
# Cleaning the population dataset
# =============================================================================

# =============================================================================
# Cleaning basics
# =============================================================================

import pandas as pd

df = pd.read_csv("03002.csv", sep=";") 

# If Year is currently string, convert to int
df['Periodo'] = df['Periodo'].astype(int)

# Convert to datetime
df['Periodo'] = pd.to_datetime(df['Periodo'], format='%Y')

# Check
print(df['Periodo'].head())


print(df.head())
print(df.columns)

'''
     Provincias Edad (grupos quinquenales)  ...    Periodo       Total
0  TOTAL ESPAÑA               TOTAL EDADES  ... 2022-01-01  47.475.420
1  TOTAL ESPAÑA               TOTAL EDADES  ... 2021-01-01  47.385.107
2  TOTAL ESPAÑA               TOTAL EDADES  ... 2020-01-01  47.450.795
3  TOTAL ESPAÑA               TOTAL EDADES  ... 2019-01-01  47.026.208
4  TOTAL ESPAÑA               TOTAL EDADES  ... 2018-01-01  46.722.980

[5 rows x 6 columns]
Index(['Provincias', 'Edad (grupos quinquenales)', 'Españoles/Extranjeros',
       'Sexo', 'Periodo', 'Total'],
      dtype='object')
'''


# Define the range as datetime
start = pd.to_datetime('1998', format='%Y')
end = pd.to_datetime('2008', format='%Y')

# Filter out unwanted rows
df_clean = df[~(
    df['Españoles/Extranjeros'].isin(['Españoles', 'Extranjeros']) |
    df['Periodo'].between(start, end)
)]

# =============================================================================
# Standardization
# =============================================================================

# Rename columns
df_clean = df_clean.rename(columns={
    'Periodo': 'Year',
    'Total': 'Population',
    'Provincias': 'Province',
    'Sexo': 'Sex',
    'Edad (grupos quinquenales)': 'Age'
})

# Rename values
age_mapping = {
    'TOTAL EDADES': 'All ages',
    '0-4 años': '0-4',
    '5-9 años': '5-9',
    '10-14 años': '10-14',
    '15-19 años': '15-19',
    '20-24 años': '20-24',
    '25-29 años': '25-29',
    '30-34 años': '30-34',
    '35-39 años': '35-39',
    '40-44 años': '40-44',
    '45-49 años': '45-49',
    '50-54 años': '50-54',
    '55-59 años': '55-59',
    '60-64 años': '60-64',
    '65-69 años': '65-69',
    '70-74 años': '70-74',
    '75-79 años': '75-79',
    '80-84 años': '80-84',
    '85-89 años': '85-89',
    '90-94 años': '90-94',
    '95-99 años': '95-99',
    '100 años y más': '100+'
}

sex_mapping = {
    'Ambos sexos': 'Both sexes',
    'Hombres': 'Male',
    'Mujeres': 'Female'
}

df_clean['Age'] = df_clean['Age'].replace(age_mapping)
df_clean['Sex'] = df_clean['Sex'].replace(sex_mapping)


#Save 
df_clean.to_csv("pop2.csv", index=False, sep=',', encoding='utf-8')


# Remove dots and commas, then convert to integer
df_clean['Population'] = df_clean['Population'].astype(str)  # ensure it's string
df_clean['Population'] = df_clean['Population'].str.replace('.', '', regex=False)  # remove dots
df_clean['Population'] = df_clean['Population'].str.replace(',', '', regex=False)  # remove commas
df_clean['Population'] = df_clean['Population'].astype(int)  # convert to integer


print(df_clean["Province"].unique())


# Mapping 
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
df_clean["Province"] = df_clean["Province"].map(prov_map)


# Drop the column
df_clean = df_clean.drop(columns=['Españoles/Extranjeros'])

# Drop rows where Province == 'TOTAL ESPAÑA'
df_clean = df_clean[df_clean['Province'] != 'TOTAL ESPAÑA']


# Map ages 90-94, 95-99, 100+ to 90+
df_clean['Age'] = df_clean['Age'].replace({
    '90-94': '90+',
    '95-99': '90+',
    '100+': '90+'
})


# Aggregate Population by Province, Year, Sex, and Age (if needed)
df_clean = df_clean.groupby(['Province', 'Year', 'Sex', 'Age'], as_index=False)['Population'].sum()


#Save 
df_clean.to_csv("pop3.csv", index=False, sep=',', encoding='utf-8')

# =============================================================================
# Missing
# Duplicates
# Inconsistency
# Uniqueness
# =============================================================================

# Check missing values per column
print(df_clean.isna().sum())

# Or percentage of missing values
print(df_clean.isna().mean() * 100)

'''
Province    0
Year        0
Sex         0
Age         0
Population      0
dtype: int64
'''

# Check total duplicate rows
print(df_clean.duplicated().sum())

'''0'''

# Basic stats
print(df_clean['Population'].describe())


#Flag unusually high or low values
# For example, Population greater than 3 standard deviations from mean
mean = df_clean['Population'].mean()
std = df_clean['Population'].std()
outliers = df_clean[(df_clean['Population'] > mean + 3*std) | (df_clean['Population'] < 0)]
print(outliers)


# Check unique values
for col in ['Province', 'Sex', 'Age']:
    print(f"{col} unique values:\n", df_clean[col].unique(), "\n")

# suspicious values
for col in ['Province', 'Sex', 'Age']:
    print(df_clean[col].value_counts())



print(df_clean.dtypes)
'''
Province    object
Year        object
Sex         object
Age         object
Population       int64
dtype: object
'''


# Check for negative values
print(df_clean[df_clean['Population'] < 0])

'''
Empty DataFrame
Columns: [Province, Year, Sex, Age, Population]
Index: []
'''


# Check for extremely high values
q_low = df_clean['Population'].quantile(0.01)
q_high = df_clean['Population'].quantile(0.99)
print(df_clean[(df_clean['Population'] < q_low) | (df_clean['Population'] > q_high)])
