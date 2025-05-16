#* S3 Bucket für Lambda-Code
resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = var.code_bucket_name
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
        Effect = "Allow",
        Action = [
          "ssm:GetParameter"
        ],
        Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.bot_name}/webhook_token"
      }
    ]
  })
}

# * Lambda IAM Policy Attachment
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# * Lambda Function
resource "aws_lambda_function" "telegram_bot" {
  function_name = "telegram-bot-handler"
  s3_bucket     = aws_s3_bucket.lambda_code_bucket.id
  s3_key        = "code.zip"    # via CI/CD hochgeladen
  handler       = "bot.handler" # Beispiel: bot.py mit def handler(event, context)
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec_role.arn
}

#* API Gateway
resource "aws_apigatewayv2_api" "telegram_api" {
  name          = "telegram-bot-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.telegram_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.telegram_bot.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "webhook_route" {
  api_id    = aws_apigatewayv2_api.telegram_api.id
  route_key = "POST /webhook/{token}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.telegram_api.id
  name        = "$default"
  auto_deploy = true
}


#* Systems Manager Parameter Store
resource "aws_ssm_parameter" "telegram_bot_token" {
  name  = "/${var.bot_name}/telegram_bot_token"
  type  = "SecureString"
  value = var.telegram_bot_token
}

resource "aws_ssm_parameter" "openai_api_key" {
  name  = "/${var.bot_name}/openai_api_key"
  type  = "SecureString"
  value = var.openai_api_key
}
