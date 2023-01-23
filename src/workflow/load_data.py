import csv
import pandas



# Downloaded manually from:
# https://stats.oecd.org/index.aspx?queryid=104676
ALL_MORTALITY_PATH = "/data/HEALTH_MORTALITY_ALL.csv"
COVID_MORTALITY_PATH = "/data/HEALTH_MORTALITY_COVID.csv"
EXCESS_MORTALITY_PATH = "/data/HEALTH_MORTALITY_EXCESS.csv"



def _query_predicate(row, key):
    return  row["VARIABLE"] == key and \
            row["AGE"] == "TOTAL" and \
            row["GENDER"] == "TOTAL"


def load_all_df(filepath):
    covid_df = pandas.DataFrame()

    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if _query_predicate(row, "ALLCAUNB"):
                covid_df = covid_df.append(
                    {
                        "country": row["COUNTRY"],
                        "year": int(row["YEAR"]),
                        "week": int(row["WEEK"]),
                        "all_deaths": float(row["Value"]),
                    }, ignore_index=True
                )
   
    return covid_df

def load_covid_df(filepath):
    covid_df = pandas.DataFrame()

    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if _query_predicate(row, "COVIDNB"):
                covid_df = covid_df.append(
                    {
                        "country": row["COUNTRY"],
                        "year": int(row["YEAR"]),
                        "week": int(row["WEEK"]),
                        "covid_deaths": float(row["Value"]),
                    }, ignore_index=True
                )
   
    return covid_df

def load_excess_df(filepath):
    excess_df = pandas.DataFrame()

    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if _query_predicate(row, "EXCESSNB"):
                excess_df = excess_df.append(
                    {
                        "country": row["COUNTRY"],
                        "year": int(row["YEAR"]),
                        "week": int(row["WEEK"]),
                        "excess_deaths": float(row["Value"]),
                    }, ignore_index=True
                )

    return excess_df


def fuse_mortality_df(all_df, covid_df, excess_df):
    joint_df = pandas.merge(excess_df, covid_df, on=["country", "year", "week"])
    joint_df = pandas.merge(all_df, joint_df, on=["country", "year", "week"])
    joint_df.sort_values(by=["country", "year", "week"], inplace=True)
    return joint_df



def run():
    all_df = load_all_df(ALL_MORTALITY_PATH)
    covid_df = load_covid_df(COVID_MORTALITY_PATH)
    excess_df = load_excess_df(EXCESS_MORTALITY_PATH)


    joint_df = fuse_mortality_df(all_df, covid_df, excess_df)
    return joint_df
