FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install flask

# Expose the service port
EXPOSE 5003

# Run the application
CMD ["python", "app.py"]
