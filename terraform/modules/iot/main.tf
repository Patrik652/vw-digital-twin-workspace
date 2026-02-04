resource "aws_iot_thing_type" "this" {
  name = "CNCMachine"
}

resource "aws_iot_thing" "this" {
  name            = "cnc-simulator-${var.environment}"
  thing_type_name = aws_iot_thing_type.this.name

  attributes = {
    machine_id = var.machine_id
    location   = var.location
    model      = var.model
  }
}

resource "aws_iot_certificate" "this" {
  active = true
}

resource "aws_secretsmanager_secret" "cert" {
  name       = "${var.project_name}-${var.environment}-iot-cert"
  kms_key_id = var.secrets_kms_key_id
}

resource "aws_secretsmanager_secret_version" "cert" {
  secret_id = aws_secretsmanager_secret.cert.id
  secret_string = jsonencode({
    certificate_pem = aws_iot_certificate.this.certificate_pem
    private_key     = aws_iot_certificate.this.private_key
  })
}

resource "aws_iot_policy" "this" {
  name   = "${var.project_name}-${var.environment}-iot-policy"
  policy = data.aws_iam_policy_document.iot.json
}

resource "aws_iot_policy_attachment" "this" {
  policy = aws_iot_policy.this.name
  target = aws_iot_certificate.this.arn
}

resource "aws_iot_thing_principal_attachment" "this" {
  thing     = aws_iot_thing.this.name
  principal = aws_iot_certificate.this.arn
}

data "aws_iot_endpoint" "this" {
  endpoint_type = "iot:Data-ATS"
}
