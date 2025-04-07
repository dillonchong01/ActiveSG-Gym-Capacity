import re
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = Path("database/gym_capacity.db")
SUMMARY_DB_PATH = Path("database/gym_capacity_summary.db")

def summarize_capacity():
    # Connect to local SQLite database
    conn = sqlite3.connect(DB_PATH)

    # Load raw data
    query = "SELECT gym_name, capacity, date, time, is_weekend FROM gym_capacity;"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
      return

    # Group by gym_name and time and obtain average capacity
    df_grouped = df.groupby(["gym_name", "time", "is_weekend"])["capacity"].mean().reset_index()
    df_grouped["gym_name"] = df_grouped["gym_name"].apply(lambda x: re.sub(r'\b(ActiveSG|Gym)\b|@', '', x).strip())
    df_grouped["time"] = df_grouped["time"].apply(lambda t: datetime.strptime(t, "%H:%M").strftime("%H:%M"))

    # Save into summary database
    summary_conn = sqlite3.connect(SUMMARY_DB_PATH)
    df_grouped.to_sql("gym_capacity_summary", summary_conn, if_exists="replace", index=False)
    summary_conn.close()

if __name__ == "__main__":
    summarize_capacity()
  
