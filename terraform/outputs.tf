output "api_gateway_url" {
  value = aws_apigatewayv2_api.webhook_api.api_endpoint
}


output "dynamodb_table_name" {
  value       = aws_dynamodb_table.media_group_buffer.name
  description = "Name of the DynamoDB table"
}

output "dynamodb_table_arn" {
  value       = aws_dynamodb_table.media_group_buffer.arn
  description = "ARN of the DynamoDB table"
}
