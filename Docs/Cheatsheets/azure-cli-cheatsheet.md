# Azure CLI Cheatsheet

## Setup & Configuration

```bash
az login                                     # interactive browser login
az login --service-principal -u <app-id> -p <password-or-cert> --tenant <tenant-id>
az login --identity                             # managed identity (from within Azure resource)

az account list
az account show
az account set --subscription "My Subscription"
az account list-locations

az configure                                       # set defaults interactively
az configure --defaults group=myrg location=westeurope

az group create --name myrg --location westeurope
az group list
az group delete --name myrg --yes --no-wait
az group show --name myrg

# Global flags (work across most commands)
--output json|table|tsv|yaml
--query "[].{Name:name, Location:location}"          # JMESPath filtering
--subscription "My Subscription"
--resource-group myrg
```

## Resource Management

```bash
az resource list
az resource list --resource-group myrg
az resource show --ids /subscriptions/.../resourceGroups/myrg/providers/...
az resource delete --ids <resource-id>
az resource tag --ids <resource-id> --tags env=prod team=finops

az deployment group create --resource-group myrg --template-file template.json --parameters params.json
az deployment group validate --resource-group myrg --template-file template.json
az deployment group what-if --resource-group myrg --template-file template.json

az provider list
az provider register --namespace Microsoft.Storage
```

## Virtual Machines

```bash
az vm list
az vm list --output table
az vm show --resource-group myrg --name myvm
az vm create --resource-group myrg --name myvm --image Ubuntu2204 \
    --admin-username azureuser --generate-ssh-keys --size Standard_B2s

az vm start --resource-group myrg --name myvm
az vm stop --resource-group myrg --name myvm
az vm deallocate --resource-group myrg --name myvm      # stop AND release compute billing
az vm restart --resource-group myrg --name myvm
az vm delete --resource-group myrg --name myvm --yes

az vm list-sizes --location westeurope
az vm list-images --output table
az vm resize --resource-group myrg --name myvm --size Standard_D2s_v3
az vm open-port --resource-group myrg --name myvm --port 22

az vm extension set --resource-group myrg --vm-name myvm \
    --name CustomScript --publisher Microsoft.Azure.Extensions --settings settings.json

az vmss list                                    # VM scale sets
az vmss create --resource-group myrg --name myvmss --image Ubuntu2204 --instance-count 3
az vmss scale --resource-group myrg --name myvmss --new-capacity 5
```

## Storage (Blob / Files / Queues / Tables)

```bash
az storage account list
az storage account create --name mystorageacct --resource-group myrg --sku Standard_LRS
az storage account show-connection-string --name mystorageacct

az storage container create --name mycontainer --account-name mystorageacct
az storage container list --account-name mystorageacct

az storage blob upload --account-name mystorageacct --container-name mycontainer \
    --name file.txt --file ./file.txt
az storage blob upload-batch --account-name mystorageacct --destination mycontainer --source ./localdir
az storage blob download --account-name mystorageacct --container-name mycontainer \
    --name file.txt --file ./file.txt
az storage blob list --account-name mystorageacct --container-name mycontainer --output table
az storage blob delete --account-name mystorageacct --container-name mycontainer --name file.txt

az storage blob generate-sas --account-name mystorageacct --container-name mycontainer \
    --name file.txt --permissions r --expiry 2026-08-01T00:00:00Z

az storage file upload --share-name myshare --source ./file.txt --account-name mystorageacct
az storage queue create --name myqueue --account-name mystorageacct
az storage message put --queue-name myqueue --content "hello" --account-name mystorageacct
```

## Azure Active Directory / Entra ID & IAM

```bash
az ad user list
az ad user show --id user@domain.com
az ad sp list --display-name myapp
az ad sp create-for-rbac --name myapp --role Contributor --scopes /subscriptions/<sub-id>
az ad app list
az ad group list
az ad group member list --group mygroup

az role assignment list --resource-group myrg
az role assignment create --assignee <object-id> --role "Contributor" --resource-group myrg
az role assignment delete --assignee <object-id> --role "Contributor" --resource-group myrg
az role definition list --output table
az role definition create --role-definition role.json
```

## Networking (VNet, NSG, Load Balancer)

```bash
az network vnet list
az network vnet create --resource-group myrg --name myvnet --address-prefix 10.0.0.0/16 \
    --subnet-name mysubnet --subnet-prefix 10.0.0.0/24
az network vnet subnet list --resource-group myrg --vnet-name myvnet

az network nsg list
az network nsg create --resource-group myrg --name mynsg
az network nsg rule create --resource-group myrg --nsg-name mynsg --name allow-ssh \
    --priority 100 --destination-port-ranges 22 --access Allow --protocol Tcp

az network public-ip create --resource-group myrg --name mypip
az network lb create --resource-group myrg --name mylb --public-ip-address mypip
az network nic list
az network dns zone list
az network route-table list
```

## Azure SQL / Cosmos DB

```bash
az sql server create --name myserver --resource-group myrg --admin-user admin --admin-password <pwd>
az sql server list
az sql db create --resource-group myrg --server myserver --name mydb --service-objective S0
az sql db list --resource-group myrg --server myserver
az sql db show --resource-group myrg --server myserver --name mydb

az cosmosdb list
az cosmosdb create --name mycosmos --resource-group myrg
az cosmosdb sql database create --account-name mycosmos --resource-group myrg --name mydb
az cosmosdb sql container create --account-name mycosmos --resource-group myrg \
    --database-name mydb --name mycontainer --partition-key-path /id
```

## Functions / App Service

```bash
az functionapp list
az functionapp create --resource-group myrg --consumption-plan-location westeurope \
    --runtime python --functions-version 4 --name myfunc --storage-account mystorageacct
az functionapp deployment source config-zip --resource-group myrg --name myfunc --src func.zip
az functionapp show --resource-group myrg --name myfunc
az functionapp log tail --resource-group myrg --name myfunc

az webapp list
az webapp create --resource-group myrg --plan myplan --name mywebapp --runtime "PYTHON:3.12"
az webapp deployment source config-zip --resource-group myrg --name mywebapp --src app.zip
az webapp restart --resource-group myrg --name mywebapp
az webapp log tail --resource-group myrg --name mywebapp

az appservice plan create --resource-group myrg --name myplan --sku B1 --is-linux
```

## AKS (Azure Kubernetes Service)

```bash
az aks create --resource-group myrg --name myaks --node-count 3 --generate-ssh-keys
az aks list
az aks get-credentials --resource-group myrg --name myaks    # configures kubectl
az aks scale --resource-group myrg --name myaks --node-count 5
az aks delete --resource-group myrg --name myaks
az aks nodepool list --resource-group myrg --cluster-name myaks
az aks upgrade --resource-group myrg --name myaks --kubernetes-version 1.29.0
```

## Key Vault

```bash
az keyvault create --name mykeyvault --resource-group myrg --location westeurope
az keyvault secret set --vault-name mykeyvault --name mysecret --value "secretvalue"
az keyvault secret show --vault-name mykeyvault --name mysecret
az keyvault secret list --vault-name mykeyvault
az keyvault secret delete --vault-name mykeyvault --name mysecret
az keyvault key create --vault-name mykeyvault --name mykey --kty RSA
az keyvault certificate create --vault-name mykeyvault --name mycert -p @policy.json
az keyvault set-policy --name mykeyvault --object-id <id> --secret-permissions get list
```

## Monitor / Log Analytics

```bash
az monitor metrics list --resource <resource-id> --metric "Percentage CPU"
az monitor activity-log list --resource-group myrg
az monitor log-analytics workspace create --resource-group myrg --workspace-name myworkspace
az monitor log-analytics query --workspace <workspace-id> --analytics-query "AzureActivity | take 10"

az monitor alert create --resource-group myrg --name my-alert --target <resource-id> \
    --condition "avg Percentage CPU > 80"

az monitor diagnostic-settings create --resource <resource-id> --name mydiag \
    --logs '[{"category": "AuditLogs","enabled": true}]' --workspace <workspace-id>
```

## Cost Management

```bash
az consumption usage list
az costmanagement query --type Usage --timeframe MonthToDate \
    --dataset-aggregation '{"totalCost":{"name":"PreTaxCost","function":"Sum"}}' \
    --scope "/subscriptions/<sub-id>"
az billing account list
az billing invoice list
```

## Azure Data Factory / Synapse

```bash
az datafactory list
az datafactory create --resource-group myrg --factory-name myadf --location westeurope
az datafactory pipeline list --resource-group myrg --factory-name myadf
az datafactory pipeline create-run --resource-group myrg --factory-name myadf --name mypipeline

az synapse workspace list
az synapse workspace create --name myworkspace --resource-group myrg \
    --storage-account mystorageacct --file-system myfs --sql-admin-login-user admin \
    --sql-admin-login-password <pwd> --location westeurope
az synapse sql pool list --workspace-name myworkspace --resource-group myrg
az synapse spark pool list --workspace-name myworkspace --resource-group myrg
```

## Container Registry (ACR)

```bash
az acr create --resource-group myrg --name myacr --sku Basic
az acr login --name myacr
az acr build --registry myacr --image myimage:tag .
az acr repository list --name myacr
az acr repository show-tags --name myacr --repository myimage
az acr task create --registry myacr --name mytask --image myimage:{{.Run.ID}} \
    --context https://github.com/user/repo.git --file Dockerfile
```

## CLI Productivity Tips

```bash
az <command> --help                       # help for any command/group
az find "az vm create"                       # search docs/examples

az config set core.output=table                # persist default output format
az interactive                                    # interactive shell with autocomplete

# JMESPath querying
az vm list --query "[].{Name:name, Size:hardwareProfile.vmSize}" --output table
az vm list --query "[?location=='westeurope']"

# REST passthrough for anything not covered by a dedicated command
az rest --method get --url "https://management.azure.com/subscriptions?api-version=2020-01-01"
```
