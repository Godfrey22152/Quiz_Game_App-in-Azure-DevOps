# Use an official Python runtime as a parent image
FROM python:3.11.9-alpine3.19

# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MONGO_URI="mongodb+srv://odo:odoH22152@quiz-app.ve3naro.mongodb.net/?retryWrites=true&w=majority&appName=quiz-app"

# Set the working directory to /app
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install MongoDB client tools
RUN apk add --no-cache mongodb-tools

# Copy the application code into the container at /app
COPY app.py /app/app.py
COPY .env /app/.env
COPY static /app/static
COPY templates /app/templates

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
