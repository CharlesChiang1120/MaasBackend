# Use the official Python image from the Docker Hub
FROM python:3.9.7

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY app/ /app

# Install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
