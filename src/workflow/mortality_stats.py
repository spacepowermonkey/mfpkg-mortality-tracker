import math



def _compute_rel_harm(row):
    if row["covid_pct"] <= 0.0 and row["nce_pct"] <= 0.0:
        return 0
    if row["covid_pct"] <= 0.0:
        return -5
    if row["nce_pct"] <= 0.0:
        return 5
    return math.log2(row["covid_pct"] / row["nce_pct"])

def _compute_death_norm(df):
    df["enorm"] = df.apply(lambda row: abs(row["excess_deaths"]) / df["excess_deaths"].max(), axis=1)
    return df



def run(mortality_df):
    mortality_df = mortality_df.groupby(by="country").apply(
        _compute_death_norm
    )

    mortality_df["covid_pct"]   = mortality_df["covid_deaths"] / mortality_df["all_deaths"]
    mortality_df["n_covid"]     = mortality_df["covid_pct"]
    mortality_df["excess_pct"]  = mortality_df["excess_deaths"] / mortality_df["all_deaths"]
    mortality_df["n_excess"]    = mortality_df["excess_pct"]

    mortality_df["nce_pct"]     = mortality_df.apply(
        lambda row: max(row["excess_pct"] - row["covid_pct"], 0),
        axis=1
    )
    mortality_df["n_nce"]       = mortality_df["nce_pct"]

    mortality_df["rel_mortality"] = mortality_df.apply(_compute_rel_harm, axis=1)
    mortality_df["n_rel_mort"]  = mortality_df["enorm"] * mortality_df["rel_mortality"]
    return mortality_df
