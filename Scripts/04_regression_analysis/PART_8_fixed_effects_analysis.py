# =============================================================================
# PART 8
# ECONOMETRIC REGRESSION ANALYSIS
# TWO-WAY FIXED EFFECTS
# =============================================================================


# =============================================================================
# MAIN RESULT
# I conducted many different analysis with different statistical methods, different variables and interaction terms, 
# but I am only showing the main outcome here.
# =============================================================================


import pandas as pd

df = pd.read_csv("merged_monthly_weat_mortrate_.csv")

print(df.info())

# Using an updated dataset (calculated more heat thresholds and added more columns)

import pandas as pd

df = pd.read_csv("merged_AC_mort.csv")


# Filter the rows that will be used in the analysis (The total population, (no age- and sex- breakdowns yet)).

df_tota = df[
    (df["Sex"] == "Both sexes") &
    (df["Age"] == "All ages") &
    (df["year_month"] >= "2017-01-01") &
    (df["year_month"] <= "2019-12-01")
].copy()



# Scaling the independent variable (due to analytic details)
df_tota['Tmax95th_p10'] = df_tota['Tmax95th'] * 10


import statsmodels.formula.api as smf

fml = """
MortRate_per100k ~ Tmax95th_p10 + RHmean + prec + WindMean + C(Province) + C(year_month)
"""

m = smf.ols(fml, data=df_tota).fit(
    cov_type="cluster",
    cov_kwds={"groups": df_tota["Province"]}
)

print(m.summary())

# Result: 1.72***, good result, it aligns with the hypothesis (extreme heat increases mortality).


# Save df_tota with scaling
df_tota.to_csv("df_tota_WITH_SCALING_COLS.csv", index=False)
