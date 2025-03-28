# Start from a base image with Python
FROM python:3.10-slim

# Install necessary dependencies including wget, curl, and lsb-release
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
    && apt-get clean

# Install Google Chrome via downloading the .deb package directly
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean

# Install ChromeDriver (you may need to update the version of chromedriver)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt file (this allows Docker to cache the dependencies)
COPY requirements.txt .

# Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (this step is after installing dependencies)
COPY . .

# Run the scraper script when the container starts
CMD ["python", ".github/scrape.py"]
