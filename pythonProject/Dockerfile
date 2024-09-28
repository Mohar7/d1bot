# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents (your local files) into the container at /app
COPY .. /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for debugging purposes if needed (optional)
EXPOSE 8080

# Command to run your bot (make sure bot.py exists in the same directory)
CMD ["python", "bot.py"]
