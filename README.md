# 🏋️ ActiveSG Gym Capacity Tracker

A web application providing insights into gym occupancy trends across ActiveSG gyms in Singapore. Plan your gym visits efficiently by exploring historical capacity trends.  

---

## ⚙️ How It Works

🤖 **Automated Data Collection**  
Capacity data is automatically scraped every 15 minutes from the [ActiveSG Gym & Pool Crowd](https://activesg.gov.sg/gym-pool-crowd) website using **Selenium** and **BeautifulSoup**, with workflows scheduled via **GitHub Actions**.  The information is then stored in a **SQLite** database for historical tracking

**📊 Trend Visualization**  
The frontend (HTML, CSS, and JavaScript) displays historical average occupancy trends, helping users compare weekday and weekend patterns and make informed decisions.

---

## 🔗 Access the Web Interface

Check out the website @ [activesg-capacity.vercel.app](https://activesg-capacity.vercel.app)

---

## 📬 Contact

For questions, feedback, or access to the database, reach out to me at: **dillonchong01@gmail.com**

---