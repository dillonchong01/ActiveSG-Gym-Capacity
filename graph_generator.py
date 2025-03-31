import re
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from datetime import datetime
import os

def generate_graphs():
    os.makedirs("static/graphs", exist_ok=True)

    # Connect to local SQLite database
    conn = sqlite3.connect("database/gym_capacity.db")

    # Load raw data
    query = "SELECT gym_name, capacity, date, time FROM gym_capacity;"
    df = pd.read_sql(query, conn)

    # Group by gym_name and time and obtain average capacity
    df_grouped = df.groupby(["gym_name", "time"])["capacity"].mean().reset_index()
    df_grouped["gym_name"] = df_grouped["gym_name"].apply(lambda x: re.sub(r'\b(ActiveSG|Gym)\b|@', '', x).strip())
    df_grouped["time"] = df_grouped["time"].apply(lambda t: datetime.strptime(t, "%H:%M"))

    # Define x-axis labels
    desired_ticks = [datetime.strptime(f"{hour:02d}:00", "%H:%M") for hour in range(7, 23)]
    desired_tick_labels = [dt.strftime("%H:%M") for dt in desired_ticks]

    for gym in df_grouped["gym_name"].unique():
        gym_data = df_grouped[df_grouped["gym_name"] == gym]

        plt.figure(figsize=(8, 5))
        plt.plot(gym_data["time"], gym_data["capacity"], marker="o", linestyle="-")
        plt.xlabel("Time of Day")
        plt.ylabel("Average Capacity")
        plt.title(f"Gym Capacity - {gym}")
        plt.xticks(ticks=desired_ticks, labels=desired_tick_labels, rotation=45)
        plt.grid(True)
        plt.tight_layout()

        # Save graph as an image
        filename = re.sub(r'[^\w\-_. ]', '_', gym).replace(' ', '_')
        plt.savefig(f"static/graphs/{filename}.png")
        plt.close()
