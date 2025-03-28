# Start from a base image with Python
FROM python:3.10-slim

# Install necessary dependencies including wget, curl, and lsb-release
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    lsb-release \
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

# Add Google Chrome's official repository and install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && DISTRO=$(lsb_release -c | awk '{print $2}') \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ $DISTRO main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean

# Install ChromeDriver (you may need to update the version of chromedriver)
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
