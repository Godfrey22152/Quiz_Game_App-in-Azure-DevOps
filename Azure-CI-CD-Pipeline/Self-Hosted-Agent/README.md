## Overview

This guide explains how to set up a self-hosted agent for Azure CI/CD pipeline using Vagrant and VirtualBox. The Vagrantfile provisions an Ubuntu 22.04 environment with necessary tools such as Python, Docker, Trivy, Bandit, Pytest, and Docker Scout CLI.

## Prerequisites

Before starting, ensure you have the following installed on your host machine:

1. [Vagrant](https://www.vagrantup.com/downloads)
2. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Setting Up the Vagrant Environment

### Step 1: Create a New Directory

Create a new directory for your Vagrant environment and navigate into it:

```sh
mkdir self-hosted-agent
cd self-hosted-agent

```
### Step 2: Create the Vagrantfile
Create a Vagrantfile in the directory with the following content:

```sh
# Vagrantfile for an Ubuntu 22.04 self-hosted agent for Azure CI/CD pipeline
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  
  # Allocate 4GB of RAM
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  # Provisioning script
  config.vm.provision "shell", inline: <<-SHELL
    # Update and upgrade the system
    sudo apt-get update

    # Install Python and pip
    sudo apt-get install -y python3 python3-pip

    # Install Docker
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo chmod 666 /var/run/docker.sock

    # Install Trivy
    wget https://github.com/aquasecurity/trivy/releases/download/v0.27.1/trivy_0.27.1_Linux-64bit.deb
    sudo dpkg -i trivy_0.27.1_Linux-64bit.deb

    # Install Bandit
    pip install bandit
    
    # Install Pytest and Pytest-cov
    pip install pytest pytest-cov

    # Install Docker Scout CLI
    curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
  SHELL
end

```
### Step 3: Start the Vagrant Environment
Run the following command to start the Vagrant environment:

```sh
vagrant up

```
This command will download the specified Ubuntu box, create a virtual machine, and run the provisioning script to install the necessary tools.

### Step 4: SSH into the Vagrant Machine
Once the setup is complete, SSH into the Vagrant machine:

```sh
vagrant ssh

```
You now have a self-hosted agent environment with all required tools installed.

## Configuring the Agent for Azure DevOps

### Step 1: Download the Agent
Within the Vagrant machine, download the Azure Pipelines agent:

```sh
# Replace 'your-organization' and 'your-project' with your actual Azure DevOps organization and project names.
wget https://vstsagentpackage.azureedge.net/agent/3.242.1/vsts-agent-linux-x64-3.242.1.tar.gz
mkdir myagent && cd myagent
tar zxvf ~/Downloads/vsts-agent-linux-x64-3.242.1.tar.gz

```
### Step 2: Configure the Agent
Configure the agent by running the configuration script:

```sh
# Replace the placeholder values with your actual Azure DevOps details
./config.sh --url https://dev.azure.com/your-organization --agent SelfHostedAgent --pool Default --work _work --auth pat --token YOUR_PERSONAL_ACCESS_TOKEN

# Or Configure the agent by running the configuration script and Follow the prompts to complete the configuration.
./config.sh
```
### Step 3: Run the Agent
Start the agent:

```
./run.sh
```
The agent is now ready and should be available in your Azure DevOps organization.

## Conclusion
By following this guide, you have successfully set up a self-hosted agent using Vagrant and VirtualBox, configured it with necessary tools, and connected it to your Azure DevOps organization. You can now use this agent to run your CI/CD pipelines.

## Additional Resources
1. [Azure DevOps Documentation](https://learn.microsoft.com/en-us/azure/devops/?view=azure-devops)
2. [Vagrant Cheat Sheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4)

