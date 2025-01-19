## Local Setup for Terraform and GCP

### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/ 

### Terraform Concepts
[Terraform Overview](1_terraform_overview.md)

### GCP setup

1. [Setup for First-time](2_gcp_overview.md#initial-setup)
    * [Only for Windows](windows.md) - Steps 4 & 5
2. [IAM / Access specific to this course](2_gcp_overview.md#setup-for-access)

### Terraform Workshop for GCP Infra
Your setup is ready!
Now head to the [terraform](terraform) directory, and perform the execution steps to create your infrastructure.



### Concepts
* [Terraform_overview](../1_terraform_overview.md)

### Execution

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

-----------------------------



## Install the Google Cloud CLI
https://cloud.google.com/sdk/docs/install-sdk#deb

- Setup app default login
```shell
export GOOGLE_APPLICATION_CREDENTIALS="/home/lan/.config/gcloud/google-terraform-creds.json"
echo $GOOGLE_APPLICATION_CREDENTIALS

gcloud auth login
gcloud config set project advance-vector-447116-m5
gcloud auth application-default set-quota-project advance-vector-447116-m5

gcloud auth application-default login
```

## Terraform intro
- [DE Zoomcamp 1.3.2 - Terraform Basics](https://www.youtube.com/watch?v=Y2ux7gq3Z0o&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12)
- [DE Zoomcamp 1.3.3 - Terraform Variables](https://www.youtube.com/watch?v=PBi0hHjLftk&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=13)

## Install the Teffaform
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
```
sudo mv terraform /usr/local/bin
sudo chmod +x /usr/local/bin/terraform
# Initialize state file (.tfstate)
terraform init
```

## Configure Terraform's code & run
- Prepare main.tf & variables.tf
```bash
# Check changes to new infra plan
terraform plan 
# Create new infra
terraform apply
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```