# GCP CLI Cheatsheet (gcloud / gsutil / bq)

## Setup & Configuration

```bash
gcloud init                                    # interactive setup
gcloud auth login
gcloud auth application-default login              # ADC for local SDK/client library use
gcloud auth list
gcloud auth revoke

gcloud config list
gcloud config set project tefde-gcp-finops-prod
gcloud config set compute/region europe-west3
gcloud config set compute/zone europe-west3-a
gcloud config configurations list
gcloud config configurations create myconfig
gcloud config configurations activate myconfig

gcloud projects list
gcloud projects describe tefde-gcp-finops-prod
gcloud components update
gcloud components install <component>

# Global flags (work on most commands)
--project=my-project
--format=json|yaml|table|csv|value|text
--filter="status:RUNNING"
--limit=10
--quiet / -q                              # skip confirmation prompts
```

## IAM & Service Accounts

```bash
gcloud iam service-accounts list
gcloud iam service-accounts create my-sa --display-name "My SA"
gcloud iam service-accounts describe my-sa@my-project.iam.gserviceaccount.com
gcloud iam service-accounts keys create key.json --iam-account my-sa@my-project.iam.gserviceaccount.com
gcloud iam service-accounts keys list --iam-account my-sa@my-project.iam.gserviceaccount.com
gcloud iam service-accounts delete my-sa@my-project.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:my-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
gcloud projects remove-iam-policy-binding my-project \
    --member="serviceAccount:my-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
gcloud projects get-iam-policy my-project

gcloud iam roles list
gcloud iam roles describe roles/bigquery.dataViewer
gcloud iam roles create myCustomRole --project my-project --file role-definition.yaml

# Workload Identity Federation (GCP -> AWS/Azure cross-cloud pattern)
gcloud iam workload-identity-pools create my-pool --location global
gcloud iam workload-identity-pools providers create-aws my-aws-provider \
    --workload-identity-pool my-pool --account-id 351931932460 --location global
gcloud iam service-accounts add-iam-policy-binding my-sa@my-project.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "principalSet://iam.googleapis.com/projects/.../workloadIdentityPools/my-pool/*"
```

## Compute Engine

```bash
gcloud compute instances list
gcloud compute instances describe myinstance --zone europe-west3-a
gcloud compute instances create myinstance --zone europe-west3-a \
    --machine-type e2-medium --image-family debian-12 --image-project debian-cloud

gcloud compute instances start myinstance --zone europe-west3-a
gcloud compute instances stop myinstance --zone europe-west3-a
gcloud compute instances delete myinstance --zone europe-west3-a
gcloud compute instances reset myinstance --zone europe-west3-a

gcloud compute ssh myinstance --zone europe-west3-a
gcloud compute scp file.txt myinstance:~/ --zone europe-west3-a

gcloud compute disks list
gcloud compute disks create mydisk --size 50GB --zone europe-west3-a
gcloud compute snapshots create mysnapshot --source-disk mydisk --zone europe-west3-a

gcloud compute images list
gcloud compute machine-types list --zones europe-west3-a
gcloud compute firewall-rules list
gcloud compute firewall-rules create allow-ssh --allow tcp:22 --source-ranges 0.0.0.0/0

gcloud compute instance-groups list
gcloud compute instance-groups managed create mygroup --template mytemplate --size 3 --zone europe-west3-a
gcloud compute instance-groups managed resize mygroup --size 5 --zone europe-west3-a
```

## Cloud Storage (gsutil + gcloud storage)

```bash
# Modern: gcloud storage (recommended, faster, being unified with gsutil)
gcloud storage buckets list
gcloud storage buckets create gs://my-bucket --location europe-west3
gcloud storage buckets delete gs://my-bucket
gcloud storage ls gs://my-bucket/
gcloud storage cp file.txt gs://my-bucket/
gcloud storage cp gs://my-bucket/file.txt .
gcloud storage cp -r gs://my-bucket/prefix/ ./localdir/
gcloud storage rsync ./localdir gs://my-bucket/prefix/ --recursive
gcloud storage rm gs://my-bucket/file.txt
gcloud storage rm -r gs://my-bucket/prefix/

# Classic gsutil (still widely used, scripts, and some advanced features)
gsutil mb -l europe-west3 gs://my-bucket
gsutil rb gs://my-bucket
gsutil ls gs://my-bucket/
gsutil ls -lh gs://my-bucket/**
gsutil cp file.txt gs://my-bucket/
gsutil cp -r ./localdir gs://my-bucket/prefix/
gsutil mv gs://my-bucket/old.txt gs://my-bucket/new.txt
gsutil rm gs://my-bucket/file.txt
gsutil rm -r gs://my-bucket/prefix/
gsutil rsync -r ./localdir gs://my-bucket/prefix/
gsutil du -sh gs://my-bucket/
gsutil cat gs://my-bucket/file.txt
gsutil signurl -d 1h key.json gs://my-bucket/file.txt
gsutil iam get gs://my-bucket
gsutil iam ch user:you@example.com:objectViewer gs://my-bucket
gsutil lifecycle set lifecycle.json gs://my-bucket
gsutil versioning set on gs://my-bucket
```

## BigQuery (bq CLI)

```bash
bq ls                                          # list datasets in current project
bq ls my_dataset                                  # list tables in a dataset
bq ls -j                                             # list recent jobs

bq mk my_dataset
bq mk --table my_dataset.my_table schema.json
bq rm -t my_dataset.my_table
bq rm -r -f my_dataset                                # remove dataset + tables

bq show my_dataset.my_table
bq show --schema --format=prettyjson my_dataset.my_table

bq query --use_legacy_sql=false 'SELECT * FROM `my_project.my_dataset.my_table` LIMIT 10'
bq query --use_legacy_sql=false --destination_table=my_dataset.result_table \
    --replace 'SELECT category, SUM(value) FROM `my_dataset.my_table` GROUP BY category'

bq load --source_format=CSV --skip_leading_rows=1 \
    my_dataset.my_table gs://my-bucket/data.csv schema.json
bq load --source_format=PARQUET my_dataset.my_table gs://my-bucket/data.parquet

bq extract my_dataset.my_table gs://my-bucket/export-*.csv
bq extract --destination_format=PARQUET my_dataset.my_table gs://my-bucket/export-*.parquet

bq cp source_dataset.source_table dest_dataset.dest_table
bq update --description "my description" my_dataset.my_table

bq ls --format=prettyjson -j -a --max_results=10
bq cancel <job_id>
bq wait <job_id>
```

## Cloud Run

```bash
gcloud run deploy myservice --image gcr.io/my-project/myimage:latest \
    --region europe-west3 --platform managed --allow-unauthenticated

gcloud run deploy myservice --source . --region europe-west3   # build+deploy from source

gcloud run services list
gcloud run services describe myservice --region europe-west3
gcloud run services update myservice --region europe-west3 --memory 2Gi --cpu 2
gcloud run services update myservice --region europe-west3 \
    --set-env-vars KEY1=value1,KEY2=value2
gcloud run services delete myservice --region europe-west3

gcloud run revisions list --service myservice --region europe-west3
gcloud run services update-traffic myservice --region europe-west3 --to-latest
gcloud run jobs create myjob --image gcr.io/my-project/myimage:latest --region europe-west3
gcloud run jobs execute myjob --region europe-west3

gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=myservice" --limit 50
```

## Vertex AI (Agent Engine / Reasoning Engine, Models, Pipelines)

```bash
gcloud ai models list --region europe-west3
gcloud ai models upload --region europe-west3 --display-name mymodel --container-image-uri <uri>
gcloud ai endpoints list --region europe-west3
gcloud ai endpoints create --region europe-west3 --display-name myendpoint
gcloud ai endpoints deploy-model <endpoint-id> --region europe-west3 --model=<model-id> \
    --display-name mydeployment --machine-type n1-standard-4

# ADK / Agent Engine (Reasoning Engine) deployment typically goes via `adk deploy agent_engine`
# or the Vertex AI SDK rather than raw gcloud commands, but reasoning engines can be inspected via:
gcloud ai reasoning-engines list --region europe-west3
gcloud ai reasoning-engines describe <reasoning-engine-id> --region europe-west3
gcloud ai reasoning-engines delete <reasoning-engine-id> --region europe-west3

gcloud ai custom-jobs list --region europe-west3
gcloud ai custom-jobs create --region europe-west3 --display-name myjob --config config.yaml

gcloud ai hp-tuning-jobs list --region europe-west3
gcloud ai pipeline-jobs list --region europe-west3
```

## Cloud Functions

```bash
gcloud functions deploy myfunction --runtime python312 --trigger-http \
    --entry-point main --region europe-west3 --allow-unauthenticated
gcloud functions list
gcloud functions describe myfunction --region europe-west3
gcloud functions call myfunction --data '{"key":"value"}'
gcloud functions logs read myfunction --region europe-west3
gcloud functions delete myfunction --region europe-west3
```

## GKE (Kubernetes Engine)

```bash
gcloud container clusters list
gcloud container clusters create mycluster --zone europe-west3-a --num-nodes 3
gcloud container clusters get-credentials mycluster --zone europe-west3-a   # configures kubectl
gcloud container clusters delete mycluster --zone europe-west3-a
gcloud container clusters resize mycluster --num-nodes 5 --zone europe-west3-a
gcloud container node-pools list --cluster mycluster --zone europe-west3-a
gcloud container images list
```

## Cloud SQL

```bash
gcloud sql instances list
gcloud sql instances create myinstance --database-version=POSTGRES_15 \
    --tier=db-f1-micro --region europe-west3
gcloud sql instances describe myinstance
gcloud sql instances patch myinstance --memory 4GB
gcloud sql databases create mydb --instance myinstance
gcloud sql users create myuser --instance myinstance --password mypassword
gcloud sql connect myinstance --user myuser
gcloud sql backups list --instance myinstance
gcloud sql export sql myinstance gs://my-bucket/backup.sql --database mydb
```

## Pub/Sub

```bash
gcloud pubsub topics list
gcloud pubsub topics create mytopic
gcloud pubsub topics publish mytopic --message "hello"
gcloud pubsub subscriptions create mysub --topic mytopic
gcloud pubsub subscriptions pull mysub --auto-ack --limit 10
gcloud pubsub subscriptions list
gcloud pubsub topics delete mytopic
```

## Cloud KMS (encryption keys — relevant for CMEK setups)

```bash
gcloud kms keyrings list --location europe-west3
gcloud kms keyrings create my-keyring --location europe-west3
gcloud kms keys list --keyring my-keyring --location europe-west3
gcloud kms keys create my-key --keyring my-keyring --location europe-west3 --purpose encryption
gcloud kms keys add-iam-policy-binding my-key --keyring my-keyring --location europe-west3 \
    --member serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role roles/cloudkms.cryptoKeyEncrypterDecrypter
```

## Logging & Monitoring

```bash
gcloud logging read "severity>=ERROR" --limit 20
gcloud logging read "resource.type=cloud_run_revision" --format json
gcloud logging logs list
gcloud logging sinks list
gcloud logging sinks create mysink bigquery.googleapis.com/projects/my-project/datasets/logs \
    --log-filter="resource.type=cloud_run_revision"

gcloud monitoring dashboards list
gcloud alpha monitoring policies list
```

## Artifact Registry / Container Registry

```bash
gcloud artifacts repositories list
gcloud artifacts repositories create my-repo --repository-format=docker --location europe-west3
gcloud auth configure-docker europe-west3-docker.pkg.dev
docker push europe-west3-docker.pkg.dev/my-project/my-repo/myimage:tag
gcloud artifacts docker images list europe-west3-docker.pkg.dev/my-project/my-repo
```

## Networking (VPC)

```bash
gcloud compute networks list
gcloud compute networks create mynetwork --subnet-mode custom
gcloud compute networks subnets create mysubnet --network mynetwork \
    --range 10.0.0.0/24 --region europe-west3
gcloud compute routers list
gcloud compute vpn-tunnels list
gcloud compute addresses list
```

## Billing & Cost

```bash
gcloud billing accounts list
gcloud billing projects describe my-project
gcloud billing budgets list --billing-account=<account-id>
```

## CLI Productivity Tips

```bash
gcloud <group> <command> --help
gcloud topic filters                    # help on --filter syntax
gcloud topic formats                       # help on --format syntax

gcloud config set core/disable_prompts true          # skip confirmations globally

# --format examples
--format="value(name)"
--format="table(name, status, createTime)"
--format=json

# --filter examples
--filter="status=RUNNING"
--filter="labels.env=prod AND zone:europe*"

gcloud info                            # diagnostics / SDK info
gcloud components list
```
