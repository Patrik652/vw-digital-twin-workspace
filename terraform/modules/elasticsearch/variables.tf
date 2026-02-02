variable "environment" {
  type        = string
  description = "Environment name."
}

variable "project_name" {
  type        = string
  description = "Project name."
}

variable "vpc_id" {
  type        = string
  description = "VPC ID."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs."
}

variable "eks_node_sg_id" {
  type        = string
  description = "EKS node security group ID."
}

variable "instance_type" {
  type        = string
  description = "OpenSearch instance type."
  default     = "t3.small.search"
}

variable "instance_count" {
  type        = number
  description = "Number of OpenSearch instances."
  default     = 2
}
