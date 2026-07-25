---
layout: default
title: "Multi-Cloud Cost Optimization Cheatsheet"
---

# Multi-Cloud Cost Optimization Cheatsheet

## AWS Cost Optimization

- **S3 Storage Tier Lifecycle Policies:** Move raw bronze-layer datasets to Glacier Flexible or Deep Archive after 30 to 90 days.
- **Compute Savings Plans & Reserved Instances (RIs):** Commit to a 1-year or 3-year term for predictable EC2/RDS/Fargate usage to save up to 72% over On-Demand rates.
- **AWS Graviton Processors:** Migrate EC2, RDS, and Lambda functions from x86 to Graviton (ARM-based) instances to achieve up to 40% better price-performance.
- **Auto-Scaling Group Dynamic Policies:** Configure scaling based on target tracking (e.g., maintain average CPU at 60%) to prevent over-provisioning during off-peak hours.
- **Identify Idle Resources:** Delete unattached Elastic IPs, terminate idle EC2 instances (CPU < 5%), and clean up orphaned EBS volumes.

---

## Azure Cost Optimization

- **Azure Hybrid Benefit (AHUB):** Reuse on-premises Windows Server and SQL Server licenses on Azure VMs to save up to 85% compared to standard pay-as-you-go rates.
- **Azure Spot VMs:** Utilize unused Azure compute capacity for fault-tolerant, batch, or development workloads at up to a 90% discount (with a 30-second eviction notice).
- **Blob Storage Archive Tier:** Use lifecycle management rules to transition cold database backups to the Archive tier.
- **Autoscale with Azure Virtual Machine Scale Sets (VMSS):** Automatically adjust the number of VM instances running your application based on load.

---

## GCP Cost Optimization

- **Committed Use Discounts (CUDs):** Secure major savings (up to 70%) on VM cores and RAM by committing to a 1-year or 3-year plan.
- **Sustained Use Discounts (SUDs):** Automatically receive incremental discounts (up to 30%) on Compute Engine VMs that run for a significant portion of a billing month.
- **GCS Autoclass:** Enable Autoclass on buckets to let Google Cloud automatically transition objects to colder, cheaper storage tiers (Nearline, Coldline, Archive) based on access patterns.
- **GKE Autopilot:** Let GCP manage cluster sizing, node provisioning, and bin-packing. You pay only for the CPU, memory, and storage requested by your active pods, eliminating worker node waste.
