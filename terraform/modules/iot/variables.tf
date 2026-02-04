variable "environment" {
  type        = string
  description = "Environment name."
}

variable "project_name" {
  type        = string
  description = "Project name."
}

variable "machine_id" {
  type        = string
  description = "Machine ID attribute."
  default     = "CNC-001"
}

variable "location" {
  type        = string
  description = "Machine location."
  default     = "Plant-A"
}

variable "model" {
  type        = string
  description = "Machine model."
  default     = "VMC"
}

variable "secrets_kms_key_id" {
  type        = string
  description = "KMS CMK ARN used to encrypt Secrets Manager secrets."
}
