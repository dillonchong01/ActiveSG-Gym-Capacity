import os
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

DB_PATH = Path("database/gym_capacity.db")
CLEANED_DB_PATH = Path("database/gym_capacity_cleaned.db")
OUTPUT_JSON_PATH = Path("static/gym_capacity_summary.json")

def summarize_capacity():
    """
    Summarizes gym capacity using only the last 6 months of data
    Deduplicates repeated timings by averaging capacities and saves into gym_capacity_cleaned.db
    Saves the summarized data into gym_capacity_summary.json
    """

    # Connect to raw data SQLite database
    conn = sqlite3.connect(DB_PATH)

    # Load raw data
    query = "SELECT gym_name, capacity, date, time, day, is_weekend FROM gym_capacity;"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return

    # Use only last 6 months of data
    df["date"] = pd.to_datetime(df["date"])
    cutoff_date = datetime.now() - timedelta(days=180)
    df = df[df["date"] >= cutoff_date]
    if df.empty:
        return

    # Deduplicate Timings in Same Day by Averaging Capacities
    df_cleaned = df.groupby(["gym_name", "date", "time", "day", "is_weekend"])["capacity"].mean().reset_index()

    # Build Cleaned Database
    if CLEANED_DB_PATH.exists():
        os.remove(CLEANED_DB_PATH)  # Delete old DB

    CLEANED_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_conn = sqlite3.connect(CLEANED_DB_PATH)
    cur = clean_conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS gym_capacity (
        id INTEGER PRIMARY KEY,
        gym_name TEXT,
        capacity INTEGER,
        date DATE,
        time TIME,
        day TEXT,
        UNIQUE(gym_name, date, time)
    )
    """)

    cur.executemany("""
    INSERT OR IGNORE INTO gym_capacity
    (gym_name, capacity, date, time, day)
    VALUES (?, ?, ?, ?, ?)
    """, df_cleaned.assign(
        date=lambda x: x["date"].dt.strftime("%Y-%m-%d")
    )[["gym_name", "capacity", "date", "time", "day"]].values.tolist())

    clean_conn.commit()
    clean_conn.close()


    # Build JSON structure, Grouping by is_weekend and Averaging Capacities
    df_summary = df_cleaned.groupby(["gym_name", "time", "is_weekend"])["capacity"].mean().reset_index()
    df_summary["time"] = df_summary["time"].apply(
        lambda t: datetime.strptime(t, "%H:%M").strftime("%H:%M:%S")
    )
    
    summary_dict = {}
    for gym_name, group in df_summary.groupby("gym_name"):
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
    summarize_capacity()