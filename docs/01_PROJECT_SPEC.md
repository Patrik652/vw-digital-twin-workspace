# CNC Machine Digital Twin - Connected Factory Demo

## Project Vision

A demonstration project showcasing cloud-native Industrial IoT capabilities for Volkswagen Group Services, combining **real manufacturing domain expertise** with **modern DevOps practices**.

**Why This Project Matters:**
- Directly relevant to VW's Digital Production Platform (DPP)
- Demonstrates understanding of both cloud AND manufacturing
- Uses the exact tech stack VW requires (AWS, EKS, ELK, Terraform, Ansible)
- Shows practical knowledge that generic "connected car" demos don't have

---

## Target Position

**Cloud Platform Engineer with Automation Focus**
- Company: Volkswagen Group Services, Slovakia
- Platform: Connected Cars Platform + Digital Production Platform
- Tech Stack: AWS, Kubernetes, Terraform, Ansible, ELK, CI/CD

---

## Project Overview

### What We're Building

A **Digital Twin** of a CNC machine that:
1. Simulates realistic CNC machine behavior with proper physics
2. Streams telemetry data to AWS IoT Core
3. Processes data through Kubernetes microservices
4. Detects anomalies and predicts maintenance needs
5. Visualizes everything in ELK dashboards

### Why CNC Machine (Not Generic IoT)?

The candidate has **10+ years of CNC programming experience**. This project demonstrates:
- Deep understanding of manufacturing processes
- Ability to model real-world industrial systems
- Knowledge that connects cloud platforms to factory floor reality
- Unique perspective that pure software engineers lack

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CNC MACHINE DIGITAL TWIN                             │
│                     Cloud-Native Industrial IoT Platform                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────┐     ┌────────────────────┐     ┌─────────────────┐  │
│  │   EDGE LAYER       │     │   INGESTION LAYER  │     │  STORAGE LAYER  │  │
│  │                    │     │                    │     │                 │  │
│  │  ┌──────────────┐  │     │  ┌──────────────┐  │     │ ┌─────────────┐ │  │
│  │  │CNC Simulator │  │────▶│  │ AWS IoT Core │  │────▶│ │   Kinesis   │ │  │
│  │  │  (Python)    │  │MQTT │  │              │  │     │ │   Firehose  │ │  │
│  │  └──────────────┘  │     │  └──────────────┘  │     │ └─────────────┘ │  │
│  │         │          │     │                    │     │        │        │  │
│  │  Generates:        │     │  Routes messages   │     │        ▼        │  │
│  │  - Spindle RPM     │     │  to appropriate    │     │ ┌─────────────┐ │  │
│  │  - Feed Rate       │     │  destinations      │     │ │    S3       │ │  │
│  │  - Tool Wear %     │     │                    │     │ │  (Archive)  │ │  │
│  │  - Temperature     │     │                    │     │ └─────────────┘ │  │
│  │  - Vibration       │     │                    │     │                 │  │
│  │  - Power Draw      │     │                    │     │                 │  │
│  └────────────────────┘     └────────────────────┘     └─────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      PROCESSING LAYER (EKS)                           │   │
│  │                                                                       │   │
│  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   │
│  │   │ Anomaly         │  │ Predictive      │  │ Alerting        │      │   │
│  │   │ Detection       │  │ Maintenance     │  │ Service         │      │   │
│  │   │ Service         │  │ Service         │  │                 │      │   │
│  │   │                 │  │                 │  │ - Slack         │      │   │
│  │   │ - Statistical   │  │ - Tool wear     │  │ - Email         │      │   │
│  │   │ - ML-based      │  │   prediction    │  │ - PagerDuty     │      │   │
│  │   │                 │  │ - RUL estimate  │  │                 │      │   │
│  │   └─────────────────┘  └─────────────────┘  └─────────────────┘      │   │
│  │                                                                       │   │
│  │   ┌─────────────────┐  ┌─────────────────┐                           │   │
│  │   │ Digital Twin    │  │ Data            │                           │   │
│  │   │ API             │  │ Aggregator      │                           │   │
│  │   │                 │  │                 │                           │   │
│  │   │ - REST API      │  │ - Time-series   │                           │   │
│  │   │ - WebSocket     │  │ - Statistics    │                           │   │
│  │   │ - GraphQL       │  │ - Rollups       │                           │   │
│  │   └─────────────────┘  └─────────────────┘                           │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      MONITORING LAYER (ELK)                           │   │
│  │                                                                       │   │
│  │   ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────┐    │   │
│  │   │Elasticsearch│◀──│  Logstash   │◀──│  Filebeat / Metricbeat  │    │   │
│  │   └─────────────┘   └─────────────┘   └─────────────────────────┘    │   │
│  │          │                                                            │   │
│  │          ▼                                                            │   │
│  │   ┌─────────────┐                                                     │   │
│  │   │   Kibana    │  Dashboards:                                        │   │
│  │   │             │  - Machine Health Overview                          │   │
│  │   │             │  - Tool Wear Trends                                 │   │
│  │   │             │  - Anomaly Detection Alerts                         │   │
│  │   │             │  - Predictive Maintenance                           │   │
│  │   └─────────────┘                                                     │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      INFRASTRUCTURE LAYER                             │   │
│  │                                                                       │   │
│  │   Terraform          Ansible            CI/CD                         │   │
│  │   ├── VPC            ├── ELK Setup      ├── GitHub Actions           │   │
│  │   ├── EKS Cluster    ├── K8s Config     ├── Concourse CI             │   │
│  │   ├── IoT Core       ├── Monitoring     └── ArgoCD                   │   │
│  │   ├── S3 Buckets     └── Security                                    │   │
│  │   └── IAM Roles                                                       │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Required by VW (Must Have)

| Category | Technology | Purpose |
|----------|------------|---------|
| Cloud | AWS | Primary cloud provider |
| Container Orchestration | Kubernetes (EKS) | Microservices platform |
| IaC | Terraform | Infrastructure provisioning |
| Configuration | Ansible | Configuration management |
| CI/CD | Concourse CI | Pipeline automation |
| Monitoring | ELK Stack | Logging and visualization |
| Containers | Docker | Application packaging |

### Additional Technologies

| Category | Technology | Purpose |
|----------|------------|---------|
| Package Management | Helm | Kubernetes templating |
| Scripting | Python, Bash | Automation scripts |
| IoT Protocol | MQTT | Device communication |
| API | FastAPI | REST endpoints |
| ML | scikit-learn | Anomaly detection |

---

## Component Specifications

### 1. CNC Machine Simulator

**Purpose:** Generate realistic CNC machine telemetry data

**Features:**
- G-code parser and executor
- Realistic physics simulation
- Multiple failure modes
- MQTT data publishing

**Telemetry Data Points:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "machine_id": "CNC-001",
  "spindle": {
    "rpm": 12000,
    "load_percent": 45.2,
    "temperature_c": 38.5,
    "vibration_mm_s": 0.8
  },
  "axes": {
    "x": {"position_mm": 150.234, "velocity_mm_min": 5000},
    "y": {"position_mm": 75.891, "velocity_mm_min": 5000},
    "z": {"position_mm": -25.500, "velocity_mm_min": 2000}
  },
  "tool": {
    "id": "T01",
    "type": "end_mill",
    "diameter_mm": 10,
    "wear_percent": 23.5,
    "runtime_minutes": 145
  },
  "coolant": {
    "flow_rate_lpm": 12.5,
    "temperature_c": 22.3,
    "pressure_bar": 4.2
  },
  "power": {
    "total_kw": 8.5,
    "spindle_kw": 5.2,
    "servo_kw": 2.8
  },
  "status": {
    "mode": "AUTO",
    "program": "O1234",
    "block": "N0150",
    "cycle_time_s": 234
  }
}
```

**Failure Modes to Simulate:**
1. Tool wear degradation (gradual)
2. Spindle bearing wear (vibration increase)
3. Coolant system degradation
4. Thermal drift
5. Axis backlash development

### 2. AWS Infrastructure (Terraform)

**Resources to Provision:**
- VPC with public/private subnets
- EKS cluster with managed node groups
- AWS IoT Core with thing, certificate, policy
- Kinesis Firehose for data streaming
- S3 buckets for data lake
- Elasticsearch domain
- IAM roles and policies

**Directory Structure:**
```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
│   ├── vpc/
│   ├── eks/
│   ├── iot/
│   ├── kinesis/
│   ├── elasticsearch/
│   └── s3/
└── environments/
    ├── dev/
    └── prod/
```

### 3. Kubernetes Microservices

**Services:**

| Service | Language | Purpose | Replicas |
|---------|----------|---------|----------|
| anomaly-detection | Python | Detect abnormal patterns | 2 |
| predictive-maintenance | Python | Predict failures | 2 |
| alerting-service | Go | Send notifications | 2 |
| digital-twin-api | Python | REST/WebSocket API | 3 |
| data-aggregator | Python | Time-series aggregation | 2 |

**Helm Chart Structure:**
```
kubernetes/
├── charts/
│   ├── anomaly-detection/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   ├── predictive-maintenance/
│   ├── alerting-service/
│   ├── digital-twin-api/
│   └── data-aggregator/
└── umbrella-chart/
    ├── Chart.yaml
    ├── values.yaml
    └── values-dev.yaml
```

### 4. CI/CD Pipeline

**Pipeline Stages:**
1. **Build** - Docker image build and push
2. **Test** - Unit tests, integration tests
3. **Security** - Container scanning, SAST
4. **Deploy Dev** - Deploy to dev environment
5. **Integration Tests** - E2E testing
6. **Deploy Prod** - Production deployment (manual approval)

**Concourse CI Pipeline:**
```yaml
resources:
  - name: source-code
    type: git
  - name: docker-image
    type: docker-image

jobs:
  - name: build-and-test
  - name: deploy-to-dev
  - name: integration-tests
  - name: deploy-to-prod
```

### 5. ELK Monitoring

**Kibana Dashboards:**

1. **Machine Health Overview**
   - Current status indicators
   - Key metrics gauges
   - Recent alerts timeline

2. **Tool Wear Analysis**
   - Wear progression over time
   - Remaining useful life
   - Replacement predictions

3. **Anomaly Detection**
   - Real-time anomaly scores
   - Historical anomaly patterns
   - Root cause analysis

4. **Predictive Maintenance**
   - Upcoming maintenance schedule
   - Component health scores
   - Cost optimization metrics

---

## Industry Standards Alignment

### Relevant Standards (VW Uses These)

| Standard | Description | How We Apply |
|----------|-------------|--------------|
| **Catena-X** | Automotive data exchange | Data model compatibility |
| **OPC UA** | Industrial communication | Protocol awareness |
| **ISO 23247** | Digital Twin framework | Architecture alignment |
| **MQTT** | IoT messaging | Device communication |

### Kubernetes Best Practices

- Resource limits and requests
- Health checks (liveness, readiness)
- Pod disruption budgets
- Horizontal pod autoscaling
- Network policies
- RBAC configuration

---

## Success Criteria

### Technical Criteria

- [ ] CNC simulator generates realistic data
- [ ] Data flows through entire pipeline
- [ ] Anomaly detection identifies injected faults
- [ ] Dashboards display real-time data
- [ ] CI/CD pipeline deploys automatically
- [ ] Infrastructure is fully codified

### Demonstration Criteria

- [ ] 5-minute demo video showing full system
- [ ] Clean, documented GitHub repository
- [ ] Architecture diagrams
- [ ] README with clear setup instructions

---

## Timeline

| Week | Deliverables |
|------|--------------|
| 1 | CNC Simulator + Basic IoT setup |
| 2 | Terraform infrastructure + EKS cluster |
| 3 | Microservices + Docker + Helm charts |
| 4 | ELK monitoring + CI/CD pipeline |
| 5 | Polish, documentation, demo video |

---

## Repository Structure

```
vw-digital-twin-demo/
├── README.md
├── LICENSE
├── .github/
│   └── workflows/
├── docs/
│   ├── architecture.md
│   ├── setup-guide.md
│   └── demo-video.md
├── simulator/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── services/
│   ├── anomaly-detection/
│   ├── predictive-maintenance/
│   ├── alerting-service/
│   ├── digital-twin-api/
│   └── data-aggregator/
├── terraform/
│   ├── modules/
│   └── environments/
├── kubernetes/
│   ├── charts/
│   └── manifests/
├── ansible/
│   ├── playbooks/
│   └── roles/
├── ci-cd/
│   └── concourse/
└── monitoring/
    ├── kibana-dashboards/
    └── grafana-dashboards/
```

---

## Contact

**Candidate:** [Your Name]
**Email:** [Your Email]
**LinkedIn:** [Your LinkedIn]
**GitHub:** [This Repository]

---

*This project demonstrates practical cloud engineering skills combined with deep manufacturing domain expertise - the unique combination that Volkswagen Group Services needs for their Industrial IoT platform.*
