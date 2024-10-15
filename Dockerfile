# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose any ports that your app runs on, if applicable (for Flask, FastAPI, etc.)
# EXPOSE 5000  # Uncomment this if your bot serves a web interface or API

# Set environment variables
# Ensure the app uses the .env file in the project
COPY .env .env

# Command to run your bot when the container starts
CMD ["python", "bot.py"]
