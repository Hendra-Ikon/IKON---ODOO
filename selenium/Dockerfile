# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set environment variables to prevent prompts and errors during the installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    gnupg2 \
    ca-certificates \
    && apt-get clean

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Download ChromeDriver and install it
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Set display to avoid any X11 errors during the execution
ENV DISPLAY=:99

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./scripts /app

# Install the necessary Python packages
RUN pip install --no-cache-dir undetected-chromedriver selenium flask

# Expose the port if needed (for communication, e.g., Flask)
EXPOSE 5000

RUN python --version
RUN chmod +x /app/main.py

# Command to run the Python script when the container launches
CMD python main.py