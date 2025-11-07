# Queue2Bucket – Email Processing System

Queue2Bucket is a cloud-native system designed to process and persist email data in AWS using a fully automated, containerized workflow.  
It follows a simple yet robust microservices architecture, leveraging AWS ECS Fargate, SQS, and S3 — all provisioned via Terraform.

---

## Architecture Overview

The system is composed of two Python-based microservices:

### Service 1 – API (Flask REST API)
- Receives POST requests through an Application Load Balancer (ALB)
- Validates an access token stored in AWS SSM Parameter Store
- Ensures the payload structure contains all required fields:
  - `email_subject`, `email_sender`, `email_timestream`, `email_content`
- Publishes validated messages to an AWS SQS queue

### Service 2 – S3 Uploader (Background Worker)
- Continuously polls the SQS queue for messages (every `10s` by default)
- Uploads each message as a JSON file into an S3 bucket
- Deletes messages from SQS upon successful upload
- Designed to run indefinitely within an ECS Fargate task

### AWS Infrastructure
Provisioned entirely via Terraform, including:
- ECS Fargate cluster (with 2 services)
- Application Load Balancer for external traffic
- SQS Queue for message passing
- S3 Bucket for persistent storage
- ECR Repository for Docker images
- SSM Parameter Store for secrets management
- VPC with public subnets and security groups

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Language | Python 3.9 |
| Frameworks | Flask, boto3 |
| Containerization | Docker |
| Orchestration | AWS ECS Fargate |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Cloud Provider | AWS (us-east-2) |

---

## CI/CD Workflows

GitHub Actions automates the full build and deployment cycle:

- **CI – Build & Push Docker Images**  
  Builds and pushes Docker images to ECR on every commit.
  
- **CD – Deploy to ECS**  
  Updates ECS services with the selected image version.

- **Terraform Apply**  
  Applies infrastructure changes when `.tf` files are modified.

- **System Test (Bonus)**  
  Runs an end-to-end test validating SQS → S3 flow.

---

## Key Highlights
Fully automated IaC deployment via Terraform

Token-based API authentication using AWS SSM Parameter Store

Event-driven microservices with SQS → S3 workflow

Containerized deployment via AWS ECS Fargate

CI/CD automation through GitHub Actions