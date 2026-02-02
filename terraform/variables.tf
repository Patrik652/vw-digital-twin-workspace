variable "environment" {
  type        = string
  description = "Environment name (dev/prod)."
}

variable "region" {
  type        = string
  description = "AWS region."
  default     = "eu-central-1"
}

variable "project_name" {
  type        = string
  description = "Project name."
  default     = "vw-digital-twin"
}

variable "eks_public_endpoint" {
  type        = bool
  description = "Enable EKS public endpoint."
  default     = true
}

variable "eks_node_instance_types" {
  type        = list(string)
  description = "EKS application node types."
  default     = ["t3.large"]
}

variable "elasticsearch_instance_type" {
  type        = string
  description = "OpenSearch instance type."
  default     = "t3.small.search"
}
