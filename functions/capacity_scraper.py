import re
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

DB_PATH = Path("database/gym_capacity.db")

def scrape():
    """
    Scrapes Gym Capacity from the ActiveSG Website

    Returns:
        list: A list of gym capacity data containing gym-capacity pairs
    """
    # Initialize the WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://activesg.gov.sg/gym-capacity"
    try:
        driver.get(url)
        WebDriverWait(driver, 45).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chakra-card.css-m97yjq")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        update_text = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.chakra-text.css-12346zh"))).text
        
        # Extract Date/Time from Webpage
        match = re.search(r"Last updated at (\d{1,2} \w+ \d{4}),\s*([\d: ]+(?:AM|PM|am|pm)?)", update_text)
        if match:
            # Get Date
            date_str = match.group(1)
            date_str = datetime.strptime(date_str, "%d %B %Y").date()

            # Get Time, rounded down to nearest 30min
            time_str = match.group(2)
            dt = datetime.strptime(time_str, "%I:%M %p")
            rounded_minute = round(dt.minute / 30) * 30
            if rounded_minute == 60:
                dt = dt.replace(minute=0, second=0) + timedelta(hours=1)
            else:
                dt = dt.replace(minute=rounded_minute, second=0)
            time_str = dt.strftime('%H:%M')

        else:
            return 0

        # Extract Capacity for each Gym
        data = []
        gym_capacity = soup.find_all('div', class_='chakra-card css-m97yjq')
        for element in gym_capacity:
            # If Gym Name not found, continue
            if element.select_one('.chakra-text'):
                gym_name = element.select_one('.chakra-text').get_text(strip=True)
                gym_name = re.sub(r'(?i)\b(activesg|gym)\b|@', '', gym_name).strip()
            else:
                continue

            # If Capacity not found, continue
            if element.select_one('.chakra-badge'):
                capacity_text = element.select_one('.chakra-badge').get_text(strip=True)
            else:
                continue

            # If Capacity is 0 or Closed, continue
            if capacity_text == 'Closed':
                continue
            capacity_percentage = int(''.join(filter(str.isdigit, capacity_text)))
            if capacity_percentage == 0:
                continue

            # Add Boolean for Weekend
            is_weekend = date_str.weekday() >= 5
            day = date_str.strftime("%A")
            data.append([gym_name, capacity_percentage, date_str, time_str, day, is_weekend])

    finally:
        driver.quit()

    return data

def save_data_to_db(data):
    """
    Saves gym capacity data into a SQLite datase

    Args:
    data (list): The list of gym capacity records to be stored
    """
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gym_capacity (
                id INTEGER PRIMARY KEY,
                gym_name TEXT,
                capacity INTEGER,
                date DATE,
                time TIME,
                day TEXT,
                is_weekend BOOLEAN,
                UNIQUE(gym_name, date, time)
            )
        ''')

        # Insert data while avoiding duplicates
        cursor.executemany('''
            INSERT OR IGNORE INTO gym_capacity (gym_name, capacity, date, time, day, is_weekend) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        
        # Commit changes to the database
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()
    
if __name__ == "__main__":
    data = scrape()
    if data:
        save_data_to_db(data)


