output "iot_endpoint" {
  value       = data.aws_iot_endpoint.this.endpoint_address
  description = "IoT endpoint."
}

output "thing_arn" {
  value       = aws_iot_thing.this.arn
  description = "Thing ARN."
}

output "certificate_arn" {
  value       = aws_iot_certificate.this.arn
  description = "Certificate ARN."
}

output "certificate_pem" {
  value       = aws_iot_certificate.this.certificate_pem
  sensitive   = true
  description = "Certificate PEM."
}

output "private_key" {
  value       = aws_iot_certificate.this.private_key
  sensitive   = true
  description = "Private key."
}
