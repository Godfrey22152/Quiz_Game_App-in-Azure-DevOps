# Quiz Game Web App Project
This project is a comprehensive Quiz Application designed to run in a Docker container and deployable to Azure Kubernetes Service (AKS) using Azure DevOps CI/CD pipelines. The application uses MongoDB for data storage and Flask as the web framework.

## Project Structure

The repository is organized into several directories and files, each serving a specific purpose in the project. Below is an overview of the project structure:

```sh
Quiz-Game-App/
├── Azure-CI-CD-Pipeline/
│ ├── Quiz-App-CI-Pipeline.yaml
| ├── README.md
│ ├── Self-Hosted-Agent/Vagrantfile
├── Monitoring_Setup/
│ ├── README.md
├── Manifest_files/
│ ├── app-deployment.yaml
├── static/
│ ├── styles.css files
├── templates/
│ ├── welcome.html
│ ├── create_account.html
│ ├── login.html
│ ├── variety.html
│ ├── dumps.html
│ ├── select_quiz.html
│ ├── play_quiz.html
│ ├── question.html
│ ├── results.html
| ├── etc
├── Tests/
│ ├── test_app.py
├── quiz-app/
│ ├── devOps_questions.json
│ ├── current_affairs_questions.json
│ ├── aws_questions.json
│ ├── azure_questions.json
| ├── etc
├── Dockerfile
├── requirements.txt
├── .env
├── app.py
├── README.md

### Directory and File Descriptions

- **Azure-CI-CD-Pipeline/**: Contains files related to the CI/CD pipeline setup using Azure DevOps.
  - **Quiz-App-CI-Pipeline.yaml**: YAML file for the CI pipeline configuration.
  - **Self-Hosted-Agent/Vagrantfile**: Configuration file for setting up a self-hosted agent using Vagrant.

- **Monitoring_Setup//**: Contains a detailed README.md file for setting up self-hosted Prometheus and Grafana to monitor the deployed application in the Azure Kubernetes Service (AKS) cluster. 
  - **README.md**: README.md file for setting up a Prometheus and Grafana to monitor the deployed application in the Azure Kubernetes Service (AKS) cluster. 

- **Manifest_files/**: Contains Kubernetes manifest files for deploying the application.
  - **app-deployment.yaml**: YAML file for deploying the app to a Kubernetes cluster.

- **static/**: Contains static files like CSS styles.
  - **styles.css files**: CSS files for styling the HTML templates.

- **templates/**: Contains HTML template files for the Flask application.
  - **welcome.html**: Template for the welcome page.
  - **create_account.html**: Template for the account creation page.
  - **login.html**: Template for the login page.
  - **variety.html**: Template for the variety page showing quiz categories.
  - **dumps.html**: Template for displaying quiz dumps.
  - **select_quiz.html**: Template for selecting a quiz.
  - **play_quiz.html**: Template for playing a quiz.
  - **question.html**: Template for displaying quiz questions.
  - **results.html**: Template for displaying quiz results.
  - **etc**: And other template files.

- **Tests/**: Contains test files for the project.
  - **test_app.py**: Security test file for the project.

- **quiz-app/**: Contains JSON files of the quiz questions used in the application.
  - **devOps_questions.json**: JSON file containing DevOps quiz questions.
  - **current_affairs_questions.json**: JSON file containing current affairs quiz questions.
  - **aws_questions.json**: JSON file containing AWS quiz questions.
  - **azure_questions.json**: JSON file containing Azure quiz questions.
  - **etc**: And other questions.

- **Dockerfile**: Dockerfile for building and running the application in a Docker container.

- **requirements.txt**: Text file listing the Python dependencies for the project.

- **.env**: Environment variables file for configuring the Flask application.

- **app.py**: Main Python file for the Flask application, containing routes and logic for the quiz functionality.
```
## Features

- Account Management Functionality: Users can create accounts, log in, and log out.
- Quizzes: Various categories of quizzes with multiple questions.
- Session Management: Custom session interface using MongoDB for session storage.
- Quiz results and performance tracking.
- Health check endpoints for readiness and liveness probes.
- Dockerized application for easy deployment.
- CI/CD pipeline setup using Azure DevOps.
- Kubernetes Deployment: Deployable to AKS using Kubernetes manifests.

## Getting Started

To get started with the project, follow these steps:

### Prerequisites

- Docker
- Python 
- MongoDB
- Vagrant (Used for self-hosted agent in azure)
- Kubernetes (Azure)
- Azure DevOps
-  Prometheus and Grafana 

### Setup

#### Step 1: Clone the repository:

   ```bash
   git clone https://github.com/Godfrey22152/quiz_game_app.git
   cd quiz_game_app
```
#### Step 2: Set up the environment variables:
Update your .env file in the root directory with your MongoDB cluster URL as required:

```sh
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/quiz_app?retryWrites=true&w=majority
```
#### Step 3: Build and run the application using Docker to check if .env Database URL is correct:
```sh
docker build -t quiz-app .
docker run -p 5000:5000 --env-file .env quiz-app
```
#### Step 4: Access the application:
Open your browser and navigate to `http://localhost:5000`.

## CI/CD Pipeline
The project includes a CI/CD pipeline setup using Azure DevOps. Follow these steps to set up the pipeline:

### 1. Configure Azure DevOps Pipeline and setup your CI pipeline:

- Navigate to the Azure-CI-CD-Pipeline/ directory.
- Find the README.md file in the directory, follow the directions in the README.md and configure your Quiz-App-CI-Pipeline.yaml and set up your release pipeline with your Azure DevOps project details.
- Run the CI pipeline in to build, test, and get your artifects ready for your release pipeline and deployment to Azure Kubernetes Service (AKS).

### 2. Set up Release Pipeline:
- Define stages and tasks to deploy the application to AKS as stated in the README.md file in the Azure-CI-CD-Pipeline/ directory.
- Use automatic triggers for continuous deployment.
- After successful deployment in the kubernetes cluster, go to ingress services and find the application ingress service external IP assigned to the application and access the application on the browser.

## Monitoring-Setup Directory:
Contains a detailed step-by-step README.md guide to help you through the process of setting up self-hosted Prometheus and Grafana to monitor your Azure Kubernetes Service (AKS) cluster.

### Prerequisites
1. Azure Kubernetes Service (AKS) cluster: Ensure you have an AKS cluster up and running.
2. Environment Setup:
- Local Machine:
Ensure you have kubectl and Helm installed on your local machine.
Your local machine should be configured to access your AKS cluster.
- Cloud Shell:
You can use Azure Cloud Shell, which has kubectl and Helm pre-installed and configured to access your Azure resources.
3. Follow the prompts in the README.md file to setup the monitoring tools.

