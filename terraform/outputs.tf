output "vpc_id" {
  value = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "opensearch_endpoint" {
  value = module.opensearch.domain_endpoint
}

output "iot_endpoint" {
  value = module.iot.iot_endpoint
}
