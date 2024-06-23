# Use an official Python runtime as a parent image
FROM python:3.11.9-alpine3.19

# Set the working directory to /app
WORKDIR /app

# Copy and install dependencies 
COPY requirements.txt requirements.txt

# Install dependencies and MongoDB client tools 
RUN pip install --no-cache-dir -r requirements.txt \
    && apk add --no-cache mongodb-tools 
    
# Copy the application code into the container at /app
COPY app.py /app/app.py
COPY .env /app/.env
COPY static /app/static
COPY templates /app/templates

# Make port 5000 available to the world outside this container    
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]

