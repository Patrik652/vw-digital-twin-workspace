variable "environment" {
  type        = string
  description = "Environment name (dev/prod)."
}

variable "project_name" {
  type        = string
  description = "Project name for tagging."
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block."
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "Public subnet CIDRs."
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "Private subnet CIDRs."
  default     = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}

variable "azs" {
  type        = list(string)
  description = "Availability zones."
  default     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
}

variable "single_nat_gateway" {
  type        = bool
  description = "Use a single NAT gateway for cost savings."
  default     = true
}
