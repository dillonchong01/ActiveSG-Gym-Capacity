FROM selenium/standalone-chrome:latest

# Install any other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Run the scraper
CMD ["python", ".github/scrape.py"]
