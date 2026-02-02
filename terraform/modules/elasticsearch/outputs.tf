output "domain_endpoint" {
  value       = aws_opensearch_domain.this.endpoint
  description = "OpenSearch domain endpoint."
}

output "domain_arn" {
  value       = aws_opensearch_domain.this.arn
  description = "OpenSearch domain ARN."
}

output "kibana_endpoint" {
  value       = aws_opensearch_domain.this.dashboard_endpoint
  description = "OpenSearch Dashboards endpoint."
}

output "security_group_id" {
  value       = aws_security_group.opensearch.id
  description = "OpenSearch security group ID."
}
