from flask import Flask, jsonify
from dash import Dash, html, dcc, Input, Output
import requests
import pandas as pd
import plotly.express as px

from data_handler import fetch_and_clean_data, get_summaries

# ======== FLASK SETUP ========
app = Flask(__name__)

@app.route('/population', methods=['GET'])
def population():
    df = fetch_and_clean_data()
    summaries = get_summaries(df)
    return jsonify(summaries)

# ======== DASH SETUP ==========
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

dash_app.layout = html.Div([
    html.H1("Malaysia Population Dashboard"),
    
    dcc.Dropdown(
        id="summary-type",
        options=[
            {"label": "Total Population Over Time", "value": "total"},
            {"label": "Gender Breakdown", "value": "gender"},
            {"label": "Age Group Comparison", "value": "age"},
            {"label": "Ethnicity Distribution", "value": "ethnicity"}
        ],
        value="total"
    ),
    
    dcc.Graph(id="summary-graph")
])

@dash_app.callback(
   Output("summary-graph", "figure"),
    Input("summary-type", "value")
)
def update_graph(summary_type):
    try:
        res = requests.get("http://localhost:5000/population")
        data = res.json()

        if summary_type == "total":
            year = list(data["total_population_per_year"].keys())
            population = [float(x) for x in data["total_population_per_year"].values()]
            return px.bar(x=year, y=population, labels={"x": "Year", "y": "Total Population"}, title="Total Population Over Time")

        elif summary_type == "gender":
            gender_dict = data["gender_summary"]
            df = pd.DataFrame(gender_dict)

            # convert string to datetime again
            df.index = pd.to_datetime(df.index)
            df["Year"] = df.index.year

            # Move Year to front
            df = df.reset_index(drop=True)
            df = df[["Year"] + [col for col in df.columns if col != "Year"]]

            return px.bar(df, x="Year", y=df.columns[1:], title="Gender Breakdown by Year", barmode="stack")


        elif summary_type == "age":
            age_dict = data["age_group_summary"]
            df = pd.DataFrame(age_dict)

            # convert string to datetime again
            df.index = pd.to_datetime(df.index)
            df["Year"] = df.index.year

            # Move Year to front
            df = df.reset_index(drop=True)
            df = df[["Year"] + [col for col in df.columns if col != "Year"]]

            return px.line(df, x="Year", y=df.columns[1:], title="Population by Age Group Over Time")


        elif summary_type == "ethnicity":
            # Ethnicity Summary - pie chart of latest year
            eth_dict = data["ethnicity_summary"]
            df = pd.DataFrame(eth_dict)
            df.index.name = "Date"
            df = df.reset_index()
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = df["Date"].dt.year
            latest_year = df["Year"].max()
            latest_df = df[df["Year"] == latest_year].drop(columns=["Date", "Year"])
            totals = latest_df.sum().reset_index()
            totals.columns = ["Ethnicity", "Population"]
            return px.pie(totals, names="Ethnicity", values="Population", title=f"Ethnicity Distribution ({latest_year})")

        return px.scatter(title="Invalid Selection")

    except Exception as e:
        return px.scatter(title=f"Error loading data: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)