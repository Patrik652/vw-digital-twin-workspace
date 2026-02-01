# AI Agent Prompts - CNC Digital Twin Project

This document contains ready-to-use prompts for AI coding agents (Codex, Claude Code) to build the VW Digital Twin project.

---

## 🎯 STRATEGY: Which Agent for What?

| Task Type | Recommended Agent | Reason |
|-----------|------------------|--------|
| CNC Simulator (Python) | **Codex** | Complex algorithms, domain logic |
| Terraform Infrastructure | **Claude Code** | Better at IaC patterns |
| Kubernetes/Helm | **Either** | Both handle well |
| CI/CD Pipelines | **Claude Code** | Better YAML understanding |
| Python Microservices | **Codex** | Faster at Python |
| Documentation | **Claude Code** | Better at writing |
| Integration/Debugging | **Claude Code** | Better context handling |

---

## 📋 MASTER PROMPT (Give This First)

Copy this to both agents at the start of each session:

```
You are building a demonstration project for a Volkswagen Group Services job application. 
The position is Cloud Platform Engineer with focus on automation.

PROJECT CONTEXT:
- This is a CNC Machine Digital Twin that simulates industrial IoT
- The candidate has 10+ years of CNC programming experience - use realistic machine parameters
- Must use VW's exact tech stack: AWS, EKS, Terraform, Ansible, ELK, Concourse CI
- Project must demonstrate both cloud skills AND manufacturing domain knowledge

QUALITY STANDARDS:
- Production-grade code with proper error handling
- Comprehensive logging
- Unit tests for critical functions
- Clear documentation and comments
- Follow industry best practices

WORKING DIRECTORY: Use the following structure:
vw-digital-twin-demo/
├── simulator/
├── services/
├── terraform/
├── kubernetes/
├── ansible/
├── ci-cd/
└── monitoring/

Always ask for clarification if requirements are unclear.
Start each file with a brief comment explaining its purpose.
```

---

## 🔧 PHASE 1: CNC MACHINE SIMULATOR

### Prompt 1.1: Core Simulator Structure

```
Create a Python CNC machine simulator with the following specifications:

DIRECTORY: simulator/

FILES TO CREATE:
1. simulator/src/cnc_machine.py - Main machine class
2. simulator/src/spindle.py - Spindle dynamics simulation
3. simulator/src/axes.py - X, Y, Z axis simulation
4. simulator/src/tool_manager.py - Tool wear and management
5. simulator/src/gcode_parser.py - G-code interpreter
6. simulator/src/physics_engine.py - Realistic physics calculations
7. simulator/src/mqtt_publisher.py - IoT data publishing
8. simulator/src/config.py - Configuration management
9. simulator/requirements.txt - Dependencies
10. simulator/Dockerfile - Container image

TECHNICAL REQUIREMENTS:

CNCMachine class should:
- Initialize with machine_id, mqtt_broker configuration
- Have start(), stop(), pause(), resume() methods
- Run simulation loop at configurable frequency (default 100ms)
- Generate telemetry data matching this schema:

{
  "timestamp": "ISO8601",
  "machine_id": "string",
  "spindle": {
    "rpm": 0-24000,
    "load_percent": 0-100,
    "temperature_c": 20-80,
    "vibration_mm_s": 0-10
  },
  "axes": {
    "x": {"position_mm": float, "velocity_mm_min": float},
    "y": {"position_mm": float, "velocity_mm_min": float},
    "z": {"position_mm": float, "velocity_mm_min": float}
  },
  "tool": {
    "id": "T01-T99",
    "type": "end_mill|drill|tap|boring_bar",
    "diameter_mm": float,
    "wear_percent": 0-100,
    "runtime_minutes": float
  },
  "coolant": {
    "flow_rate_lpm": 0-20,
    "temperature_c": 15-35,
    "pressure_bar": 0-10
  },
  "power": {
    "total_kw": float,
    "spindle_kw": float,
    "servo_kw": float
  },
  "status": {
    "mode": "AUTO|MDI|JOG|REF",
    "program": "O0001-O9999",
    "block": "N0001-N9999",
    "cycle_time_s": int
  }
}

SPINDLE PHYSICS:
- Model thermal expansion (coefficient: 11.7e-6 /°C for steel)
- Calculate bearing frequencies: BPFO, BPFI, BSF, FTF
- Power consumption: P = (2π × RPM × Torque) / 60000
- Vibration increases with bearing wear (use exponential model)

TOOL WEAR MODEL:
- Use Taylor's tool life equation: VT^n = C
- Where V = cutting speed, T = tool life, n = 0.2-0.3 for carbide
- Wear rate depends on: material hardness, cutting speed, feed rate

Include realistic default values based on actual CNC machining parameters.
Add docstrings explaining the physics behind each calculation.
```

### Prompt 1.2: Failure Mode Injection

```
Extend the CNC simulator with failure mode injection capabilities.

ADD TO: simulator/src/failure_modes.py

FAILURE MODES TO IMPLEMENT:

1. TOOL_WEAR_ACCELERATED
   - Increases tool wear rate by configurable multiplier
   - Symptoms: increased cutting forces, surface finish degradation
   - Telemetry changes: spindle load increases, vibration increases

2. SPINDLE_BEARING_DEGRADATION
   - Simulates progressive bearing wear
   - Symptoms: increased vibration at specific frequencies (BPFO/BPFI)
   - Telemetry changes: vibration_mm_s increases, temperature increases

3. COOLANT_SYSTEM_FAILURE
   - Simulates pump degradation or blockage
   - Symptoms: reduced flow, increased temperatures
   - Telemetry changes: flow_rate drops, spindle_temp increases

4. THERMAL_DRIFT
   - Simulates thermal expansion affecting accuracy
   - Symptoms: positional errors over time
   - Telemetry changes: position deviation from programmed

5. AXIS_BACKLASH
   - Simulates mechanical wear in ball screws
   - Symptoms: positioning errors on direction changes
   - Telemetry changes: position oscillation on reversal

IMPLEMENTATION:
- Create FailureMode base class with inject(), remove(), get_impact() methods
- Each failure mode should be injectable at runtime via API
- Failures should be gradual (not instant) with configurable progression rate
- Add logging for all failure events

CREATE API ENDPOINTS (add to main.py):
POST /failures/inject - Inject a failure mode
DELETE /failures/{failure_id} - Remove a failure
GET /failures - List active failures

Include unit tests for each failure mode.
```

### Prompt 1.3: G-code Parser

```
Create a G-code parser for the CNC simulator.

FILE: simulator/src/gcode_parser.py

SUPPORTED G-CODES:
G00 - Rapid positioning
G01 - Linear interpolation
G02 - Circular interpolation CW
G03 - Circular interpolation CCW
G17 - XY plane selection
G18 - XZ plane selection
G19 - YZ plane selection
G20 - Inch mode
G21 - Metric mode
G28 - Return to reference
G40 - Cutter compensation cancel
G41 - Cutter compensation left
G42 - Cutter compensation right
G43 - Tool length compensation +
G49 - Tool length compensation cancel
G54-G59 - Work coordinate systems
G90 - Absolute positioning
G91 - Incremental positioning
G94 - Feed per minute
G95 - Feed per revolution

SUPPORTED M-CODES:
M00 - Program stop
M01 - Optional stop
M02 - End of program
M03 - Spindle CW
M04 - Spindle CCW
M05 - Spindle stop
M06 - Tool change
M08 - Coolant on
M09 - Coolant off
M30 - End program, reset

PARSER REQUIREMENTS:
- Parse standard FANUC-style G-code
- Handle block numbers (N0010, N0020, etc.)
- Parse comments in parentheses
- Extract feed rate (F), spindle speed (S), tool number (T)
- Calculate motion duration based on distance and feed rate
- Return structured motion commands for the simulator

OUTPUT FORMAT:
class GCodeCommand:
    block_number: int
    g_codes: List[int]
    m_codes: List[int]
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
    f: Optional[float]  # Feed rate
    s: Optional[float]  # Spindle speed
    t: Optional[int]    # Tool number
    i: Optional[float]  # Arc center X
    j: Optional[float]  # Arc center Y
    k: Optional[float]  # Arc center Z
    comment: Optional[str]

Include sample G-code programs for testing:
1. Simple square pocket
2. Circular interpolation test
3. Tool change sequence
```

---

## 🏗️ PHASE 2: TERRAFORM INFRASTRUCTURE

### Prompt 2.1: VPC and Networking

```
Create Terraform configuration for AWS VPC and networking.

DIRECTORY: terraform/modules/vpc/

FILES:
- main.tf
- variables.tf
- outputs.tf

REQUIREMENTS:
- VPC CIDR: 10.0.0.0/16
- 3 public subnets (10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24)
- 3 private subnets (10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24)
- Internet Gateway for public subnets
- NAT Gateway (single for cost, configurable for HA)
- Route tables for public and private subnets
- Enable DNS hostnames and DNS support
- Use availability zones: eu-central-1a, eu-central-1b, eu-central-1c

TAGS:
- Project: "vw-digital-twin"
- Environment: var.environment
- ManagedBy: "terraform"

OUTPUT:
- vpc_id
- public_subnet_ids
- private_subnet_ids
- nat_gateway_id

Follow AWS Well-Architected Framework best practices.
Add comments explaining each resource.
```

### Prompt 2.2: EKS Cluster

```
Create Terraform configuration for AWS EKS cluster.

DIRECTORY: terraform/modules/eks/

FILES:
- main.tf
- variables.tf
- outputs.tf
- iam.tf
- node_groups.tf

REQUIREMENTS:

EKS CLUSTER:
- Kubernetes version: 1.28
- Enable private endpoint access
- Enable public endpoint access (configurable)
- Enable secrets encryption with KMS
- Configure OIDC provider for IRSA

NODE GROUPS:
1. system-nodes:
   - Instance types: t3.medium
   - Min: 2, Max: 4, Desired: 2
   - Labels: role=system
   - Taints: CriticalAddonsOnly=true:NoSchedule

2. application-nodes:
   - Instance types: t3.large
   - Min: 2, Max: 10, Desired: 3
   - Labels: role=application
   - No taints

IAM ROLES:
- Cluster role with AmazonEKSClusterPolicy
- Node role with:
  - AmazonEKSWorkerNodePolicy
  - AmazonEKS_CNI_Policy
  - AmazonEC2ContainerRegistryReadOnly
  - Custom policy for IoT access

ADDONS:
- vpc-cni
- coredns
- kube-proxy
- aws-ebs-csi-driver

OUTPUT:
- cluster_id
- cluster_endpoint
- cluster_certificate_authority
- oidc_provider_arn
- node_security_group_id

Include aws-auth ConfigMap configuration for additional IAM users/roles.
```

### Prompt 2.3: IoT Core Setup

```
Create Terraform configuration for AWS IoT Core.

DIRECTORY: terraform/modules/iot/

FILES:
- main.tf
- variables.tf
- outputs.tf
- policies.tf
- rules.tf

REQUIREMENTS:

IOT THING:
- Name: cnc-simulator-{environment}
- Thing type: CNCMachine
- Attributes: machine_id, location, model

CERTIFICATES:
- Generate IoT certificate
- Attach to thing and policy
- Store private key and certificate in Secrets Manager

IOT POLICY:
Allow:
- iot:Connect with client ID matching thing name
- iot:Publish to topics: dt/cnc/{machine_id}/*
- iot:Subscribe to topics: cmd/cnc/{machine_id}/*
- iot:Receive from subscribed topics

IOT RULES:
1. TelemetryToKinesis:
   - SQL: SELECT * FROM 'dt/cnc/+/telemetry'
   - Action: Kinesis Firehose
   
2. AlertsToSNS:
   - SQL: SELECT * FROM 'dt/cnc/+/alerts' WHERE severity = 'critical'
   - Action: SNS Topic

3. TelemetryToElasticsearch:
   - SQL: SELECT * FROM 'dt/cnc/+/telemetry'
   - Action: Elasticsearch (via Lambda)

OUTPUT:
- iot_endpoint
- thing_arn
- certificate_arn
- certificate_pem (sensitive)
- private_key (sensitive)

Use data sources to get current region and account ID.
```

### Prompt 2.4: Elasticsearch Domain

```
Create Terraform configuration for Amazon Elasticsearch Service.

DIRECTORY: terraform/modules/elasticsearch/

REQUIREMENTS:

DOMAIN CONFIGURATION:
- Domain name: vw-digital-twin-{environment}
- Elasticsearch version: OpenSearch_2.11
- Instance type: t3.small.search (configurable)
- Instance count: 2
- EBS storage: 20GB gp3 per node
- Zone awareness: enabled (2 AZs)

ACCESS POLICY:
- Allow access from EKS node security group
- Allow access from specific IAM roles
- Deny public access

ENCRYPTION:
- Node-to-node encryption: enabled
- Encryption at rest: enabled (use AWS managed key)
- HTTPS required

ADVANCED OPTIONS:
- Automated snapshots at 00:00 UTC
- Slow log publishing to CloudWatch

VPC CONFIGURATION:
- Deploy in private subnets
- Create security group allowing:
  - Port 443 from EKS nodes
  - Port 443 from bastion (if exists)

OUTPUT:
- domain_endpoint
- domain_arn
- kibana_endpoint
- security_group_id

Add CloudWatch alarms for:
- Cluster health
- Free storage space
- CPU utilization
```

### Prompt 2.5: Main Terraform Configuration

```
Create the main Terraform configuration that ties all modules together.

DIRECTORY: terraform/

FILES:
- main.tf - Module calls
- variables.tf - Input variables
- outputs.tf - Outputs
- versions.tf - Provider versions
- backend.tf - S3 backend configuration
- locals.tf - Local values

ALSO CREATE:
terraform/environments/dev/
- terraform.tfvars
- backend.hcl

terraform/environments/prod/
- terraform.tfvars
- backend.hcl

MAIN.TF SHOULD:
1. Configure AWS provider with region variable
2. Call all modules in correct order:
   - VPC (no dependencies)
   - EKS (depends on VPC)
   - IoT (no dependencies)
   - Elasticsearch (depends on VPC)
   - Kinesis (depends on IoT, Elasticsearch)

3. Create additional resources:
   - S3 bucket for data lake
   - ECR repositories for each service
   - Secrets Manager secrets for sensitive data

VARIABLES:
- environment (dev/staging/prod)
- region (default: eu-central-1)
- project_name (default: vw-digital-twin)
- eks_node_instance_types
- elasticsearch_instance_type

BACKEND CONFIGURATION:
- Use S3 backend with DynamoDB locking
- State file path: {project}/{environment}/terraform.tfstate

Include a Makefile with common commands:
- make init ENV=dev
- make plan ENV=dev
- make apply ENV=dev
- make destroy ENV=dev
```

---

## ☸️ PHASE 3: KUBERNETES MICROSERVICES

### Prompt 3.1: Anomaly Detection Service

```
Create the Anomaly Detection microservice.

DIRECTORY: services/anomaly-detection/

FILES:
- src/main.py - FastAPI application
- src/detector.py - Anomaly detection logic
- src/models.py - Pydantic models
- src/kafka_consumer.py - Kafka/Kinesis consumer
- src/config.py - Configuration
- requirements.txt
- Dockerfile
- tests/test_detector.py

REQUIREMENTS:

DETECTION ALGORITHMS:
1. Statistical (Z-score):
   - Calculate rolling mean and std for each metric
   - Flag values > 3 sigma as anomalies
   
2. Isolation Forest:
   - Train on historical data
   - Detect multivariate anomalies

3. Rule-based:
   - Spindle temperature > 70°C
   - Tool wear > 80%
   - Vibration > 5 mm/s
   - Coolant flow < 2 LPM when spindle running

API ENDPOINTS:
GET /health - Health check
GET /ready - Readiness check
POST /detect - Detect anomalies in batch
GET /anomalies - List recent anomalies
GET /metrics - Prometheus metrics

KAFKA CONSUMER:
- Subscribe to telemetry topic
- Process messages in batches
- Publish anomalies to anomaly topic

DATA FLOW:
Kinesis -> Consumer -> Detector -> Elasticsearch + Kafka

METRICS TO EXPORT (Prometheus):
- anomalies_detected_total
- detection_latency_seconds
- messages_processed_total

Include Dockerfile with:
- Python 3.11 slim base
- Non-root user
- Health check
- Proper signal handling
```

### Prompt 3.2: Predictive Maintenance Service

```
Create the Predictive Maintenance microservice.

DIRECTORY: services/predictive-maintenance/

REQUIREMENTS:

PREDICTION MODELS:

1. Tool Remaining Useful Life (RUL):
   - Input: tool wear %, runtime, cutting parameters
   - Output: estimated minutes until replacement needed
   - Algorithm: Linear regression + safety factor

2. Spindle Bearing Health:
   - Input: vibration spectrum, temperature trend
   - Output: health score (0-100), days until maintenance
   - Algorithm: Degradation curve fitting

3. Coolant System Health:
   - Input: flow rate, pressure, temperature trends
   - Output: filter replacement prediction

API ENDPOINTS:
POST /predict/tool-rul - Predict tool remaining life
POST /predict/spindle-health - Assess spindle condition
POST /predict/maintenance-schedule - Generate maintenance schedule
GET /predictions/{machine_id} - Get all predictions for machine

MAINTENANCE SCHEDULE OUTPUT:
{
  "machine_id": "CNC-001",
  "generated_at": "2024-01-15T10:00:00Z",
  "predictions": [
    {
      "component": "Tool T01",
      "action": "Replace",
      "urgency": "medium",
      "estimated_time": "2024-01-16T14:00:00Z",
      "confidence": 0.85
    },
    {
      "component": "Spindle Bearings",
      "action": "Inspect",
      "urgency": "low",
      "estimated_time": "2024-01-25T00:00:00Z",
      "confidence": 0.72
    }
  ]
}

Include model training scripts in scripts/ directory.
Add sample training data in data/ directory.
```

### Prompt 3.3: Digital Twin API

```
Create the Digital Twin API service.

DIRECTORY: services/digital-twin-api/

REQUIREMENTS:

This is the main API that external clients use to interact with the digital twin.

API ENDPOINTS:

GET /machines - List all machines
GET /machines/{id} - Get machine details
GET /machines/{id}/status - Current machine status
GET /machines/{id}/telemetry - Real-time telemetry (WebSocket available)
GET /machines/{id}/history - Historical data query

POST /machines/{id}/commands - Send command to machine
  Commands: start, stop, pause, set_speed, tool_change

GET /predictions/{machine_id} - Get maintenance predictions
GET /anomalies/{machine_id} - Get detected anomalies

WEBSOCKET:
/ws/machines/{id}/telemetry - Real-time telemetry stream

FEATURES:
- Rate limiting (100 req/min per client)
- API key authentication
- Request validation with Pydantic
- OpenAPI documentation
- CORS configuration

DATABASE:
- Use PostgreSQL for machine metadata
- Use Elasticsearch for telemetry queries
- Use Redis for caching and rate limiting

RESPONSE FORMAT:
{
  "status": "success",
  "data": {...},
  "metadata": {
    "timestamp": "ISO8601",
    "request_id": "uuid"
  }
}

ERROR FORMAT:
{
  "status": "error",
  "error": {
    "code": "MACHINE_NOT_FOUND",
    "message": "Machine CNC-001 not found",
    "details": {}
  }
}

Include comprehensive API tests using pytest and httpx.
```

### Prompt 3.4: Helm Charts

```
Create Helm charts for all microservices.

DIRECTORY: kubernetes/charts/

CREATE UMBRELLA CHART:
kubernetes/charts/digital-twin/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── charts/
    ├── anomaly-detection/
    ├── predictive-maintenance/
    ├── alerting-service/
    ├── digital-twin-api/
    └── data-aggregator/

EACH SERVICE CHART SHOULD INCLUDE:
- Deployment with:
  - Configurable replicas
  - Resource limits/requests
  - Liveness/readiness probes
  - Environment variables from ConfigMap/Secret
  - Pod anti-affinity for HA
  
- Service (ClusterIP)
- ServiceAccount with IRSA annotations
- HorizontalPodAutoscaler
- PodDisruptionBudget
- NetworkPolicy

VALUES.YAML STRUCTURE:
replicaCount: 2
image:
  repository: ""
  tag: "latest"
  pullPolicy: IfNotPresent
resources:
  limits:
    cpu: "500m"
    memory: "512Mi"
  requests:
    cpu: "100m"
    memory: "128Mi"
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilization: 70
serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: ""
env: []
secrets: []

ALSO CREATE:
- kubernetes/manifests/namespace.yaml
- kubernetes/manifests/elasticsearch-credentials.yaml
- kubernetes/manifests/iot-certificates.yaml

Include NOTES.txt in each chart with post-install instructions.
```

---

## 🔄 PHASE 4: CI/CD PIPELINE

### Prompt 4.1: GitHub Actions Workflow

```
Create GitHub Actions CI/CD workflows.

DIRECTORY: .github/workflows/

FILES:
1. ci.yaml - Continuous Integration
2. cd-dev.yaml - Deploy to dev
3. cd-prod.yaml - Deploy to prod
4. terraform.yaml - Infrastructure changes

CI.YAML SHOULD:
- Trigger on: push to main, pull requests
- Jobs:
  1. lint:
     - Python: flake8, black, isort
     - Terraform: terraform fmt, tflint
     - Helm: helm lint
     
  2. test:
     - Python unit tests with coverage
     - Minimum coverage: 80%
     
  3. security:
     - Trivy container scanning
     - Checkov for Terraform
     - Safety for Python dependencies
     
  4. build:
     - Build Docker images
     - Push to ECR with commit SHA tag
     - Run on: main branch only

CD-DEV.YAML SHOULD:
- Trigger on: push to main
- Jobs:
  1. deploy:
     - Configure AWS credentials
     - Update kubeconfig
     - Helm upgrade with atomic flag
     - Run integration tests
     - Rollback on failure

CD-PROD.YAML SHOULD:
- Trigger on: release published
- Jobs:
  1. approve:
     - Require manual approval
  2. deploy:
     - Blue-green deployment
     - Smoke tests
     - Progressive rollout

TERRAFORM.YAML SHOULD:
- Trigger on: changes to terraform/**
- Jobs:
  1. plan:
     - terraform init, validate, plan
     - Post plan to PR comment
  2. apply:
     - Only on merge to main
     - Require approval for prod

Use GitHub environments for secrets management.
Include reusable workflow for common steps.
```

### Prompt 4.2: Concourse CI Pipeline

```
Create Concourse CI pipeline configuration.

DIRECTORY: ci-cd/concourse/

FILES:
- pipeline.yaml
- tasks/
  - build-image.yaml
  - run-tests.yaml
  - deploy-helm.yaml
  - terraform-plan.yaml
  - terraform-apply.yaml
- scripts/
  - build.sh
  - test.sh
  - deploy.sh

PIPELINE.YAML:

RESOURCES:
- source-code (git)
- docker-images (registry-image) for each service
- helm-chart (git or s3)
- terraform-state (s3)
- slack-notification (slack-alert)

JOBS:

1. test-and-build:
   - Get source-code
   - Run unit tests
   - Run security scans
   - Build and push Docker images
   - Tag with version

2. deploy-dev:
   - Triggered by successful test-and-build
   - Deploy to dev cluster
   - Run integration tests
   - Notify Slack

3. integration-tests:
   - Run E2E tests against dev
   - Generate test report

4. deploy-staging:
   - Manual trigger
   - Deploy to staging
   - Run smoke tests

5. deploy-prod:
   - Manual trigger with approval
   - Blue-green deployment
   - Canary analysis
   - Full rollout or rollback

6. terraform-plan:
   - Triggered on terraform/* changes
   - Run terraform plan
   - Store plan artifact

7. terraform-apply:
   - Manual trigger
   - Apply saved plan
   - Notify on completion

RESOURCE TYPES:
- registry-image
- git
- s3
- slack-alert

Include fly commands in README for pipeline setup.
```

---

## 📊 PHASE 5: MONITORING & DASHBOARDS

### Prompt 5.1: Kibana Dashboards

```
Create Kibana dashboard configurations.

DIRECTORY: monitoring/kibana-dashboards/

FILES:
- machine-health-overview.ndjson
- tool-wear-analysis.ndjson
- anomaly-detection.ndjson
- predictive-maintenance.ndjson

MACHINE HEALTH OVERVIEW:
Visualizations:
1. Machine Status Indicator (Metric)
   - Shows: Running/Stopped/Error
   - Color coded

2. Key Metrics Gauges
   - Spindle RPM (0-24000)
   - Spindle Load (0-100%)
   - Tool Wear (0-100%)
   - Temperature (20-80°C)

3. Telemetry Time Series (Line chart)
   - Spindle RPM over time
   - Multiple axes support

4. Recent Alerts (Data table)
   - Last 10 alerts
   - Severity, time, message

5. Power Consumption (Area chart)
   - Total, spindle, servo breakdown

TOOL WEAR ANALYSIS:
Visualizations:
1. Wear Progression (Line chart)
   - Wear % over runtime
   - Trend line

2. Tool Life Comparison (Bar chart)
   - Actual vs expected life per tool

3. Wear Rate by Material (Heat map)
   - Rows: Tool types
   - Columns: Material types

4. Replacement Predictions (Table)
   - Tool ID, current wear, predicted replacement time

ANOMALY DETECTION:
Visualizations:
1. Anomaly Timeline (Event chart)
   - Anomaly occurrences over time
   - Severity color coding

2. Anomaly Types (Pie chart)
   - Distribution by type

3. Anomaly Score Trend (Line chart)
   - Rolling anomaly score

4. Root Cause Analysis (Tag cloud)
   - Contributing factors

Export as NDJSON for import via Kibana API.
Include index patterns and saved searches.
```

### Prompt 5.2: Ansible Playbooks

```
Create Ansible playbooks for configuration management.

DIRECTORY: ansible/

STRUCTURE:
ansible/
├── ansible.cfg
├── inventory/
│   ├── dev.yaml
│   └── prod.yaml
├── playbooks/
│   ├── setup-monitoring.yaml
│   ├── configure-elk.yaml
│   ├── deploy-services.yaml
│   └── security-hardening.yaml
├── roles/
│   ├── common/
│   ├── docker/
│   ├── kubernetes/
│   ├── elasticsearch/
│   └── monitoring/
└── group_vars/
    ├── all.yaml
    └── dev.yaml

PLAYBOOKS:

1. setup-monitoring.yaml:
   - Install Prometheus node exporter
   - Configure Filebeat
   - Configure Metricbeat
   - Set up log rotation

2. configure-elk.yaml:
   - Configure Elasticsearch indices
   - Set up index lifecycle management
   - Import Kibana dashboards
   - Configure alerting rules

3. deploy-services.yaml:
   - Pull latest images
   - Update Kubernetes deployments
   - Verify health checks
   - Rollback on failure

4. security-hardening.yaml:
   - Configure firewall rules
   - Set up fail2ban
   - Rotate secrets
   - Update TLS certificates

ROLES:

common:
- Install base packages
- Configure NTP
- Set up logging

elasticsearch:
- Configure index templates
- Set up ILM policies
- Configure snapshot repository

kubernetes:
- Install kubectl
- Configure kubeconfig
- Set up Helm

Include variable encryption with Ansible Vault.
Add molecule tests for roles.
```

---

## 📝 PHASE 6: DOCUMENTATION

### Prompt 6.1: README Template

```
Create a comprehensive README for the GitHub repository.

FILE: README.md

STRUCTURE:

# CNC Machine Digital Twin - Connected Factory Demo

## 🎯 Overview
Brief description of what this project demonstrates.
Link to VW job position.
Mention unique value: CNC expertise + cloud skills.

## 🏗️ Architecture
Embed architecture diagram.
Brief explanation of each component.

## 🛠️ Technology Stack
Table of all technologies used.
Why each was chosen.

## 🚀 Quick Start

### Prerequisites
- AWS account with appropriate permissions
- Terraform >= 1.5
- kubectl >= 1.28
- Helm >= 3.12
- Python >= 3.11
- Docker >= 24.0

### Deployment

1. Infrastructure Setup
```bash
cd terraform/environments/dev
terraform init
terraform apply
```

2. Deploy Services
```bash
cd kubernetes/charts/digital-twin
helm upgrade --install digital-twin . -f values-dev.yaml
```

3. Start Simulator
```bash
cd simulator
python -m src.main
```

## 📊 Dashboards
Screenshots of Kibana dashboards.
How to access.

## 🧪 Testing
How to run tests.
Coverage requirements.

## 📈 Demo
Link to demo video.
What the demo shows.

## 🤝 About the Author
Brief intro.
Link to LinkedIn.
Why this project demonstrates relevant skills.

## 📄 License
MIT License

Include badges for:
- Build status
- Code coverage
- License
- Python version
```

### Prompt 6.2: Demo Video Script

```
Create a script for the demo video.

FILE: docs/demo-script.md

VIDEO STRUCTURE (5 minutes):

0:00-0:30 - INTRODUCTION
"Hi, I'm [Name], a CNC programmer with 10 years of experience, 
transitioning into cloud engineering. This project demonstrates 
how I combine manufacturing domain knowledge with modern DevOps practices."

0:30-1:30 - ARCHITECTURE OVERVIEW
Show architecture diagram.
Explain data flow briefly.
Highlight VW-relevant technologies.

1:30-2:30 - LIVE DEMO: SIMULATOR
- Show CNC simulator running
- Explain telemetry data
- Show MQTT messages
- Inject a failure mode

2:30-3:30 - LIVE DEMO: MONITORING
- Show Kibana dashboards
- Point out anomaly detection
- Show predictive maintenance predictions

3:30-4:30 - INFRASTRUCTURE
- Show Terraform code briefly
- Show Kubernetes pods
- Show CI/CD pipeline

4:30-5:00 - CLOSING
"This project shows I can:
1. Design cloud architectures
2. Implement Infrastructure as Code
3. Build microservices on Kubernetes
4. Apply manufacturing domain expertise

I'm excited about the opportunity to bring this combination 
to Volkswagen's Connected Cars platform."

RECORDING TIPS:
- Use OBS or similar
- 1080p resolution
- Clear audio
- Show terminal and browser side by side
- Use tmux for terminal management
```

---

## 🔥 QUICK START PROMPTS

### For Immediate Progress

**Start with Codex:**
```
I'm building a CNC machine simulator for a VW job application demo.
Create the core CNCMachine class in Python with realistic spindle 
physics and telemetry generation. The candidate has 10+ years of 
CNC experience, so use accurate machining parameters.

Start with: simulator/src/cnc_machine.py
```

**Start with Claude Code:**
```
I'm building a cloud infrastructure demo for VW. Create the 
Terraform VPC module with 3 public and 3 private subnets in 
eu-central-1. Follow AWS Well-Architected best practices.

Create: terraform/modules/vpc/
```

---

## 📋 CHECKLIST

Use this to track progress:

### Phase 1: Simulator
- [ ] Core CNCMachine class
- [ ] Spindle physics
- [ ] Tool wear model
- [ ] G-code parser
- [ ] MQTT publisher
- [ ] Failure mode injection
- [ ] Dockerfile
- [ ] Unit tests

### Phase 2: Infrastructure
- [ ] VPC module
- [ ] EKS module
- [ ] IoT module
- [ ] Elasticsearch module
- [ ] Main configuration
- [ ] Backend setup

### Phase 3: Microservices
- [ ] Anomaly detection
- [ ] Predictive maintenance
- [ ] Digital Twin API
- [ ] Alerting service
- [ ] Helm charts

### Phase 4: CI/CD
- [ ] GitHub Actions
- [ ] Concourse CI
- [ ] Deployment scripts

### Phase 5: Monitoring
- [ ] Kibana dashboards
- [ ] Ansible playbooks
- [ ] Alerting rules

### Phase 6: Documentation
- [ ] README
- [ ] Architecture docs
- [ ] Demo video

---

*These prompts are designed to be copy-pasted directly into Codex or Claude Code. Each prompt is self-contained with all necessary context.*
