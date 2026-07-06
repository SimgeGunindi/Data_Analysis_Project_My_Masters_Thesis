# =============================================================================
# PART 10
# Making 2 MAPS
# =============================================================================


# =============================================================================
# MAP 1: A province-level map of Spain, showing the number of weather stations in each province
# =============================================================================


# =============================================================================
# Making a clean stations list with relevant information
# =============================================================================

import pandas as pd

df = pd.read_excel("stations_list.xlsx")

df_dailystat = pd.read_csv("verA_sorted_by_comunidad_2.csv")

# drop columns
df_newstat = df.drop(columns=["nombre","indsinop"])

# rename
df_newstat = df_newstat.rename(columns={
    "provincia": "Province",
    "indicativo": "Station ID",
    "altitud": "Altitude",
    "latitud": "Latitude",
    "longitud": "Longitude"
})


# extract 2 columns from the previously cleaned dataset
prov_table = (
    df_dailystat[["provincia", "indicativo"]]
    .drop_duplicates()
    .sort_values(["provincia", "indicativo"])
)

prov_table

# lets match them

prov_list = sorted(prov_table["provincia"].unique())
prov_list


main_prov_list = sorted(df_newstat["Province"].unique())
main_prov_list


# matching names
prov_fix = {
    "BALEARES": "ILLES BALEARS",
    "STA. CRUZ DE TENERIFE": "SANTA CRUZ DE TENERIFE"
}

df_newstat["Province"] = df_newstat["Province"].replace(prov_fix)


sorted(df_newstat["Province"].unique())


# sort rows & cols

df_newstat = df_newstat[
    ["Province", "Station ID", "Latitude", "Longitude", "Altitude"]
]


df_newstat = df_newstat.sort_values(
    by="Province",
    ascending=True
).reset_index(drop=True)


df_newstat.head()
df_newstat["Province"].unique()


# save 
df_newstat.to_csv("APPX_STAT_LIST.csv", index=False)


# =============================================================================
# I need to convert the location coordinates in the dataset to decimal degrees,
# to be able to use the coordinates in the data
# "degrees, minutes, seconds (DMS) to decimal degrees (dd)"
# =============================================================================


def dms_to_dd(dms):
    """
    Convert DMS string, like '425234N' to decimal degrees
    Longitude may have 'W' (negative)
    """
    dms = str(dms).strip()
    if not dms:
        return None

    deg = int(dms[0:2])
    minutes = int(dms[2:4])
    sec = int(dms[4:6])
    direction = dms[-1]

    dd = deg + minutes/60 + sec/3600
    if direction in ['S','W']:
        dd *= -1
    return dd

# Example:
dms_to_dd("425234N")  # becomes 42.8761
dms_to_dd("0021234W") #  -2.3594

# and apply all

df_newstat["lat_dd"] = df_newstat["Latitude"].apply(dms_to_dd)
df_newstat["lon_dd"] = df_newstat["Longitude"].apply(dms_to_dd)


# =============================================================================
# I got the Shapefiles from Eurostat GISCO (geojson)
# Extracting Spain data from it and cleaning the file
# =============================================================================


import geopandas as gpd

# Read the file
gdf_nuts3 = gpd.read_file("Spain_NUTS3.geojson")

# Filter for Spain only
spain_prov = gdf_nuts3[gdf_nuts3["CNTR_CODE"] == "ES"].copy()

print(spain_prov[["NUTS_ID", "NAME_LATN", "CNTR_CODE"]])



# Map islands to their provinces
island_map = {
    "Tenerife": "Santa Cruz de Tenerife",
    "El Hierro": "Santa Cruz de Tenerife",
    "La Palma": "Santa Cruz de Tenerife",
    "La Gomera": "Santa Cruz de Tenerife",
    "Gran Canaria": "Las Palmas",
    "Fuerteventura": "Las Palmas",
    "Lanzarote": "Las Palmas",
    "Mallorca": "Illes Balears",
    "Menorca": "Illes Balears",
    "Eivissa y Formentera": "Illes Balears"
}

spain_prov["NAME_LATN"] = spain_prov["NAME_LATN"].replace(island_map)

# Drop duplicates to get 52 provinces
spain_prov_52 = spain_prov.drop_duplicates(subset="NAME_LATN").copy()



print(spain_prov_52[["NUTS_ID", "NAME_LATN", "CNTR_CODE"]])


# Mapping old NAME_LATN to my correct province names
prov_mapping = {
    "A Coruña": "A CORUÑA",
    "Albacete": "ALBACETE",
    "Alicante/Alacant": "ALICANTE",
    "Almería": "ALMERIA",
    "Araba/Álava": "ARABA/ALAVA",
    "Asturias": "ASTURIAS",
    "Ávila": "AVILA",
    "Badajoz": "BADAJOZ",
    "Barcelona": "BARCELONA",
    "Bizkaia": "BIZKAIA",
    "Burgos": "BURGOS",
    "Cáceres": "CACERES",
    "Cádiz": "CADIZ",  
    "Cantabria": "CANTABRIA",
    "Castellón/Castelló": "CASTELLON",
    "Ceuta": "CEUTA",
    "Ciudad Real": "CIUDAD REAL",
    "Córdoba": "CORDOBA",
    "Cuenca": "CUENCA",
    "Gipuzkoa": "GIPUZKOA",
    "Girona": "GIRONA",
    "Granada": "GRANADA",
    "Guadalajara": "GUADALAJARA",
    "Huelva": "HUELVA",
    "Huesca": "HUESCA",
    "Illes Balears": "ILLES BALEARS",
    "Jaén": "JAEN",
    "La Rioja": "LA RIOJA",
    "Las Palmas": "LAS PALMAS",
    "León": "LEON",
    "Lleida": "LLEIDA",
    "Lugo": "LUGO",
    "Madrid": "MADRID",
    "Málaga": "MALAGA",
    "Melilla": "MELILLA",
    "Murcia": "MURCIA",
    "Navarra": "NAVARRA",
    "Ourense": "OURENSE",
    "Palencia": "PALENCIA",
    "Pontevedra": "PONTEVEDRA",
    "Salamanca": "SALAMANCA",
    "Santa Cruz de Tenerife": "SANTA CRUZ DE TENERIFE",
    "Segovia": "SEGOVIA",
    "Sevilla": "SEVILLA",
    "Soria": "SORIA",
    "Tarragona": "TARRAGONA",
    "Teruel": "TERUEL",
    "Toledo": "TOLEDO",
    "Valencia/València": "VALENCIA",
    "Valladolid": "VALLADOLID",
    "Zamora": "ZAMORA",
    "Zaragoza": "ZARAGOZA"
}

# Apply mapping
spain_prov_52["prov_correct"] = spain_prov_52["NAME_LATN"].replace(prov_mapping)

# Check
print(spain_prov_52[["NAME_LATN", "prov_correct"]])



#drop cols
spain_prov_52 = spain_prov_52.drop(columns=["n_stations_x","n_stations_y","n_stations","Province","Province_x","Province_y"])


# =============================================================================
# Plotting the map
# =============================================================================


import geopandas as gpd
import matplotlib.pyplot as plt

# Stations -> GeoDataFrame

gdf_stations = gpd.GeoDataFrame(
    df_newstat,
    geometry=gpd.points_from_xy(df_newstat["lon_dd"], df_newstat["lat_dd"]),
    crs="EPSG:4326"
)

# Count stations per province

station_counts = (
    df_newstat
    .groupby("Province")
    .size()
    .reset_index(name="n_stations")
)

spain_prov_52 = spain_prov_52.merge(
    station_counts,
    left_on="prov_correct",
    right_on="Province",
    how="left"
)

spain_prov_52["n_stations"] = spain_prov_52["n_stations"].fillna(0)

# Plot

fig, ax = plt.subplots(figsize=(14, 16))

# Provinces shaded by station count
spain_prov_52.plot(
    ax=ax,
    column="n_stations",
    cmap="Oranges",
    edgecolor="black",
    linewidth=0.5,
    legend=True,
    legend_kwds={
        "label": "Number of stations",
        "shrink": 0.6,    
        "aspect": 25,    
        "pad": 0.02
    }
)

# Station points (smaller dots)
gdf_stations.plot(
    ax=ax,
    color="blue",
    markersize=8,
    zorder=3
)

# Province labels
for _, row in spain_prov_52.iterrows():
    ax.text(
        row.geometry.centroid.x,
        row.geometry.centroid.y,
        row["prov_correct"],
        fontsize=8,
        fontweight="bold",
        ha="center",
        va="center"
    )

# Formatting
ax.set_axis_off()
ax.set_title("AEMET Stations across Spanish Provinces", fontsize=16)

# Reduce empty margins so map fills the page
plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

# Save figures

fig.savefig("spain_mapstat_7.png", dpi=300, bbox_inches="tight")
fig.savefig("spain_mapstat_7.pdf", dpi=300, bbox_inches="tight")

plt.show()




# I wanna add number of stations in each province to the APPX_STAT_LIST

# Count stations per province
station_counts = (
    df_newstat
    .groupby("Province")
    .size()
    .rename("n_stations")
)

# Add province-level count to each station row
df_newstat["n_stations"] = df_newstat["Province"].map(station_counts)

# Check
df_newstat[["Province", "n_stations"]].head()




# =============================================================================
# # MAP 2: Average monthly mortality rate by province, 2017–2019
# =============================================================================



# =============================================================================
# Calculations
# =============================================================================

import pandas as pd

df = pd.read_csv("df_tota_WITH_SCALING_COLS.csv")


# Calculate:
# Mean mortality rate per province (across months)
prov_mort_mean = (
    df
    .groupby("Province", as_index=False)["MortRate_per100k"]
    .mean()
)

# Round for presentation:
prov_mort_mean["MortRate_per100k"] = prov_mort_mean["MortRate_per100k"].round(2)


# =============================================================================
# Plotting the map
# =============================================================================


# Start the map

spain_prov_52 = spain_prov_52.merge(
    prov_mort_mean,
    left_on="prov_correct",
    right_on="Province",
    how="left"
)

# Drop duplicate column
spain_prov_52 = spain_prov_52.drop(columns=["Province"])



import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 14))

# Provinces shaded by average mortality rate (orange scale)
spain_prov_52.plot(
    ax=ax,
    column="MortRate_per100k",
    cmap="Oranges",           
    edgecolor="black",
    linewidth=0.5,
    legend=True,
    legend_kwds={
        "label": "Mean monthly mortality rate (per 100,000)",
        "shrink": 0.6,
        "aspect": 25
    }
)

# Add numeric mortality values on provinces
for _, row in spain_prov_52.iterrows():
    ax.text(
        row.geometry.centroid.x,
        row.geometry.centroid.y,
        f"{row['MortRate_per100k']:.1f}",
        fontsize=8,
        ha="center",
        va="center",
        color="black"
    )

ax.set_axis_off()
ax.set_title(
    "Average Monthly Mortality Rate by Province (2017–2019)",
    fontsize=15
)

plt.tight_layout()


# Save
fig.savefig("prov_meanmort2.png", dpi=300, bbox_inches="tight")
fig.savefig("prov_meanmort2.pdf", dpi=300, bbox_inches="tight")

plt.show()

