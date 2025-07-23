import pandas as pd
import requests

# PREPROCESSING PROCEDURES
def fetch_and_clean_data():
    # Fetch data from API
    url = "https://api.data.gov.my/data-catalogue?id=population_malaysia"
    df = pd.read_json(url)

    # Filter data for 2020 onwards
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"] >= pd.to_datetime("2020-01-01")]

    # Check for missing values
    print("\nMissing values per column:")
    print(df.isna().sum())

    # Check for duplicates
    print(f"\nNumber of duplicated rows: {df.duplicated().sum()}")

    # Show unique values
    print("\nUnique values:")
    print("Age:", df["age"].unique())
    print("Sex:", df["sex"].unique())
    print("Date (sample):", df["date"].dt.year.unique())
    print("Ethnicity:", df["ethnicity"].unique())

    # statistical overview
    print("\nData overview:")
    print(df.describe(include="all"))
    
    return df


# SUMMARY PROCESSING
def get_summaries(df):
    # Yearly total
    total_by_year = (
        df[df["age"] == "overall"]
        .groupby(df["date"].dt.year)["population"]
        .sum()
        .astype(str)
        .to_dict()
    )

    # Convert datetime index to string in summaries as jsonify only accepts certain data types
    def convert_keys_to_str(d):
        return {str(k): v for k, v in d.items()}

    # Gender summary
    gender_summary = (
        df[df["age"] == "overall"]
        .groupby(["date", "sex"])["population"]
        .sum()
        .unstack()
        .fillna(0)
        .astype(int)
        .to_dict()
    )
    gender_summary = {k: convert_keys_to_str(v) for k, v in gender_summary.items()}

    # Age group summary
    age_summary = (
        df[df["sex"] == "both"]
        .groupby(["date", "age"])["population"]
        .sum()
        .unstack()
        .fillna(0)
        .astype(int)
        .to_dict()
    )
    age_summary = {k: convert_keys_to_str(v) for k, v in age_summary.items()}

    # Ethnicity summary
    ethnicity_summary = (
        df[df["age"] == "overall"]
        .groupby(["date", "ethnicity"])["population"]
        .sum()
        .unstack()
        .fillna(0)
        .astype(int)
        .to_dict()
    )
    ethnicity_summary = {k: convert_keys_to_str(v) for k, v in ethnicity_summary.items()}

    return {
        "total_population_per_year": total_by_year,
        "gender_summary": gender_summary,
        "age_group_summary": age_summary,
        "ethnicity_summary": ethnicity_summary,
    }
