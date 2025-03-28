# Start from a base image with Python
FROM python:3.10-slim

# Install necessary dependencies for running Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
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

# Install the latest stable Google Chrome version
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Set up the working directory in the container
WORKDIR /app

# Copy the scraper script into the container
COPY .github/scrape.py .

# Install Python dependencies
COPY requirements.txt .  # If you have any Python dependencies, this line will work.
RUN pip install --no-cache-dir -r requirements.txt

# Run the scraper script when the container starts
CMD ["python", "scrape.py"]
