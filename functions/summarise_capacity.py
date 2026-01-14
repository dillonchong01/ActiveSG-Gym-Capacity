import re
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

DB_PATH = Path("database/gym_capacity.db")
OUTPUT_JSON_PATH = Path("static/gym_capacity_summary.json")

def summarize_capacity_to_json():
    """
    Summarizes gym capacity using only the last 3 months of data and saves it as JSON.
    """

    # Connect to raw data SQLite database
    conn = sqlite3.connect(DB_PATH)

    # Load raw data
    query = "SELECT gym_name, capacity, date, time, is_weekend FROM gym_capacity;"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return

    # Use only last 3 months of data
    df["date"] = pd.to_datetime(df["date"])
    cutoff_date = datetime.now() - timedelta(days=90)
    df = df[df["date"] >= cutoff_date]
    if df.empty:
        return

    # Group by gym_name, date, time, is_weekend and obtain average capacity
    df_grouped1 = df.groupby(["gym_name", "date", "time", "is_weekend"])["capacity"].mean().reset_index()
    df_grouped = df_grouped1.groupby(["gym_name", "time", "is_weekend"])["capacity"].mean().reset_index()

    # Clean gym names and format time
    df_grouped["gym_name"] = df_grouped["gym_name"].apply(
        lambda x: re.sub(r'\b(ActiveSG|Gym)\b|@', '', x).replace('  ', ' ').strip().replace(' ', '_')
    )
    df_grouped["time"] = df_grouped["time"].apply(lambda t: datetime.strptime(t, "%H:%M").strftime("%H:%M:%S"))

    # Build JSON structure
    summary_dict = {}
    for gym_name, group in df_grouped.groupby("gym_name"):
        summary_dict[gym_name] = {
            "weekday": [],
            "weekend": []
        }
        for _, row in group.iterrows():
            # Round capacity to nearest 1 decimal
            entry = {"time": row["time"], "capacity": round(float(row["capacity"]), 1)}
            if row["is_weekend"]:
                summary_dict[gym_name]["weekend"].append(entry)
            else:
                summary_dict[gym_name]["weekday"].append(entry)

    # Save to JSON
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(summary_dict, f, indent=4)

if __name__ == "__main__":
    summarize_capacity_to_json()