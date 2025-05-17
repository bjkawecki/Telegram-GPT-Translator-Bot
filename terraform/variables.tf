variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-central-1"
}

variable "code_bucket_name" {
  type      = string
  sensitive = true
}

variable "bot_token" {
  description = "Geheimer Token für Telegram Webhook URL"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  type      = string
  sensitive = true
}


variable "bot_name" {
  type    = string
  default = "mirrowchan_bot"
}
