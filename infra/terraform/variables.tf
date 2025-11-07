variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "queue2bucket"
}

