variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "ap-southeast-2"
}

variable "bucket_name" {
  type        = string
  description = "The existing S3 bucket name"
}

variable "discord_webhook_url" {
  type        = string
  description = "Discord webhook URL"
  sensitive   = true
}