output "api_gateway_invoke_url" {
  value = aws_apigatewayv2_api.telegram_api.api_endpoint
}
