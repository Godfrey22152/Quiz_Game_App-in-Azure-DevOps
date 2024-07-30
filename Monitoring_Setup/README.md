# Self-hosted Prometheus and Grafana to monitor your Azure Kubernetes Service (AKS) cluster.

# definition
Prometheus is an open-source systems monitoring and alerting toolkit. Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels. Grafana is an open-source platform for monitoring and observability. It allows you to query, visualize, alert on and understand your metrics no matter where they are stored.

Setting up self-hosted Prometheus and Grafana to monitor your Azure Kubernetes Service (AKS) cluster involves several steps. Here’s a step-by-step guide to help you through the process:

## Steps to be followed:

1. Prerequisites
2. Setup Port-forwarding for both Prometheus and Grafana
3. Create a Service Principal and add roles to AKS cluster RG
4. Create Data Source in Grafana
5. Import Azure Monitor for Containers in Grafana
6. View the metrics in Grafana Dashboard

## Prerequisites
1. Azure Kubernetes Service (AKS) cluster: Ensure you have an AKS cluster up and running.
2. Environment Setup:
- **Local Machine:**
   - Ensure you have kubectl and Helm installed on your local machine.
   - Your local machine should be configured to access your AKS cluster.
- **Cloud Shell:**
   - You can use Azure Cloud Shell, which has kubectl and Helm pre-installed and configured to access your Azure resources.

## Detailed Execution Steps

1. Configure kubectl to Connect to AKS
- First, connect kubectl to your AKS cluster from your local machine or Cloud Shell:

```bash
az aks get-credentials --resource-group <your-resource-group> --name <your-aks-cluster>
```
- Verify the connection

```bash
kubectl get nodes
```
2. Create a Namespace for Monitoring
Create a namespace in your AKS cluster to separate your monitoring components:

``` bash
kubectl create namespace monitoring
```
3. Add Helm Repositories
Add the Helm repositories for Prometheus and Grafana:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
4. Deploy Prometheus
Execute this command to deploy Prometheus in your AKS cluster:

```bash
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```
This command installs the kube-prometheus-stack which includes Prometheus, Alertmanager, and Grafana.

5. Verify Prometheus and Grafana Deployment: Check all resources in Monitoring Namespace.

```bash
kubectl get all --namespace monitoring 
```
You should see pods for Prometheus, Grafana, Alertmanager, and other components running.

6. Accessing Prometheus and Grafana
- **Option 1:** To access Prometheus and Grafana dashboards, you can use port forwarding.

**Prometheus:**
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```
Open a browser and go to `http://localhost:9090`.

**Grafana:**
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```
Open a browser and go to `http://localhost:3000`. 
The default username is "admin". The Username and the password can be retrieved with:

 - **Retrieve the Username:**
 ```bash
 kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 --decode ; echo
 ```
 - **Retrieve the password:**
 ```bash
 kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
 ```
- **Option 2:** Alternative Method to Access Prometheus and Grafana.
Access via LoadBalancer:
If port-forwarding is not working, you can expose the Prometheus and grafana service using a LoadBalancer.

**Prometheus:**
```bash
kubectl patch svc prometheus-kube-prometheus-prometheus -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc prometheus-kube-prometheus-prometheus -n monitoring
```
**Grafana:**
```bash
kubectl patch svc prometheus-grafana -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc prometheus-grafana -n monitoring
```
After patching, you will get a new EXTERNAL-IP for your service. You can then access Prometheus and grafana using this IP address.

7. Create a Log Analytics workspace if none exists:
- In the Azure Portal, select "Create a resource" and then search for "Log Analytics".
- Follow the prompts to create a new Log Analytics workspace.

8. Register the Azure Resource Manager API
- Check if the ARM API is registered:
 - Go to the Azure Portal.
 - Navigate to "Subscriptions" and select your subscription.
 - In the left-hand menu, select "Resource providers".
 - Search for "Microsoft.Resources".
 - Ensure that it is registered. If it is not, click on "Register".

9. Create a Service Principal and Assign Role
- Create a Service Principal:
Open Azure Cloud Shell or your local terminal with Azure CLI installed.
Run the following command to create a service principal:

```bash
az ad sp create-for-rbac --name "<ServicePrincipalName>" --role Reader --scopes /subscriptions/<SubscriptionID>
```
Replace <ServicePrincipalName> with a name for your service principal and <SubscriptionID> with your Azure subscription ID.

- Save the output:
The command will output JSON with the following details:
```bash
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "displayName": "<ServicePrincipalName>",
  "password": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```
 - The appId is your Client ID.
 - The password is your Client Secret.
 - The tenant is your Tenant ID.

- Assign Reader Role to the Service Principal:

```bash
az role assignment create --role "Reader" --assignee <Client ID> --scope /subscriptions/<Subscription ID>/resourceGroups/<Resource Group>/providers/Microsoft.OperationalInsights/workspaces/<Log Analytics Workspace Name>
```
Replace the placeholders with the actual values:

 - <Client ID>: The appId from the service principal creation or retrieval step.
 - <Subscription ID>: Your Azure subscription ID.
 - <Resource Group>: The resource group containing your Log Analytics workspace.
 - <Log Analytics Workspace Name>: The name of your Log Analytics workspace.

10. Create Data Source in Grafana
- Configure Azure Monitor as a Data Source:
 - In Grafana, go to "Configuration" -> "Data Sources".
 - Add a new data source and select "Azure Monitor".
 - Enter the required details such as Subscription ID, Tenant ID, Client ID, and Client Secret.
 - Click "Save & Test" to ensure the connection is working.

- Configure Prometheus as a Data Source (if applicable):

 - In Grafana, go to "Configuration" -> "Data Sources".
 - Add a new data source and select "Prometheus".
 - Enter the URL of your Prometheus server (e.g., http://localhost:9090 if using port-forwarding).
 - Click "Save & Test" to ensure the connection is working.

![Data Source In Grafana](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bGQUEsCswqIXbJFCj1NZWQ.png)

11. Import a Kubernetes Dashboard
- First Dashboard import: Import Azure Monitor for Containers in Grafana
Go to Create and click import.
Import Dashboard ID 10956 and load and finally import the “Azure Monitor for Containers — Metrics” Dashboard.

![Import Azure Monitor for Containers in Grafana](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*EbhsC7max_vhHd_Vc4KNEQ.png)


- Second Dashboard Import: In Grafana, go to "Create" -> "Import".
You can use the dashboard ID from Grafana's dashboard library. For Kubernetes monitoring, a popular choice is dashboard ID 315, which is "Kubernetes cluster monitoring (via Prometheus)".

-**NOTE:**
Select the Data Source:
- During the import process, you will be prompted to select data sources for various metrics.
- For metrics coming from Prometheus, select the Prometheus data source.
- For metrics coming from Azure Monitor, select the Azure Monitor data source.

**SUMMARY:**
Dashboards give us a visual representation of the AKS cluster’s health, resource utilisation trends of specific application pods, network traffic flow across the cluster, and much more. Prometheus and Grafana are powerful monitoring tools for Kubernetes clusters, and Helm makes it simple to set up and get up and running in minutes.
