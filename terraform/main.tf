provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

module "vpc" {
  source       = "./modules/vpc"
  environment  = var.environment
  project_name = var.project_name
}

module "eks" {
  source             = "./modules/eks"
  environment        = var.environment
  project_name       = var.project_name
  cluster_name       = "${var.project_name}-${var.environment}"
  cluster_version    = "1.28"
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  public_endpoint    = var.eks_public_endpoint
  app_instance_types = var.eks_node_instance_types
}

module "iot" {
  source             = "./modules/iot"
  environment        = var.environment
  project_name       = var.project_name
  secrets_kms_key_id = aws_kms_key.security.arn
}

module "opensearch" {
  source         = "./modules/elasticsearch"
  environment    = var.environment
  project_name   = var.project_name
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  eks_node_sg_id = module.eks.node_security_group_id
  instance_type  = var.elasticsearch_instance_type
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-${var.environment}-data-lake-${data.aws_caller_identity.current.account_id}"

  tags = local.tags
}

resource "aws_ecr_repository" "services" {
  for_each = toset([
    "anomaly-detection",
    "predictive-maintenance",
    "digital-twin-api",
    "alerting-service",
    "data-aggregator",
    "simulator"
  ])

  name                 = "${var.project_name}-${each.key}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.security.arn
  }

  tags = local.tags
}

resource "aws_secretsmanager_secret" "app" {
  name       = "${var.project_name}-${var.environment}-app-secrets"
  kms_key_id = aws_kms_key.security.arn

  tags = local.tags
}

resource "aws_kms_key" "security" {
  description             = "CMK for ECR and Secrets Manager resources"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = local.tags
}

resource "aws_kms_alias" "security" {
  name          = "alias/${var.project_name}-${var.environment}-security"
  target_key_id = aws_kms_key.security.key_id
}
