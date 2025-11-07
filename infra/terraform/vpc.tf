# Create VPC for ECS Fargate using the official VPC module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  # Two availability zones in the chosen region
  azs = [
    "${var.aws_region}a",
    "${var.aws_region}b",
  ]

  # Public subnets (for simplicity in this assignment)
  public_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24",
  ]

  enable_nat_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Project = var.project_name
  }
}
