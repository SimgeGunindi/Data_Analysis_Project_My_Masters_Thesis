# =============================================================================
# PART 7
# MERGING MORTALITY AND WEATHER DATA (PROVINCE-MONTH LEVEL)
# =============================================================================


# =============================================================================
# Controliing the datasets before merging
# =============================================================================


import pandas as pd

df_weat = pd.read_csv("prov_month_PRECSUM_weather.csv")

print(df_weat.info())

print(df_weat.columns)


rename_dict = {
    'provincia': 'Province',
    'tmax': 'Tmax',
    'tmed': 'Tmean',
    'tmin': 'Tmin',
    'velmedia': 'WindMean',
    'racha': 'WindGustMax',
    'hrMedia': 'Hmean',
    'hrMax': 'Hmax',
    'hrMin': 'Hmin',

    # Threshold values (not used in analysis)
    'tmax_90th': 'Tmax_thr90',
    'tmax_95th': 'Tmax_thr95',
    'tmed_90th': 'Tmean_thr90',
    'tmed_95th': 'Tmean_thr95',

    # Threshold flags
    'tmax90_flag': 'Tmax90th',
    'tmax95_flag': 'Tmax95th',
    'tmed90_flag': 'Tmean90th',
    'tmed95_flag': 'Tmean95th',

    # 2+ and 3+ day threshold exceedances
    'tmax95_flag_2plus': 'Tmax95th2plus',
    'tmax95_flag_3plus': 'Tmax95th3plus',
    'tmax90_flag_2plus': 'Tmax90th2plus',
    'tmax90_flag_3plus': 'Tmax90th3plus',
    'tmed95_flag_2plus': 'Tmean95th2plus',
    'tmed95_flag_3plus': 'Tmean95th3plus',
    'tmed90_flag_2plus': 'Tmean90th2plus',
    'tmed90_flag_3plus': 'Tmean90th3plus',

    # Deciles (reference bin)
    'tmax_decile': 'Tmax_ref_decile',
    'tmed_decile': 'Tmean_ref_decile',
    'hr_decile': 'Hmean_ref_decile',

    # Decile flags (D1...D10)
    # Tmax
    'tmax_decile_1_flag': 'Tmax_D1',
    'tmax_decile_2_flag': 'Tmax_D2',
    'tmax_decile_3_flag': 'Tmax_D3',
    'tmax_decile_4_flag': 'Tmax_D4',
    'tmax_decile_5_flag': 'Tmax_D5',
    'tmax_decile_6_flag': 'Tmax_D6',
    'tmax_decile_7_flag': 'Tmax_D7',
    'tmax_decile_8_flag': 'Tmax_D8',
    'tmax_decile_9_flag': 'Tmax_D9',
    'tmax_decile_10_flag': 'Tmax_D10',

    # Tmean
    'tmed_decile_1_flag': 'Tmean_D1',
    'tmed_decile_2_flag': 'Tmean_D2',
    'tmed_decile_3_flag': 'Tmean_D3',
    'tmed_decile_4_flag': 'Tmean_D4',
    'tmed_decile_5_flag': 'Tmean_D5',
    'tmed_decile_6_flag': 'Tmean_D6',
    'tmed_decile_7_flag': 'Tmean_D7',
    'tmed_decile_8_flag': 'Tmean_D8',
    'tmed_decile_9_flag': 'Tmean_D9',
    'tmed_decile_10_flag': 'Tmean_D10',

    # Humidity decile flags
    'hr_decile_1_flag': 'Hmean_D1',
    'hr_decile_2_flag': 'Hmean_D2',
    'hr_decile_3_flag': 'Hmean_D3',
    'hr_decile_4_flag': 'Hmean_D4',
    'hr_decile_5_flag': 'Hmean_D5',
    'hr_decile_6_flag': 'Hmean_D6',
    'hr_decile_7_flag': 'Hmean_D7',
    'hr_decile_8_flag': 'Hmean_D8',
    'hr_decile_9_flag': 'Hmean_D9',
    'hr_decile_10_flag': 'Hmean_D10',
}

df_weat = df_weat.rename(columns=rename_dict)



for p in sorted(df_weat['Province'].unique()):
    print(p)


# Checking mortality data


import pandas as pd

df_mort = pd.read_csv("pop-mort-withMORTRATE-merged.csv")


print(df_mort.info())


for p in sorted(df_mort['Province'].unique()):
    print(p)


set(df_mort['Province']).difference(df_weat['Province'])


df_mort['year_month'] = pd.to_datetime(df_mort['year_month']).dt.to_period('M').dt.to_timestamp()

df_weat['year_month'] = pd.to_datetime(df_weat['year_month'], format='%Y-%m')


print(df_mort['year_month'].dtype)
print(df_weat['year_month'].dtype)

# =============================================================================
# Merging
# =============================================================================

df_merged = df_mort.merge(
    df_weat,
    on=['Province', 'year_month'],
    how='left'
)


# Save
df_weat.to_csv("weat_monthlyprov_final.csv", index=False)
df_mort.to_csv("MortRate_final.csv", index=False)
df_merged.to_csv("merged_monthly_weat_mortrate_.csv", index=False)
