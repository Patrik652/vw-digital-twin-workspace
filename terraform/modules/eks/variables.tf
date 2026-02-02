variable "environment" {
  type        = string
  description = "Environment name."
}

variable "project_name" {
  type        = string
  description = "Project name."
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name."
}

variable "cluster_version" {
  type        = string
  description = "Kubernetes version."
  default     = "1.28"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for EKS."
}

variable "public_endpoint" {
  type        = bool
  description = "Enable public endpoint access."
  default     = true
}

variable "system_instance_types" {
  type        = list(string)
  description = "Instance types for system nodes."
  default     = ["t3.medium"]
}

variable "app_instance_types" {
  type        = list(string)
  description = "Instance types for application nodes."
  default     = ["t3.large"]
}
