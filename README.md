# ActiveSG Gym Capacity Tracking Application

A web application that provides insights into gym occupancy trends for ActiveSG gyms across Singapore. Users can view historical capacity trends to plan visits efficiently.

---

## Features

- **Historical Gym Capacity Trends:**  
  Displays **average gym occupancy trends over the past three months**, helping users identify the best times to visit each gym.

- **Automated Data Collection:**  
  Gym capacity data is automatically scraped at regular intervals using **Selenium** and **BeautifulSoup**, with workflows scheduled every **15 minutes** via **GitHub Actions**.

- **Interactive Web Interface:**  
  Users can explore capacity trends for different gyms through a clean and intuitive web interface built with **HTML** and **CSS**. Separate views are available for **weekdays** and **weekends**.

- **Comprehensive Coverage:**  
  Includes multiple ActiveSG gyms across Singapore, giving users a broad view of trends island-wide.

---

## How It Works

1. **Data Collection:**  
   Selenium navigates the ActiveSG gym booking pages and extracts capacity data, which is stored in a **SQLite database** to maintain a historical record.

2. **Automation:**  
   GitHub Actions triggers the scraping workflow every 15 minutes, continuously building a **three-month dataset** of gym occupancy.

3. **Trend Visualization:**  
   The frontend aggregates historical data from the SQLite database to display **average occupancy trends**. Users can easily compare weekday and weekend patterns to make informed decisions about when to visit.

---

## Access the Web Interface

The application is publicly available at: [**activesg-capacity.vercel.app**](https://activesg-capacity.vercel.app)

---

## Technology Stack

- **Data Extraction:** Python (Selenium, BeautifulSoup)
- **Automation:** GitHub Actions  
- **Frontend:** HTML, CSS  
- **Database:** SQLite (stores historical gym occupancy data)  

---

## Contact

For questions, feedback, or access to the gym capacity database results, please reach out to me at **dillonchong01@gmail.com**.
