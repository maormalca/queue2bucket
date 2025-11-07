# Random suffix so bucket name is globally unique
resource "random_integer" "rand_suffix" {
  min = 10000
  max = 99999
}

# S3 bucket for processed email data
resource "aws_s3_bucket" "emails_bucket" {
  bucket = "${var.project_name}-emails-${random_integer.rand_suffix.id}"

  tags = {
    Project = var.project_name
  }
}

# SQS queue between API and worker
resource "aws_sqs_queue" "emails_queue" {
  name = "${var.project_name}-queue"

  visibility_timeout_seconds = 60
  message_retention_seconds  = 86400 # 1 day

  tags = {
    Project = var.project_name
  }
}

# SSM parameter for API token validation
resource "aws_ssm_parameter" "api_token" {
  name        = "${var.project_name}-api-token"
  description = "Token for validating API requests"
  type        = "SecureString"
  value       = "dev-secret-2025"

  tags = {
    Project = var.project_name
  }
}

resource "aws_ecr_repository" "queue2bucket" {
  name                 = "queue2bucketrepo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

force_delete = true
  tags = {
    Project = "queue2bucket"
  }
}
