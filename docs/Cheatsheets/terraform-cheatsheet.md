---
layout: default
title: "Terraform Cheatsheet"
---

# Terraform Cheatsheet

Terraform is an open-source infrastructure as code (IaC) software tool created by HashiCorp. It enables users to define and provision a datacenter infrastructure using a high-level configuration language known as HashiCorp Configuration Language (HCL).

---

## 1. Core Workflow Commands

The standard Terraform workflow consists of three main steps: Write, Plan, and Apply.

```bash
# Initialize a new or existing Terraform working directory (downloads providers/modules)
terraform init

# Check whether the configuration is valid and syntactically correct
terraform validate

# Automatically format HCL files to follow standard canonical style rules
terraform fmt -recursive

# Generate and show an execution plan (dry run to see what resources will be created/modified)
terraform plan -out=tfplan.binary

# Apply the changes required to reach the desired state of the configuration
terraform apply tfplan.binary

# Destroy all managed infrastructure in the current environment
terraform destroy -auto-approve
```

---

## 2. Configuration Syntax (HCL)

### Provider Configuration
Providers are plugins that Terraform uses to communicate with cloud providers, SaaS providers, and other APIs.

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

### Input Variables & Outputs
Input variables act as function parameters, while output values are like function return values.

```hcl
variable "aws_region" {
  type        = string
  description = "The target AWS deployment region"
  default     = "us-east-1"
}

variable "instance_config" {
  type = object({
    ami           = string
    instance_type = string
    subnet_ids    = list(string)
  })
}

output "instance_public_ip" {
  value       = aws_instance.web.public_ip
  description = "The public IP address of the deployed EC2 instance"
}
```

### Resource and Data Source Blocks
* **Resource:** Declares an infrastructure component that Terraform will manage.
* **Data Source:** Fetches data from APIs or existing cloud environments outside Terraform's scope.

```hcl
# Fetch the latest Amazon Linux 2 AMI
data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Create a virtual server
resource "aws_instance" "web" {
  ami           = data.aws_ami.latest_amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = var.instance_config.subnet_ids[0]

  tags = {
    Name        = "Web-Server-Instance"
    Environment = "production"
  }
}
```

---

## 3. Advanced Expression & Logic

### Count vs For Each
* Use `count` for loops when resources are identical or based on a simple index.
* Use `for_each` when creating distinct resources based on a map or set of strings (prevents index-shift destroy problems).

```hcl
# Example of for_each with a map
resource "aws_iam_user" "users" {
  for_each = toset(["developer-1", "developer-2", "ops-lead"])
  name     = each.key
}

# Dynamic Block inside an AWS Security Group
resource "aws_security_group" "web_sg" {
  name        = "web-server-sg"
  description = "Allow port 80 and 443 inbound"

  dynamic "ingress" {
    for_each = [80, 443]
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

---

## 4. State Management Reference

Terraform records information about what real infrastructure it created in a state file (`terraform.tfstate`).

```bash
# List all resources currently recorded in the state file
terraform state list

# Show detailed attributes of a specific resource in the state
terraform state show aws_instance.web

# Move/rename a resource within state without destroying/creating it
terraform state mv aws_instance.old_name aws_instance.new_name

# Remove a resource from state so that Terraform stops tracking it
terraform state rm aws_instance.web

# Import existing infrastructure into your Terraform state file
terraform import aws_instance.web i-0123456789abcdef0
```

### Remote Backend Configuration (With S3 and DynamoDB Locking)
```hcl
terraform {
  backend "s3" {
    bucket         = "my-enterprise-tfstate-bucket"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
    encrypt        = true
  }
}
```

---

## 5. Working with Modules

Modules are reusable packages of Terraform configurations.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "production"
  }
}
```

---

## 6. Security & Best Practices

1. **Never commit sensitive `.tfvars` or `.tfstate` files to git.** Always add them to your `.gitignore`.
2. **Lock your state:** Use backend lockers (like DynamoDB) to prevent concurrent executions from corrupting the state file.
3. **Pin version numbers:** Pin both provider versions and module versions to avoid unexpected breaking updates.
4. **Use local-only variables safely:** Mark sensitive variables to prevent them from showing up in console output logs:
   ```hcl
   variable "db_password" {
     type      = string
     sensitive = true
   }
   ```
