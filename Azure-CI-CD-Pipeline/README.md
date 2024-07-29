## Overview

This guide will help you set up a Continuous Integration (CI) and Continuous Deployment (CD) pipeline for the Quiz App using Azure DevOps. The CI pipeline will include steps for installing dependencies, running security scans, performing static code analysis, and running unit tests. The CD pipeline will automatically deploy the application to Azure Kubernetes Service (AKS) upon successful completion of the CI pipeline.

## Prerequisites

Before you begin, ensure you have the following:

1. An Azure DevOps account.
2. An Azure subscription with an AKS cluster.
3. A self-hosted agent pool in Azure DevOps.
4. Docker installed on the agent.
5. Access to Docker Hub for pushing images.

### Step 1. Set Up Azure DevOps Project

#### Create a New Project:
1. Go to Azure DevOps.
2. Create a new project for your Python application.

### Step 2. Set Up Repositories:
1. Create or import your Python application's repository.
2. Ensure the repository contains your application code, Dockerfile, Kubernetes   manifests, and any configuration files.

### Step 2. Set Up Self-Hosted Agent
#### Register Self-Hosted Agent:
Go to your Azure DevOps project.
Navigate to Project Settings -> Pipelines -> Agent pools.
Select the Default pool or create a new pool, then register your self-hosted agent.

## Setting Up the CI Pipeline

### Step 1: Create a New Pipeline (Quiz-App-CI-Pipeline.yaml)

1. Navigate to your Azure DevOps project.
2. Select **Pipelines** > **New Pipeline**.
3. Choose **Use the classic editor** for the configuration method.
4. Select your repository and the default branch.

### Step 2: Define the YAML Script

Copy the following YAML script into the editor. This script includes all necessary steps to install dependencies, perform security scans, run static code analysis, and execute unit tests.

```yaml
# Quiz-App-CI-Pipeline.yaml

pool:
  name: quiz-app-agent-pool

variables:
  pwd: $(System.DefaultWorkingDirectory)
  DOCKER_HUB_PAT: 'Your DOCKER_HUB_PAT '
  DOCKER_HUB_USER: 'your DOCKER_USERNAME'

steps:
- script: |
    # Install Python and pip
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip

    # Install Docker
    sudo apt-get remove docker docker-engine docker.io containerd runc
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Install Trivy
    wget https://github.com/aquasecurity/trivy/releases/download/v0.27.1/trivy_0.27.1_Linux-64bit.deb
    sudo dpkg -i trivy_0.27.1_Linux-64bit.deb

    # Install Bandit
    pip install bandit

    # Install Pytest and Pytest-cov
    pip install pytest pytest-cov
  displayName: 'Install Dependencies and Tools'

- script: |
    pip install -r requirements.txt
  displayName: 'Install Project Dependencies'

- script: 'trivy fs --format json -o $(Build.ArtifactStagingDirectory)/trivy-fs-report.json --scanners vuln,misconfig --severity HIGH,CRITICAL .'
  displayName: 'Trivy FS Scan'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Trivy FS Report'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/trivy-fs-report.json'
    ArtifactName: 'Trivy-fs-report'

- script: |
    bandit -ll -ii -r . -f json -o $(Build.ArtifactStagingDirectory)/bandit_report.json
  displayName: 'Static Code Analysis with Bandit'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Bandit Report'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/bandit_report.json'
    ArtifactName: 'Bandit-Scan-Report'

- script: |
    export PYTHONPATH=$(pwd)
    pytest --cov=app tests/ --junitxml=$(Build.ArtifactStagingDirectory)/pytest_report.xml --cov-report=xml:$(Build.ArtifactStagingDirectory)/coverage.xml
  displayName: 'Unit Testing and Coverage with Pytest & Pytest-cov'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Test Results'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/pytest_report.xml'
    ArtifactName: 'Pytest_Unit_Test-Report'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Code Coverage Results'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/coverage.xml'
    ArtifactName: 'Code_Coverage-Report'

- task: CopyFiles@2
  displayName: 'Copy Manifest Files to: $(build.artifactstagingdirectory)'
  inputs:
    SourceFolder: 'Manifest_Files'
    Contents: 'app-deployment.yaml'
    TargetFolder: '$(build.artifactstagingdirectory)'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Artifact: Manifest_File'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/app-deployment.yaml'
    ArtifactName: 'Manifest_File'

- task: Docker@2
  displayName: 'Docker build and push'
  inputs:
    containerRegistry: 'docker_con'
    repository: 'godfrey22152/quiz-game-app'
    tags: '3.0'

- script: |
    # Install Docker Scout CLI
    curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
    
    # Login to Docker Hub using environment variables
    echo $(DOCKER_HUB_PAT) | docker login -u $(DOCKER_HUB_USER) --password-stdin
    
    mkdir -p $(Build.ArtifactStagingDirectory)/Docker-Scout-Reports
    
    # Run Docker Scout quickview command
    docker scout quickview godfrey22152/quiz-game-app:3.0 > $(Build.ArtifactStagingDirectory)/Docker-Scout-Reports/quickview_scan_report.sarif.json
    
    # Run Docker Scout CVEs command
    docker scout cves godfrey22152/quiz-game-app:3.0 --format sarif --only-severity critical,high > $(Build.ArtifactStagingDirectory)/Docker-Scout-Reports/cves_scan_report.sarif.json
  displayName: 'Docker Image Scan with Docker Scout'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Docker Scout Image Reports'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/Docker-Scout-Reports'
    ArtifactName: 'Image-Scan-Reports'

```

### Step 3: Save and Run the Pipeline
1. Save the pipeline with a meaningful name, such as Quiz-App-CI-Pipeline.
2. Click Run to execute the pipeline.

## Setting Up the CD Pipeline (Quiz-App-CD-Release-Pipeline)

### Step 1: Create a New Release Pipeline
1. Navigate to Pipelines > Releases.
2. Click New pipeline.
3. Select Empty job.

### Step 2: Add an Artifact
1. Click Add an artifact.
2. Select your build pipeline (Quiz-App-CI-Pipeline).
3. Choose the latest version of the build.
3. Enable the Continuous deployment trigger.

### Step 3: Configure the Deployment Stage
1. Click on Stage 1 and rename it to Deploy to AKS.
2. Add a task by clicking the + icon.
3. Select Kubernetes from the list of tasks.

### Step 4: Configure Kubernetes Deployment
1. In the Kubernetes service connection field, select your existing Azure Kubernetes Service connection or create a new one.
2. For the Namespace, enter the Kubernetes namespace where you want to deploy the app.
3. In the Manifest files field, select the app-deployment.yaml file from the published artifacts.
4. Set the ImagePullSecrets and other necessary configurations as per your requirements.

### Step 5: Save and Create a Release
1. Save the pipeline with a name like "Quiz-App-CD-Release-Pipeline".
2. Click Create release to start the deployment process.

### Final Steps
1. Ensure that your Kubernetes cluster is configured correctly to pull images from Docker Hub.
2. Verify that the application is deployed successfully in your AKS cluster.

## Conclusion
By following this guide, you will set up a robust CI/CD pipeline using Azure DevOps that automates the entire process of building, testing, and deploying your Quiz App to Azure Kubernetes Service.

For further customization, refer to the official Azure DevOps documentation and Kubernetes deployment guidelines.
