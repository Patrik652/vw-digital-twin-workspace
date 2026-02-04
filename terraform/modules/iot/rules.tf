resource "aws_iot_topic_rule" "telemetry_to_kinesis" {
  name        = "telemetry_to_kinesis_${var.environment}"
  description = "Route telemetry to Kinesis"
  enabled     = true
  sql         = "SELECT * FROM 'dt/cnc/+/telemetry'"
  sql_version = "2016-03-23"

  kinesis {
    role_arn    = aws_iam_role.iot_rules.arn
    stream_name = "${var.project_name}-${var.environment}-telemetry"
  }
}

resource "aws_iot_topic_rule" "alerts_to_sns" {
  name        = "alerts_to_sns_${var.environment}"
  description = "Route critical alerts to SNS"
  enabled     = true
  sql         = "SELECT * FROM 'dt/cnc/+/alerts' WHERE severity = 'critical'"
  sql_version = "2016-03-23"

  sns {
    role_arn   = aws_iam_role.iot_rules.arn
    target_arn = aws_sns_topic.alerts.arn
  }
}

resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-${var.environment}-alerts"
}

resource "aws_iam_role" "iot_rules" {
  name = "${var.project_name}-${var.environment}-iot-rules"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "iot.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "iot_rules" {
  role = aws_iam_role.iot_rules.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["kinesis:PutRecord", "kinesis:PutRecords"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = aws_sns_topic.alerts.arn
      }
    ]
  })
}
