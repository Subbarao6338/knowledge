# AWS CLI Cheatsheet

## Setup & Configuration

```bash
aws configure                                    # interactive: access key, secret, region, output format
aws configure --profile myprofile
aws configure list
aws configure list-profiles
aws configure get region
aws configure set region eu-central-1

export AWS_PROFILE=myprofile
export AWS_REGION=eu-central-1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...                        # for temporary/STS credentials

aws sts get-caller-identity                            # who am I / which account+role
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/MyRole --role-session-name mysession
aws sts assume-role-with-web-identity ...

# Global output/query flags (work on almost every command)
--output json|table|text|yaml
--query "Reservations[].Instances[].InstanceId"        # JMESPath filtering
--profile myprofile
--region eu-central-1
--no-cli-pager
--dry-run
```

## IAM

```bash
aws iam list-users
aws iam list-roles
aws iam list-policies --scope Local
aws iam get-user --user-name myuser
aws iam create-user --user-name myuser
aws iam delete-user --user-name myuser
aws iam create-role --role-name myrole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name myrole --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
aws iam detach-role-policy --role-name myrole --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
aws iam list-attached-role-policies --role-name myrole
aws iam create-policy --policy-name mypolicy --policy-document file://policy.json
aws iam create-access-key --user-name myuser
aws iam list-access-keys --user-name myuser
aws iam delete-access-key --access-key-id AKIA... --user-name myuser
aws iam get-policy-version --policy-arn <arn> --version-id v1
aws iam simulate-principal-policy --policy-source-arn <arn> --action-names s3:GetObject
```

## S3

```bash
aws s3 ls                                       # list buckets
aws s3 ls s3://mybucket/                            # list objects in a bucket/prefix
aws s3 ls s3://mybucket/ --recursive --human-readable --summarize

aws s3 mb s3://mybucket                           # make bucket
aws s3 rb s3://mybucket --force                      # remove bucket (and contents)

aws s3 cp file.txt s3://mybucket/                 # upload
aws s3 cp s3://mybucket/file.txt .                    # download
aws s3 cp s3://mybucket/ s3://otherbucket/ --recursive    # bucket-to-bucket copy
aws s3 sync ./localdir s3://mybucket/prefix/             # sync (only changed/new files)
aws s3 sync s3://mybucket/prefix/ ./localdir --delete       # sync + remove local files not in source
aws s3 mv file.txt s3://mybucket/
aws s3 rm s3://mybucket/file.txt
aws s3 rm s3://mybucket/prefix/ --recursive

aws s3 presign s3://mybucket/file.txt --expires-in 3600      # generate a presigned URL

# s3api — lower-level, more control
aws s3api list-buckets
aws s3api list-objects-v2 --bucket mybucket --prefix data/
aws s3api head-object --bucket mybucket --key file.txt
aws s3api put-object --bucket mybucket --key file.txt --body ./file.txt
aws s3api get-object --bucket mybucket --key file.txt out.txt
aws s3api delete-object --bucket mybucket --key file.txt
aws s3api put-bucket-versioning --bucket mybucket --versioning-configuration Status=Enabled
aws s3api put-bucket-policy --bucket mybucket --policy file://policy.json
aws s3api get-bucket-lifecycle-configuration --bucket mybucket
aws s3api create-multipart-upload --bucket mybucket --key bigfile.zip
```

## EC2

```bash
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 describe-instances --query "Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,State:State.Name}" --output table

aws ec2 run-instances --image-id ami-xxxx --instance-type t3.micro --key-name mykey \
    --security-group-ids sg-xxxx --subnet-id subnet-xxxx --count 1

aws ec2 start-instances --instance-ids i-xxxx
aws ec2 stop-instances --instance-ids i-xxxx
aws ec2 terminate-instances --instance-ids i-xxxx
aws ec2 reboot-instances --instance-ids i-xxxx

aws ec2 describe-images --owners self
aws ec2 create-image --instance-id i-xxxx --name "my-ami"
aws ec2 describe-security-groups
aws ec2 create-security-group --group-name mysg --description "my sg" --vpc-id vpc-xxxx
aws ec2 authorize-security-group-ingress --group-id sg-xxxx --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 describe-volumes
aws ec2 create-volume --availability-zone eu-central-1a --size 20 --volume-type gp3
aws ec2 create-snapshot --volume-id vol-xxxx

aws ec2 describe-vpcs
aws ec2 describe-subnets
aws ec2 describe-key-pairs
aws ec2 create-key-pair --key-name mykey --query "KeyMaterial" --output text > mykey.pem
```

## Lambda

```bash
aws lambda list-functions
aws lambda get-function --function-name myfunc
aws lambda create-function --function-name myfunc --runtime python3.12 \
    --role arn:aws:iam::123456789012:role/lambda-role --handler app.handler \
    --zip-file fileb://function.zip
aws lambda update-function-code --function-name myfunc --zip-file fileb://function.zip
aws lambda update-function-configuration --function-name myfunc --timeout 30 --memory-size 512
aws lambda invoke --function-name myfunc --payload '{"key":"value"}' response.json
aws lambda delete-function --function-name myfunc
aws lambda list-event-source-mappings --function-name myfunc
aws lambda add-permission --function-name myfunc --statement-id sid1 \
    --action lambda:InvokeFunction --principal s3.amazonaws.com
```

## Athena

```bash
aws athena start-query-execution \
    --query-string "SELECT * FROM my_table LIMIT 10" \
    --query-execution-context Database=my_database \
    --result-configuration OutputLocation=s3://my-athena-results/

aws athena get-query-execution --query-execution-id <id>
aws athena get-query-results --query-execution-id <id>
aws athena stop-query-execution --query-execution-id <id>
aws athena list-query-executions
aws athena list-databases --catalog-name AwsDataCatalog
aws athena list-table-metadata --catalog-name AwsDataCatalog --database-name my_database
aws athena get-table-metadata --catalog-name AwsDataCatalog --database-name my_database --table-name my_table
aws athena list-work-groups
```

## Glue / Data Catalog

```bash
aws glue get-databases
aws glue get-tables --database-name my_database
aws glue get-table --database-name my_database --name my_table
aws glue start-crawler --name my-crawler
aws glue get-crawler --name my-crawler
aws glue start-job-run --job-name my-etl-job
aws glue get-job-runs --job-name my-etl-job
```

## RDS

```bash
aws rds describe-db-instances
aws rds describe-db-instances --query "DBInstances[].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Engine:Engine}"
aws rds create-db-instance --db-instance-identifier mydb --db-instance-class db.t3.micro \
    --engine postgres --master-username admin --master-user-password mypassword --allocated-storage 20
aws rds start-db-instance --db-instance-identifier mydb
aws rds stop-db-instance --db-instance-identifier mydb
aws rds delete-db-instance --db-instance-identifier mydb --skip-final-snapshot
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snap
aws rds describe-db-snapshots
```

## CloudWatch

```bash
aws cloudwatch list-metrics --namespace AWS/EC2
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-xxxx --start-time 2026-07-16T00:00:00Z \
    --end-time 2026-07-17T00:00:00Z --period 3600 --statistics Average

aws cloudwatch put-metric-alarm --alarm-name high-cpu --metric-name CPUUtilization \
    --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 \
    --comparison-operator GreaterThanThreshold --evaluation-periods 2 \
    --alarm-actions arn:aws:sns:...

aws logs describe-log-groups
aws logs describe-log-streams --log-group-name /aws/lambda/myfunc
aws logs get-log-events --log-group-name /aws/lambda/myfunc --log-stream-name <stream>
aws logs tail /aws/lambda/myfunc --follow                    # live tail
aws logs filter-log-events --log-group-name /aws/lambda/myfunc --filter-pattern "ERROR"
```

## CloudFormation

```bash
aws cloudformation deploy --template-file template.yaml --stack-name mystack \
    --capabilities CAPABILITY_IAM
aws cloudformation create-stack --stack-name mystack --template-body file://template.yaml
aws cloudformation update-stack --stack-name mystack --template-body file://template.yaml
aws cloudformation delete-stack --stack-name mystack
aws cloudformation describe-stacks --stack-name mystack
aws cloudformation describe-stack-events --stack-name mystack
aws cloudformation list-stacks
aws cloudformation validate-template --template-body file://template.yaml
```

## ECS / ECR

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.eu-central-1.amazonaws.com
aws ecr create-repository --repository-name myrepo
aws ecr describe-repositories
aws ecr list-images --repository-name myrepo
aws ecr batch-delete-image --repository-name myrepo --image-ids imageTag=old

aws ecs list-clusters
aws ecs list-services --cluster mycluster
aws ecs describe-services --cluster mycluster --services myservice
aws ecs update-service --cluster mycluster --service myservice --desired-count 3
aws ecs run-task --cluster mycluster --task-definition mytask
aws ecs list-tasks --cluster mycluster
```

## SNS / SQS

```bash
aws sns list-topics
aws sns create-topic --name mytopic
aws sns publish --topic-arn arn:aws:sns:... --message "hello"
aws sns subscribe --topic-arn arn:aws:sns:... --protocol email --notification-endpoint you@example.com

aws sqs list-queues
aws sqs create-queue --queue-name myqueue
aws sqs send-message --queue-url <url> --message-body "hello"
aws sqs receive-message --queue-url <url>
aws sqs delete-message --queue-url <url> --receipt-handle <handle>
aws sqs purge-queue --queue-url <url>
```

## Secrets Manager / SSM Parameter Store

```bash
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id mysecret
aws secretsmanager create-secret --name mysecret --secret-string "value"
aws secretsmanager update-secret --secret-id mysecret --secret-string "newvalue"
aws secretsmanager delete-secret --secret-id mysecret

aws ssm get-parameter --name /myapp/config --with-decryption
aws ssm put-parameter --name /myapp/config --value "value" --type SecureString
aws ssm get-parameters-by-path --path /myapp/ --recursive
aws ssm describe-parameters
```

## STS / Cross-Account Role Assumption (GCP → AWS pattern)

```bash
# Assume a role using a web identity token (used for OIDC federation, e.g. GCP workload identity)
aws sts assume-role-with-web-identity \
    --role-arn arn:aws:iam::351931932460:role/MyCrossCloudRole \
    --role-session-name gcp-session \
    --web-identity-token file://token.jwt

# Standard cross-account assume-role (with an existing credential/session)
aws sts assume-role --role-arn arn:aws:iam::351931932460:role/MyRole --role-session-name mysession

# Output includes AccessKeyId, SecretAccessKey, SessionToken — export these to use the assumed role
```

## VPC / Networking

```bash
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 describe-route-tables
aws ec2 create-route --route-table-id rtb-xxxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxxx
aws ec2 describe-internet-gateways
aws ec2 describe-nat-gateways
aws ec2 describe-network-interfaces
```

## CLI Productivity Tips

```bash
aws <service> help                          # command help
aws <service> <action> help                    # action-specific help

aws configure set cli_pager ""                    # disable the pager permanently
aws --query "..." --output text                     # JMESPath query examples:
    "Reservations[*].Instances[*].[InstanceId,State.State.Name]"
    "Users[?UserName=='myuser']"
    "length(Buckets)"

# Waiters — block until a resource reaches a state
aws ec2 wait instance-running --instance-ids i-xxxx
aws cloudformation wait stack-create-complete --stack-name mystack

# Combine with jq for advanced JSON processing
aws ec2 describe-instances --output json | jq '.Reservations[].Instances[].InstanceId'
```
