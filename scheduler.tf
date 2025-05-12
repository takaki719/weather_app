terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

# ---- Lambda ----
resource "aws_iam_role" "lambda_exec" {
  name = "weather_bot_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals { type = "Service", identifiers = ["lambda.amazonaws.com"] }
  }
}

resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "ssm_read" {
  name   = "weather_bot_ssm_read"
  policy = data.aws_iam_policy_document.ssm_read.json
}

data "aws_iam_policy_document" "ssm_read" {
  statement {
    actions   = ["ssm:GetParameter"]
    resources = ["arn:aws:ssm:ap-northeast-1:*:parameter/LINE_ACCESS_TOKEN",
                 "arn:aws:ssm:ap-northeast-1:*:parameter/OWM_API_KEY"]
  }
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.ssm_read.arn
}

resource "aws_lambda_function" "weather" {
  function_name = "weather-bot"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn

  filename         = "dist/weather.zip"   # zip created by CI/CD
  source_code_hash = filebase64sha256("dist/weather.zip")

  environment {
    variables = {
      TZ  = "Asia/Tokyo"
      LAT = "35.6812"
      LON = "139.7671"
    }
  }
}

# ---- EventBridge schedule (morning/night) ----
resource "aws_cloudwatch_event_rule" "morning" {
  name                = "weather_morning"
  schedule_expression = "cron(0 22 * * ? *)"   # UTC22 → JST7
}

resource "aws_cloudwatch_event_rule" "night" {
  name                = "weather_night"
  schedule_expression = "cron(0 12 * * ? *)"   # UTC12 → JST21
}

resource "aws_cloudwatch_event_target" "tg_morning" {
  rule = aws_cloudwatch_event_rule.morning.name
  arn  = aws_lambda_function.weather.arn
  input = jsonencode({ target_day = "today" })
}

resource "aws_cloudwatch_event_target" "tg_night" {
  rule = aws_cloudwatch_event_rule.night.name
  arn  = aws_lambda_function.weather.arn
  input = jsonencode({ target_day = "tomorrow" })
}

resource "aws_lambda_permission" "allow_events" {
  statement_id  = "AllowExecutionFromEvents"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather.function_name
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.morning.arn}"
}
