#* S3 Bucket für Lambda-Code
resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket        = var.code_bucket_name
  force_destroy = true
}

# * Lambda IAM Role
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# * Lambda IAM Policy
resource "aws_iam_policy" "lambda_policy" {
  name = "lambda-access-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action   = ["ssm:GetParameter", "ssm:GetParameters"],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action   = ["s3:GetObject"],
        Effect   = "Allow",
        Resource = "${aws_s3_bucket.lambda_code_bucket.arn}/*"
      },
      {
        Action = [
          "ssm:GetParameter"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.bot_name}/webhook_token"
      },
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:DeleteItem"
        ],
        Effect   = "Allow",
        Resource = aws_dynamodb_table.media_group_buffer.arn
      }
    ]
  })
}

#* Lambda IAM Policy Attachment
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

#* Lambda Function
resource "aws_lambda_function" "telegram_bot_handler" {
  function_name    = "mirrowchanbot-handler"
  filename         = "../lambda/initial_lambda.zip"                   # Lokale ZIP-Datei
  source_code_hash = filebase64sha256("../lambda/initial_lambda.zip") # wichtig für Updates
  handler          = "bot.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_exec_role.arn
  depends_on       = [aws_iam_role_policy_attachment.lambda_policy_attach]
}
#* Permission getting invoked by API Gateway
resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.telegram_bot_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.webhook_api.execution_arn}/*/*"
}

#* API Gateway
resource "aws_apigatewayv2_api" "webhook_api" {
  name          = "telegram-bot-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.webhook_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.telegram_bot_handler.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "webhook_route" {
  api_id    = aws_apigatewayv2_api.webhook_api.id
  route_key = "POST /webhook/{token}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.webhook_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_ssm_parameter" "bot_token" {
  name      = "/${var.bot_name}/bot_token"
  type      = "SecureString"
  value     = var.bot_token
  overwrite = true
}

resource "aws_ssm_parameter" "openai_api_key" {
  name  = "/${var.bot_name}/openai_api_key"
  type  = "SecureString"
  value = var.openai_api_key
}

resource "aws_ssm_parameter" "api_gateway_url" {
  name  = "/${var.bot_name}/api_gateway_url"
  type  = "String"
  value = aws_apigatewayv2_api.webhook_api.api_endpoint
}

#* LOG GROUP
resource "aws_cloudwatch_log_group" "http_api_logs" {
  name              = "/aws/http-api/${aws_apigatewayv2_api.webhook_api.id}/access-logs"
  retention_in_days = 3
}

resource "aws_iam_role" "api_gw_logging_role" {
  name = "APIGatewayCloudWatchLogsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "apigateway.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "api_gw_logging_policy" {
  name = "APIGatewayCloudWatchLogsPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "${aws_cloudwatch_log_group.http_api_logs.arn}:*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_logging_policy" {
  role       = aws_iam_role.api_gw_logging_role.name
  policy_arn = aws_iam_policy.api_gw_logging_policy.arn
}

#* DynamoDB Table
resource "aws_dynamodb_table" "media_group_buffer" {
  name         = "MediaGroupBuffer"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "media_group_id"
  range_key = "message_id"

  attribute {
    name = "media_group_id"
    type = "S"
  }

  attribute {
    name = "message_id"
    type = "N"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  tags = {
    Environment = "dev"
    Project     = "TelegramBot"
  }
}
