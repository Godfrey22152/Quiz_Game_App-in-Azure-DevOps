# Quiz Game Web Application

This is a Dockerized web application for a quiz game, consisting of a Flask web server, MongoDB database, and a MongoDB Express interface for database management.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/quiz-game-web-app.git

## Navigate to the project directory:
cd quiz-game-web-app

## Build and run the Docker containers:
docker-compose up --build
Access the web application in your browser at http://localhost:5000.

## Docker Containers
web: The Flask web server for the quiz game application.
mongo: MongoDB database container.
mongo-express: MongoDB Express interface for managing the database.

## Configuration
MongoDB port: 27018 (mapped to host port 27018)
Web server port: 5000 (mapped to host port 5000)
MongoDB Express port: 8081 (mapped to host port 8081)

## Directory Structure
app.py: Flask application code containing the routes and logic for the quiz game.
Dockerfile: Dockerfile for building the Flask application container.
mongodb.Dockerfile: Dockerfile for building the MongoDB container.
docker-compose.yml: Docker Compose configuration file defining services for the web server, MongoDB, and MongoDB Express.
entrypoint.sh: Shell script executed during container startup to run MongoDB in the background and import data into the database.
requirements.txt: List of Python dependencies for the Flask application.
static/: Directory containing static files such as CSS and JavaScript.
templates/: Directory containing HTML templates for the web application.

## Usage
Users can create accounts, login, select quiz categories, play quizzes, and view quiz results.
The Flask application interacts with the MongoDB database to store user accounts, quiz data, and quiz results.
MongoDB Express provides a web interface for managing the MongoDB database.

## License
This project is licensed under the MIT License.


