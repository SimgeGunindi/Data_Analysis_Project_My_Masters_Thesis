# =============================================================================
# PART 9
# FURTHER REGRESSION ANALYSIS (DETAILED)
# HETEROGENEITY (AGE & SEX BREAKDOWNS)
# =============================================================================


# =============================================================================
# I have to make broader age groups for heterogeneity analysis (instead of using 5-year age groups)
# =============================================================================


import pandas as pd

df = pd.read_csv("merged_AC_mort.csv")

df.columns.tolist()



# Copy the dataset
df_new1 = df.copy()


# Create broad age groups

def recode_age_broad(age):
    if age == "All ages":
        return "All ages"
    elif age in ["0-4","5-9","10-14"]:
        return "0-14"
    elif age in ["15-19","20-24","25-29","30-34","35-39","40-44",
                 "45-49","50-54","55-59","60-64"]:
        return "15-64"
    else:
        return "65+"

df_new1["Age_group_broad"] = df_new1["Age"].apply(recode_age_broad)


# NEED TO DROP
cols_to_drop = ["mort_rate", "MortRate_per100k", "MortRate_per1000"]
df_new1 = df_new1.drop(columns=cols_to_drop, errors="ignore")


# Build aggregation dictionary

sum_vars = ["Deaths", "Population"]   # only these two SUM

# everything else numeric should be MEAN
exclude_cols = [
    "Province", "Sex", "Age", "Age_group_broad",
    "year", "month", "year_month"
] + sum_vars

all_other_numeric = [
    c for c in df_new1.columns
    if c not in exclude_cols and df_new1[c].dtype != "object"
]

agg = {}

# sums
for v in sum_vars:
    agg[v] = "sum"

# means
for v in all_other_numeric:
    agg[v] = "mean"


# Group the dataset

df_broad = df_new1.groupby(
    ["Province", "Sex", "year", "month", "year_month", "Age_group_broad"],
    as_index=False
).agg(agg)


# Recalculate mortality rates

df_broad["mort_rate"] = df_broad["Deaths"] / df_broad["Population"]
df_broad["MortRate_per100k"] = df_broad["mort_rate"] * 100000
df_broad["MortRate_per1000"] = df_broad["mort_rate"] * 1000


# Save
df_broad.to_csv("df_broad.csv", index=False)


# =============================================================================
# Another age category (more detailed)
# =============================================================================


# Copy the dataset
df_new2 = df.copy()


def recode_age_detailed(age):
    if age == "All ages":
        return "All ages"
    elif age in ["0-4","5-9","10-14"]:
        return "0-14"
    elif age in ["15-19","20-24","25-29","30-34","35-39","40-44",
                 "45-49","50-54","55-59","60-64"]:
        return "15-64"
    elif age in ["65-69","70-74"]:
        return "65-74"
    elif age in ["75-79","80-84"]:
        return "75-84"
    elif age in ["85-89","90+"]:
        return "85+"

df_new2["Age_group_detailed"] = df_new2["Age"].apply(recode_age_detailed)


# NEED TO DROP
cols_to_drop = ["mort_rate", "MortRate_per100k", "MortRate_per1000"]
df_new2 = df_new2.drop(columns=cols_to_drop, errors="ignore")


# Build aggregation dictionary

sum_vars = ["Deaths", "Population"]   # only these two SUM

# everything else numeric should be MEAN
exclude_cols = [
    "Province", "Sex", "Age", "Age_group_detailed",
    "year", "month", "year_month"
] + sum_vars

all_other_numeric = [
    c for c in df_new2.columns
    if c not in exclude_cols and df_new2[c].dtype != "object"
]

agg = {}

# sums
for v in sum_vars:
    agg[v] = "sum"

# means
for v in all_other_numeric:
    agg[v] = "mean"


# Group the dataset

df_detailed = df_new2.groupby(
    ["Province", "Sex", "year", "month", "year_month", "Age_group_detailed"],
    as_index=False
).agg(agg)


# Recalculate mortality rates

df_detailed["mort_rate"] = df_detailed["Deaths"] / df_detailed["Population"]
df_detailed["MortRate_per100k"] = df_detailed["mort_rate"] * 100000
df_detailed["MortRate_per1000"] = df_detailed["mort_rate"] * 1000


# Save
df_detailed.to_csv("df_detailed.csv", index=False)


# =============================================================================
# Scaling the variables again (needed for the analysis)
# =============================================================================

 
# List of all datasets
datasets = [df, df_broad, df_detailed]

for dataset in datasets:
    # Select columns ending with 'th'
    threshold_cols = [col for col in dataset.columns if col.endswith("th")]
    
    # Multiply each by 10, and create new columns with "_p10" suffix
    for col in threshold_cols:
        dataset[col + "_p10"] = dataset[col] * 10

# Drop month ones (extras)
for dataset in [df, df_broad, df_detailed]:
    for col in ["year_month_p10", "month_p10"]:
        if col in dataset.columns:
            dataset.drop(columns=col, inplace=True)


# Save

df.to_csv("df_SCALED-5agegroups.csv", index=False)
df_broad.to_csv("df_broad_SCALED.csv", index=False)
df_detailed.to_csv("df_detailed_SCALED.csv", index=False)



# =============================================================================
# Heterogeneity Analysis:
# =============================================================================



import pandas as pd
from statsmodels.formula.api import ols

# Remove deaths having "0" (needed for the regression analysis)

df = df[df["Deaths"] > 0].copy()
df_broad = df_broad[df_broad["Deaths"] > 0].copy()
df_detailed = df_detailed[df_detailed["Deaths"] > 0].copy()


# SUBSETS

subsets = {
    "Male": df[(df["Sex"] == "Male") &
               (df["Age"] == "All ages") &
               (df["year_month"] >= "2017-01-01") &
               (df["year_month"] <= "2019-12-01")].copy(),

    "Female": df[(df["Sex"] == "Female") &
                 (df["Age"] == "All ages") &
                 (df["year_month"] >= "2017-01-01") &
                 (df["year_month"] <= "2019-12-01")].copy(),

    "0-14": df_broad[(df_broad["Age_group_broad"] == "0-14") &
                     (df_broad["Sex"] == "Both sexes") &
                     (df_broad["year_month"] >= "2017-01-01") &
                     (df_broad["year_month"] <= "2019-12-01")].copy(),

    "15-64": df_broad[(df_broad["Age_group_broad"] == "15-64") &
                      (df_broad["Sex"] == "Both sexes") &
                      (df_broad["year_month"] >= "2017-01-01") &
                      (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65+": df_broad[(df_broad["Age_group_broad"] == "65+") &
                    (df_broad["Sex"] == "Both sexes") &
                    (df_broad["year_month"] >= "2017-01-01") &
                    (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65-74": df_detailed[(df_detailed["Age_group_detailed"] == "65-74") &
                         (df_detailed["Sex"] == "Both sexes") &
                          (df_detailed["year_month"] >= "2017-01-01") &
                          (df_detailed["year_month"] <= "2019-12-01")].copy(),

    "75-84": df_detailed[(df_detailed["Age_group_detailed"] == "75-84") &
                         (df_detailed["Sex"] == "Both sexes") &
                          (df_detailed["year_month"] >= "2017-01-01") &
                          (df_detailed["year_month"] <= "2019-12-01")].copy(),

    "85+": df_detailed[(df_detailed["Age_group_detailed"] == "85+") &
                       (df_detailed["Sex"] == "Both sexes") &
                        (df_detailed["year_month"] >= "2017-01-01") &
                        (df_detailed["year_month"] <= "2019-12-01")].copy(),

    "65+ Female": df_broad[(df_broad["Age_group_broad"] == "65+") &
                           (df_broad["Sex"] == "Female") &
                           (df_broad["year_month"] >= "2017-01-01") &
                           (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65+ Male": df_broad[(df_broad["Age_group_broad"] == "65+") &
                         (df_broad["Sex"] == "Male") &
                         (df_broad["year_month"] >= "2017-01-01") &
                         (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65+ Humidity": df_broad[(df_broad["Age_group_broad"] == "65+") &
                             (df_broad["Sex"] == "Both sexes") &
                             (df_broad["year_month"] >= "2017-01-01") &
                             (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65+ Female Humidity": df_broad[(df_broad["Age_group_broad"] == "65+") &
                                    (df_broad["Sex"] == "Female") &
                                    (df_broad["year_month"] >= "2017-01-01") &
                                    (df_broad["year_month"] <= "2019-12-01")].copy(),

    "65+ Male Humidity": df_broad[(df_broad["Age_group_broad"] == "65+") &
                                  (df_broad["Sex"] == "Male") &
                                  (df_broad["year_month"] >= "2017-01-01") &
                                  (df_broad["year_month"] <= "2019-12-01")].copy()
}


# FORMULAS

formulas = {
    "Formula1": "MortRate_per100k ~ Tmax95th_p10 + RHmean + prec + WindMean + C(Province) + C(year_month)",
    "Formula2": "MortRate_per100k ~ Tmax95th_p10 * RHmean95th_p10 + prec + WindMean + C(Province) + C(year_month)",
    "Formula3": "MortRate_per100k ~ Tmax90th_p10 * RHmean95th_p10 + prec + WindMean + C(Province) + C(year_month)"
}

coeffs_map = {
    "Formula1": "Tmax95th_p10",
    "Formula2": "Tmax95th_p10:RHmean95th_p10",
    "Formula3": "Tmax90th_p10:RHmean95th_p10"
}


# FORMATTER (for the p-values)

def format_coef(coef, se, pval):
    star = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
    return f"{coef:.3f}{star}\\\\\n({se:.3f})"


# RESULT + N TABLES

results = pd.DataFrame(index=subsets.keys(), columns=formulas.keys())
Ns = pd.DataFrame(index=subsets.keys(), columns=formulas.keys())


# RUN MODELS

for name, data in subsets.items():

    if "Humidity" in name:
        for f in ["Formula2", "Formula3"]:
            model = ols(formulas[f], data=data).fit(
                cov_type="cluster",
                cov_kwds={"groups": data["Province"]}
            )
            coef = coeffs_map[f]
            results.at[name, f] = format_coef(
                model.params.get(coef, 0),
                model.bse.get(coef, 0),
                model.pvalues.get(coef, 1)
            )
            Ns.at[name, f] = int(model.nobs)

        results.at[name, "Formula1"] = ""
        Ns.at[name, "Formula1"] = ""

    else:
        model = ols(formulas["Formula1"], data=data).fit(
            cov_type="cluster",
            cov_kwds={"groups": data["Province"]}
        )
        coef = coeffs_map["Formula1"]
        results.at[name, "Formula1"] = format_coef(
            model.params.get(coef, 0),
            model.bse.get(coef, 0),
            model.pvalues.get(coef, 1)
        )
        Ns.at[name, "Formula1"] = int(model.nobs)
        results.at[name, "Formula2"] = ""
        results.at[name, "Formula3"] = ""
        Ns.at[name, "Formula2"] = ""
        Ns.at[name, "Formula3"] = ""


# OUTPUT

print("COEFFICIENTS")
print(results)

print("\n OBSERVATIONS (N)")
print(Ns)


# LATEX OUTPUT (for getting the results table with academic thesis style on LaTeX)

latex_code = results.to_latex(
    escape=False,
    column_format='lccc',
    caption="Regression Results with Clustered SEs",
    label="tab:reg_results"
)

print(latex_code)

