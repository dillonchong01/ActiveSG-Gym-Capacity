# Start from a base image with Python and install necessary dependencies
FROM python:3.10-slim

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    libx11-dev \
    libxpm-dev \
    libpng-dev \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libatspi2.0-0 \
    libxrandr2 \
    libgbm-dev \
    libasound2 \
    libgtk-3-0 \
    google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper script into the container
COPY .github/scrape.py .

# Run the scraper script when the container starts
CMD ["python", "scrape.py"]
