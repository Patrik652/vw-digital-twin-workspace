# Starter Code Templates

This file contains copy-paste ready starter code to accelerate development.

---

## 1. CNC Simulator - Main Entry Point

**File:** `simulator/src/main.py`

```python
#!/usr/bin/env python3
"""
CNC Machine Digital Twin Simulator
Main entry point for the simulation.

This simulator generates realistic CNC machine telemetry data
for demonstration of Industrial IoT capabilities.

Author: [Your Name]
Project: VW Digital Twin Demo
"""

import asyncio
import signal
import logging
from typing import Optional

from .cnc_machine import CNCMachine
from .mqtt_publisher import MQTTPublisher
from .config import Config
from .failure_modes import FailureModeManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimulatorApp:
    """Main application class for the CNC simulator."""
    
    def __init__(self):
        self.config = Config()
        self.machine: Optional[CNCMachine] = None
        self.publisher: Optional[MQTTPublisher] = None
        self.failure_manager: Optional[FailureModeManager] = None
        self._running = False
        
    async def start(self):
        """Initialize and start the simulator."""
        logger.info("Starting CNC Machine Simulator...")
        
        # Initialize MQTT publisher
        self.publisher = MQTTPublisher(
            broker=self.config.mqtt_broker,
            port=self.config.mqtt_port,
            use_tls=self.config.mqtt_use_tls,
            cert_path=self.config.mqtt_cert_path,
            key_path=self.config.mqtt_key_path,
            ca_path=self.config.mqtt_ca_path
        )
        await self.publisher.connect()
        
        # Initialize CNC machine
        self.machine = CNCMachine(
            machine_id=self.config.machine_id,
            publisher=self.publisher
        )
        
        # Initialize failure mode manager
        self.failure_manager = FailureModeManager(self.machine)
        
        # Start the simulation loop
        self._running = True
        await self._simulation_loop()
        
    async def _simulation_loop(self):
        """Main simulation loop."""
        logger.info(f"Simulation started for machine: {self.config.machine_id}")
        
        while self._running:
            try:
                # Update machine state
                self.machine.update()
                
                # Apply any active failure modes
                self.failure_manager.apply_effects()
                
                # Publish telemetry
                telemetry = self.machine.get_telemetry()
                await self.publisher.publish(
                    topic=f"dt/cnc/{self.config.machine_id}/telemetry",
                    payload=telemetry
                )
                
                # Wait for next cycle
                await asyncio.sleep(self.config.cycle_time_ms / 1000)
                
            except Exception as e:
                logger.error(f"Error in simulation loop: {e}")
                await asyncio.sleep(1)  # Back off on error
                
    async def stop(self):
        """Gracefully stop the simulator."""
        logger.info("Stopping simulator...")
        self._running = False
        
        if self.publisher:
            await self.publisher.disconnect()
            
        logger.info("Simulator stopped")


async def main():
    """Main entry point."""
    app = SimulatorApp()
    
    # Handle shutdown signals
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(app.stop()))
    
    try:
        await app.start()
    except KeyboardInterrupt:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2. Configuration Class

**File:** `simulator/src/config.py`

```python
"""
Configuration management for the CNC simulator.
Loads settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration settings for the simulator."""
    
    # Machine settings
    machine_id: str = os.getenv("MACHINE_ID", "CNC-001")
    machine_model: str = os.getenv("MACHINE_MODEL", "VMC-850")
    
    # Simulation settings
    cycle_time_ms: int = int(os.getenv("CYCLE_TIME_MS", "100"))
    
    # MQTT settings
    mqtt_broker: str = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port: int = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_use_tls: bool = os.getenv("MQTT_USE_TLS", "false").lower() == "true"
    mqtt_cert_path: Optional[str] = os.getenv("MQTT_CERT_PATH")
    mqtt_key_path: Optional[str] = os.getenv("MQTT_KEY_PATH")
    mqtt_ca_path: Optional[str] = os.getenv("MQTT_CA_PATH")
    
    # Spindle settings
    spindle_max_rpm: int = int(os.getenv("SPINDLE_MAX_RPM", "24000"))
    spindle_power_kw: float = float(os.getenv("SPINDLE_POWER_KW", "15.0"))
    
    # Axis settings (travel in mm)
    x_axis_travel: float = float(os.getenv("X_AXIS_TRAVEL", "850"))
    y_axis_travel: float = float(os.getenv("Y_AXIS_TRAVEL", "500"))
    z_axis_travel: float = float(os.getenv("Z_AXIS_TRAVEL", "500"))
    
    # Feed rate settings (mm/min)
    max_feed_rate: float = float(os.getenv("MAX_FEED_RATE", "15000"))
    rapid_feed_rate: float = float(os.getenv("RAPID_FEED_RATE", "30000"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.mqtt_use_tls:
            if not all([self.mqtt_cert_path, self.mqtt_key_path, self.mqtt_ca_path]):
                raise ValueError(
                    "TLS enabled but certificate paths not provided. "
                    "Set MQTT_CERT_PATH, MQTT_KEY_PATH, and MQTT_CA_PATH"
                )
```

---

## 3. Telemetry Data Model

**File:** `simulator/src/models.py`

```python
"""
Data models for CNC machine telemetry.
Uses Pydantic for validation and JSON serialization.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class SpindleData(BaseModel):
    """Spindle telemetry data."""
    rpm: int = Field(ge=0, le=30000, description="Spindle RPM")
    load_percent: float = Field(ge=0, le=100, description="Spindle load percentage")
    temperature_c: float = Field(ge=-10, le=150, description="Spindle temperature in Celsius")
    vibration_mm_s: float = Field(ge=0, le=50, description="Vibration in mm/s")


class AxisData(BaseModel):
    """Single axis telemetry data."""
    position_mm: float = Field(description="Current position in mm")
    velocity_mm_min: float = Field(ge=0, description="Current velocity in mm/min")


class AxesData(BaseModel):
    """All axes telemetry data."""
    x: AxisData
    y: AxisData
    z: AxisData


class ToolData(BaseModel):
    """Tool telemetry data."""
    id: str = Field(pattern=r"T\d{1,2}", description="Tool ID (T01-T99)")
    type: Literal["end_mill", "drill", "tap", "boring_bar", "face_mill"]
    diameter_mm: float = Field(gt=0, description="Tool diameter in mm")
    wear_percent: float = Field(ge=0, le=100, description="Tool wear percentage")
    runtime_minutes: float = Field(ge=0, description="Total runtime in minutes")


class CoolantData(BaseModel):
    """Coolant system telemetry data."""
    flow_rate_lpm: float = Field(ge=0, le=50, description="Flow rate in liters per minute")
    temperature_c: float = Field(ge=-10, le=80, description="Coolant temperature in Celsius")
    pressure_bar: float = Field(ge=0, le=20, description="Coolant pressure in bar")


class PowerData(BaseModel):
    """Power consumption telemetry data."""
    total_kw: float = Field(ge=0, description="Total power consumption in kW")
    spindle_kw: float = Field(ge=0, description="Spindle power consumption in kW")
    servo_kw: float = Field(ge=0, description="Servo motors power consumption in kW")


class MachineStatus(BaseModel):
    """Machine status data."""
    mode: Literal["AUTO", "MDI", "JOG", "REF", "IDLE", "ALARM"]
    program: Optional[str] = Field(pattern=r"O\d{4}", description="Program number")
    block: Optional[str] = Field(pattern=r"N\d{4}", description="Current block number")
    cycle_time_s: int = Field(ge=0, description="Current cycle time in seconds")


class MachineTelemetry(BaseModel):
    """Complete machine telemetry payload."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    machine_id: str
    spindle: SpindleData
    axes: AxesData
    tool: ToolData
    coolant: CoolantData
    power: PowerData
    status: MachineStatus
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }
```

---

## 4. Terraform Main Module

**File:** `terraform/main.tf`

```hcl
# -----------------------------------------------------------------------------
# VW Digital Twin Demo - Main Terraform Configuration
# -----------------------------------------------------------------------------
# This configuration creates the complete AWS infrastructure for the
# CNC Machine Digital Twin demonstration project.
# -----------------------------------------------------------------------------

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
  
  backend "s3" {
    # Backend configuration loaded from backend.hcl
  }
}

# -----------------------------------------------------------------------------
# Provider Configuration
# -----------------------------------------------------------------------------

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = local.common_tags
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    }
  }
}

# -----------------------------------------------------------------------------
# Local Values
# -----------------------------------------------------------------------------

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Repository  = "vw-digital-twin-demo"
  }
}

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

# -----------------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------------

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  name_prefix         = local.name_prefix
  vpc_cidr            = var.vpc_cidr
  availability_zones  = slice(data.aws_availability_zones.available.names, 0, 3)
  
  tags = local.common_tags
}

# EKS Module
module "eks" {
  source = "./modules/eks"
  
  name_prefix        = local.name_prefix
  kubernetes_version = var.kubernetes_version
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  node_instance_types = var.eks_node_instance_types
  node_desired_size   = var.eks_node_desired_size
  node_min_size       = var.eks_node_min_size
  node_max_size       = var.eks_node_max_size
  
  tags = local.common_tags
}

# IoT Core Module
module "iot" {
  source = "./modules/iot"
  
  name_prefix = local.name_prefix
  machine_id  = var.machine_id
  
  tags = local.common_tags
}

# Elasticsearch Module
module "elasticsearch" {
  source = "./modules/elasticsearch"
  
  name_prefix = local.name_prefix
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  instance_type  = var.elasticsearch_instance_type
  instance_count = var.elasticsearch_instance_count
  
  allowed_security_groups = [module.eks.node_security_group_id]
  
  tags = local.common_tags
}

# -----------------------------------------------------------------------------
# Additional Resources
# -----------------------------------------------------------------------------

# S3 Bucket for Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${local.name_prefix}-data-lake"
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# ECR Repositories
resource "aws_ecr_repository" "services" {
  for_each = toset([
    "anomaly-detection",
    "predictive-maintenance",
    "alerting-service",
    "digital-twin-api",
    "data-aggregator",
    "cnc-simulator"
  ])
  
  name                 = "${local.name_prefix}/${each.key}"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "iot_endpoint" {
  description = "AWS IoT endpoint"
  value       = module.iot.endpoint
}

output "elasticsearch_endpoint" {
  description = "Elasticsearch endpoint"
  value       = module.elasticsearch.endpoint
}

output "ecr_repositories" {
  description = "ECR repository URLs"
  value       = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}
```

---

## 5. Helm Chart values.yaml

**File:** `kubernetes/charts/digital-twin/values.yaml`

```yaml
# Default values for digital-twin umbrella chart
# This is a YAML-formatted file.

global:
  # Environment name (dev, staging, prod)
  environment: dev
  
  # AWS region
  region: eu-central-1
  
  # Image pull policy
  imagePullPolicy: IfNotPresent
  
  # Service account settings
  serviceAccount:
    create: true
    annotations: {}

# Anomaly Detection Service
anomaly-detection:
  enabled: true
  replicaCount: 2
  
  image:
    repository: ""  # Set via CI/CD
    tag: "latest"
  
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
    requests:
      cpu: "100m"
      memory: "256Mi"
  
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilization: 70
  
  env:
    - name: LOG_LEVEL
      value: "INFO"
    - name: ELASTICSEARCH_URL
      valueFrom:
        secretKeyRef:
          name: elasticsearch-credentials
          key: url
  
  probes:
    liveness:
      path: /health
      port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readiness:
      path: /ready
      port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5

# Predictive Maintenance Service
predictive-maintenance:
  enabled: true
  replicaCount: 2
  
  image:
    repository: ""
    tag: "latest"
  
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "512Mi"
  
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilization: 70

# Digital Twin API
digital-twin-api:
  enabled: true
  replicaCount: 3
  
  image:
    repository: ""
    tag: "latest"
  
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
    requests:
      cpu: "100m"
      memory: "256Mi"
  
  service:
    type: ClusterIP
    port: 80
    targetPort: 8080
  
  ingress:
    enabled: true
    className: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
      alb.ingress.kubernetes.io/target-type: ip
    hosts:
      - host: api.digital-twin.example.com
        paths:
          - path: /
            pathType: Prefix

# Alerting Service
alerting-service:
  enabled: true
  replicaCount: 2
  
  image:
    repository: ""
    tag: "latest"
  
  resources:
    limits:
      cpu: "200m"
      memory: "256Mi"
    requests:
      cpu: "50m"
      memory: "128Mi"
  
  env:
    - name: SLACK_WEBHOOK_URL
      valueFrom:
        secretKeyRef:
          name: alerting-secrets
          key: slack-webhook-url

# Data Aggregator
data-aggregator:
  enabled: true
  replicaCount: 2
  
  image:
    repository: ""
    tag: "latest"
  
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
    requests:
      cpu: "100m"
      memory: "256Mi"

# Shared settings
podDisruptionBudget:
  enabled: true
  minAvailable: 1

networkPolicy:
  enabled: true
  
metrics:
  enabled: true
  serviceMonitor:
    enabled: true
```

---

## 6. GitHub Actions CI Workflow

**File:** `.github/workflows/ci.yaml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"
  TERRAFORM_VERSION: "1.5.7"

jobs:
  # Lint and format checks
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install linting tools
        run: pip install flake8 black isort
      
      - name: Run flake8
        run: flake8 simulator/ services/
      
      - name: Run black
        run: black --check simulator/ services/
      
      - name: Run isort
        run: isort --check-only simulator/ services/
      
      - name: Terraform Format
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TERRAFORM_VERSION }}
      
      - name: Terraform fmt
        run: terraform fmt -check -recursive terraform/
      
      - name: Helm Lint
        run: |
          helm lint kubernetes/charts/digital-twin/
          helm lint kubernetes/charts/digital-twin/charts/*/

  # Run tests
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install simulator dependencies
        run: |
          cd simulator
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run simulator tests
        run: |
          cd simulator
          pytest tests/ -v --cov=src --cov-report=xml --cov-fail-under=80
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: simulator/coverage.xml
          fail_ci_if_error: true

  # Security scanning
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          soft_fail: true

  # Build Docker images
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    if: github.ref == 'refs/heads/main'
    strategy:
      matrix:
        service:
          - simulator
          - anomaly-detection
          - predictive-maintenance
          - alerting-service
          - digital-twin-api
          - data-aggregator
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-central-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2
      
      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          if [ "${{ matrix.service }}" == "simulator" ]; then
            cd simulator
          else
            cd services/${{ matrix.service }}
          fi
          
          docker build -t $ECR_REGISTRY/vw-digital-twin-dev/${{ matrix.service }}:$IMAGE_TAG .
          docker push $ECR_REGISTRY/vw-digital-twin-dev/${{ matrix.service }}:$IMAGE_TAG
          
          # Also tag as latest
          docker tag $ECR_REGISTRY/vw-digital-twin-dev/${{ matrix.service }}:$IMAGE_TAG \
                     $ECR_REGISTRY/vw-digital-twin-dev/${{ matrix.service }}:latest
          docker push $ECR_REGISTRY/vw-digital-twin-dev/${{ matrix.service }}:latest
```

---

## 7. Docker Compose for Local Development

**File:** `docker-compose.yaml`

```yaml
version: '3.8'

services:
  # MQTT Broker (Mosquitto)
  mqtt:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./docker/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto-data:/mosquitto/data
      - mosquitto-log:/mosquitto/log
    networks:
      - digital-twin

  # Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - digital-twin
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -vq '\"status\":\"red\"'"]
      interval: 10s
      timeout: 10s
      retries: 5

  # Kibana
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - digital-twin

  # CNC Simulator
  simulator:
    build:
      context: ./simulator
      dockerfile: Dockerfile
    environment:
      - MACHINE_ID=CNC-001
      - MQTT_BROKER=mqtt
      - MQTT_PORT=1883
      - LOG_LEVEL=DEBUG
    depends_on:
      - mqtt
    networks:
      - digital-twin

  # Redis (for caching)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - digital-twin

  # PostgreSQL (for metadata)
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=digitaltwin
      - POSTGRES_PASSWORD=digitaltwin
      - POSTGRES_DB=digitaltwin
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - digital-twin

networks:
  digital-twin:
    driver: bridge

volumes:
  mosquitto-data:
  mosquitto-log:
  elasticsearch-data:
  postgres-data:
```

---

## 8. Requirements Files

**File:** `simulator/requirements.txt`

```
# Core dependencies
paho-mqtt>=1.6.1
pydantic>=2.5.0
python-dotenv>=1.0.0

# Async support
aiofiles>=23.2.1
aiomqtt>=1.2.1

# Data processing
numpy>=1.26.0
scipy>=1.11.0

# API (if running standalone)
fastapi>=0.104.0
uvicorn>=0.24.0

# Logging
structlog>=23.2.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Development
black>=23.11.0
flake8>=6.1.0
isort>=5.12.0
mypy>=1.7.0
```

---

*These starter files provide a solid foundation to begin development immediately. Copy-paste into your project and customize as needed.*
