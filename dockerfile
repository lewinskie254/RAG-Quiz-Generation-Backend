FROM python:3.11-slim 

# Prevent Python from writing .pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
# Remove langchain-textsplitters from requirements.txt if present
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Django port
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
