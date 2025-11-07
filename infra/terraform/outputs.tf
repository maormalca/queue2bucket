# Data-layer outputs

output "s3_bucket_name" {
  value       = aws_s3_bucket.emails_bucket.bucket
  description = "Bucket where processed emails are stored"
}

output "sqs_queue_url" {
  value       = aws_sqs_queue.emails_queue.id
  description = "SQS queue URL for messages"
}

output "api_token_param_name" {
  value       = aws_ssm_parameter.api_token.name
  description = "SSM parameter name that holds the API token"
}


output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.queue2bucket.repository_url
}

output "ecr_repository_name" {
  description = "ECR repository name"
  value       = aws_ecr_repository.queue2bucket.name
}

output "api_alb_dns_name" {
  description = "Public DNS of the API load balancer"
  value       = aws_lb.api_alb.dns_name
}

#output "aws_ecs_cluster_name" {
#  description = "Public DNS of the API load balancer"
#  value       = aws_ecs_cluster.name
#}