# Use an official Python image as the base
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install required dependencies (e.g., Chrome and ChromeDriver)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    || apt-get -f install -y

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Install Python dependencies (Selenium, BeautifulSoup4, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . .

# Default command to run the scraper
CMD ["python", ".github/scrape.py"]
