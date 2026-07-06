# =============================================================================
# PART 5
# MERGING MORTALITY AND POPULATION DATA 
# =============================================================================


# =============================================================================
# Checking both datasets before merging
# =============================================================================


import pandas as pd

df_mort = pd.read_csv("mortality7.csv")

df_pop = pd.read_csv("pop4.csv")


print(df_mort.dtypes)

print(df_pop.dtypes)

'''
print(df_mort.dtypes)
Province       object
Sex            object
Age            object
year_month     object
Deaths        float64
year            int64
month           int64
dtype: object

print(df_pop.dtypes)
Province      object
Year          object
Sex           object
Age           object
Population     int64
dtype: object
'''


df_pop['year'] = df_pop['Year'].dt.year

print(df_pop.dtypes)

'''
Province              object
Year          datetime64[ns]
Sex                   object
Age                   object
Population             int64
year                   int32
dtype: object
'''

# =============================================================================
# Merging
# =============================================================================


df_merged = df_mort.merge(
    df_pop[['Province', 'Sex', 'Age', 'year', 'Population']],
    on=['Province', 'Sex', 'Age', 'year'],
    how='left'
)


df_pop.to_csv("pop5.csv", index=False)
df_merged.to_csv("pop-mort-OHNEMORTRATE-merged.csv", index=False)



# =============================================================================
# Calculating the "Mortality Rate",
# the outcome of the analysis will be "mortality rate per 100.000 inhabitants",
# (to standardize the populations of different locations and to conduct the analysis accurately)
# =============================================================================


df_merged['mort_rate'] = df_merged['Deaths'] / df_merged['Population']

#This calculates the raw proportion: fraction of people who died in that month
#The values will be very small, like 0.05% for monthly mortality


df_merged['MortRate_per100k'] = df_merged['Deaths'] / df_merged['Population'] * 100000

#Now a value of 50 means 50 deaths per 100,000 population in that month.


df_merged['MortRate_per1000'] = df_merged['Deaths'] / df_merged['Population'] * 1000



# check missing
cols = ['Deaths', 'Population', 'MortRate_per100k']
print(df_merged[cols].isna().sum())
'''
Deaths              107090
Population               0
MortRate_per100k    107090
dtype: int64
'''


df_merged.to_csv("pop-mort-withMORTRATE-merged.csv", index=False)


# =============================================================================
# Checking the dataset after merging
# =============================================================================

import pandas as pd

df_merged = pd.read_csv("pop-mort-withMORTRATE-merged.csv")


print(df_merged.info())


print(df_merged.describe())


cols = ['Deaths', 'Population', 'MortRate_per100k']
print(df_merged[cols].describe())


'''
print(df_merged.info())
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 411840 entries, 0 to 411839
Data columns (total 11 columns):
 #   Column            Non-Null Count   Dtype  
---  ------            --------------   -----  
 0   Province          411840 non-null  object 
 1   Sex               411840 non-null  object 
 2   Age               411840 non-null  object 
 3   year_month        411840 non-null  object 
 4   Deaths            304750 non-null  float64
 5   year              411840 non-null  int64  
 6   month             411840 non-null  int64  
 7   Population        411840 non-null  int64  
 8   mort_rate         304750 non-null  float64
 9   MortRate_per100k  304750 non-null  float64
 10  MortRate_per1000  304750 non-null  float64
dtypes: float64(4), int64(3), object(4)
memory usage: 34.6+ MB
None



print(df_merged.describe())
              Deaths           year  ...  MortRate_per100k  MortRate_per1000
count  304750.000000  411840.000000  ...     304750.000000     304750.000000
mean       58.078372    2014.000000  ...        258.998519          2.589985
std       182.189215       3.162281  ...        493.339719          4.933397
min         1.000000    2009.000000  ...          0.280596          0.002806
25%         3.000000    2011.000000  ...         11.114198          0.111142
50%        12.000000    2014.000000  ...         54.101565          0.541016
75%        44.000000    2017.000000  ...        211.097408          2.110974
max      5757.000000    2019.000000  ...       9230.769231         92.307692

[8 rows x 7 columns]



cols = ['Deaths', 'Population', 'MortRate_per100k']
print(df_merged[cols].describe())
              Deaths    Population  MortRate_per100k
count  304750.000000  4.118400e+05     304750.000000
mean       58.078372  6.009633e+04        258.998519
std       182.189215  2.303880e+05        493.339719
min         1.000000  5.900000e+01          0.280596
25%         3.000000  8.266500e+03         11.114198
50%        12.000000  1.898900e+04         54.101565
75%        44.000000  4.083925e+04        211.097408
max      5757.000000  6.663394e+06       9230.769231
'''
