# 🏭 CNC Machine Digital Twin - Connected Factory Demo

[![Build Status](https://github.com/YOUR_USERNAME/vw-digital-twin-demo/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/vw-digital-twin-demo/actions)
[![Coverage](https://codecov.io/gh/YOUR_USERNAME/vw-digital-twin-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/vw-digital-twin-demo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-1.5+-623CE4.svg)](https://www.terraform.io/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-1.28+-326CE5.svg)](https://kubernetes.io/)

> **A cloud-native Industrial IoT platform demonstrating Digital Twin capabilities for CNC machines, built with the exact technology stack used by Volkswagen Group Services.**

---

## 🎯 Project Overview

This project demonstrates the integration of **manufacturing domain expertise** with **modern cloud engineering practices**. It showcases:

- **Real-time CNC machine simulation** with accurate physics modeling
- **Industrial IoT data pipeline** using AWS IoT Core
- **Kubernetes-based microservices** for data processing
- **ML-powered anomaly detection** and predictive maintenance
- **Complete Infrastructure as Code** with Terraform
- **Production-grade CI/CD** with comprehensive testing

### Why This Project?

As a **CNC programmer with 10+ years of experience** transitioning into cloud engineering, I bring a unique perspective that combines:

| Manufacturing Knowledge | Cloud Skills |
|------------------------|--------------|
| CNC machine dynamics | AWS architecture |
| G-code programming | Kubernetes orchestration |
| Predictive maintenance | Infrastructure as Code |
| Quality control processes | CI/CD pipelines |
| Production optimization | Monitoring & observability |

This combination is directly relevant to **Volkswagen's Digital Production Platform (DPP)** and their **Connected Cars** initiatives.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CNC MACHINE DIGITAL TWIN                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐           │
│  │ CNC Simulator  │────▶│  AWS IoT Core  │────▶│    Kinesis     │           │
│  │   (Python)     │MQTT │                │     │    Firehose    │           │
│  └────────────────┘     └────────────────┘     └───────┬────────┘           │
│                                                         │                    │
│  ┌──────────────────────────────────────────────────────┼──────────────────┐│
│  │                    KUBERNETES (EKS)                  │                  ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │                  ││
│  │  │  Anomaly    │  │ Predictive  │  │  Alerting   │   │                  ││
│  │  │ Detection   │  │ Maintenance │  │  Service    │◀──┘                  ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘                      ││
│  │  ┌─────────────┐  ┌─────────────┐                                       ││
│  │  │ Digital Twin│  │    Data     │                                       ││
│  │  │    API      │  │ Aggregator  │                                       ││
│  │  └─────────────┘  └─────────────┘                                       ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │                         MONITORING (ELK)                                 ││
│  │  Elasticsearch ◀── Logstash ◀── Filebeat/Metricbeat                     ││
│  │       │                                                                  ││
│  │       ▼                                                                  ││
│  │    Kibana ───▶ Dashboards: Health | Anomalies | Predictions             ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  Infrastructure: Terraform │ Ansible │ GitHub Actions / Concourse CI        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Cloud** | AWS | Primary cloud provider |
| **Orchestration** | Kubernetes (EKS) | Microservices platform |
| **Infrastructure** | Terraform | Infrastructure as Code |
| **Configuration** | Ansible | Configuration management |
| **CI/CD** | GitHub Actions, Concourse CI | Deployment automation |
| **Monitoring** | ELK Stack (Elasticsearch, Logstash, Kibana) | Logging & visualization |
| **Containers** | Docker, Helm | Packaging & deployment |
| **IoT** | AWS IoT Core, MQTT | Device communication |
| **Languages** | Python, Go, Bash | Application code |

---

## 📊 Features

### CNC Machine Simulator
- ✅ Realistic spindle dynamics with thermal modeling
- ✅ Tool wear simulation using Taylor's equation
- ✅ G-code parser supporting FANUC syntax
- ✅ Multiple failure mode injection
- ✅ MQTT telemetry publishing

### Anomaly Detection
- ✅ Statistical analysis (Z-score)
- ✅ Machine Learning (Isolation Forest)
- ✅ Rule-based thresholds
- ✅ Real-time alerting

### Predictive Maintenance
- ✅ Tool Remaining Useful Life (RUL) prediction
- ✅ Spindle bearing health assessment
- ✅ Maintenance scheduling optimization

### Infrastructure
- ✅ Multi-AZ VPC with public/private subnets
- ✅ Managed Kubernetes (EKS) with autoscaling
- ✅ Elasticsearch domain with lifecycle management
- ✅ Complete IAM and security configuration

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required tools
aws --version        # >= 2.0
terraform --version  # >= 1.5
kubectl version      # >= 1.28
helm version         # >= 3.12
python --version     # >= 3.11
docker --version     # >= 24.0
```

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/vw-digital-twin-demo.git
cd vw-digital-twin-demo
```

### 2. Configure AWS

```bash
# Configure AWS credentials
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="eu-central-1"
```

### 3. Deploy Infrastructure

```bash
cd terraform/environments/dev

# Initialize Terraform
terraform init

# Review plan
terraform plan

# Apply infrastructure
terraform apply
```

### 4. Configure Kubernetes

```bash
# Update kubeconfig
aws eks update-kubeconfig --name vw-digital-twin-dev --region eu-central-1

# Verify connection
kubectl get nodes
```

### 5. Deploy Services

```bash
cd kubernetes/charts/digital-twin

# Install Helm chart
helm upgrade --install digital-twin . \
  -f values-dev.yaml \
  --namespace digital-twin \
  --create-namespace
```

### 6. Run Simulator Locally

```bash
cd simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run simulator
python -m src.main
```

---

## 📈 Dashboards

### Machine Health Overview
![Machine Health Dashboard](docs/images/dashboard-health.png)

### Anomaly Detection
![Anomaly Dashboard](docs/images/dashboard-anomaly.png)

### Predictive Maintenance
![Predictive Dashboard](docs/images/dashboard-predictive.png)

---

## 🧪 Testing

### Unit Tests

```bash
# Simulator tests
cd simulator
pytest tests/ -v --cov=src --cov-report=html

# Service tests
cd services/anomaly-detection
pytest tests/ -v --cov=src
```

### Integration Tests

```bash
# Run integration test suite
./scripts/integration-tests.sh
```

### Infrastructure Tests

```bash
# Terraform validation
cd terraform
terraform validate

# Helm linting
cd kubernetes/charts/digital-twin
helm lint .
```

---

## 🎬 Demo Video

[![Demo Video](docs/images/video-thumbnail.png)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

**Demo Contents (5 minutes):**
1. Architecture overview
2. Live simulator demonstration
3. Failure mode injection
4. Anomaly detection in action
5. Kibana dashboard walkthrough
6. CI/CD pipeline execution

---

## 📁 Project Structure

```
vw-digital-twin-demo/
├── 📄 README.md
├── 📄 LICENSE
├── 📁 .github/
│   └── workflows/          # CI/CD pipelines
├── 📁 docs/
│   ├── architecture.md
│   ├── setup-guide.md
│   └── images/
├── 📁 simulator/           # CNC machine simulator
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── 📁 services/            # Microservices
│   ├── anomaly-detection/
│   ├── predictive-maintenance/
│   ├── alerting-service/
│   ├── digital-twin-api/
│   └── data-aggregator/
├── 📁 terraform/           # Infrastructure as Code
│   ├── modules/
│   └── environments/
├── 📁 kubernetes/          # K8s configurations
│   ├── charts/
│   └── manifests/
├── 📁 ansible/             # Configuration management
│   ├── playbooks/
│   └── roles/
├── 📁 ci-cd/               # Pipeline configurations
│   └── concourse/
└── 📁 monitoring/          # Dashboards & alerting
    ├── kibana-dashboards/
    └── grafana-dashboards/
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `eu-central-1` |
| `MQTT_BROKER` | MQTT broker address | `localhost` |
| `MQTT_PORT` | MQTT broker port | `1883` |
| `ELASTICSEARCH_URL` | Elasticsearch endpoint | - |
| `LOG_LEVEL` | Logging level | `INFO` |

### Terraform Variables

See `terraform/variables.tf` for all available configuration options.

---

## 🔒 Security

- All secrets stored in AWS Secrets Manager
- TLS encryption for all communications
- IRSA (IAM Roles for Service Accounts) for pod-level permissions
- Network policies restricting pod-to-pod communication
- Container images scanned with Trivy

---

## 🤝 About the Author

**[Your Name]**

CNC Programmer & Production Planner transitioning into Cloud Engineering

- 🏭 10+ years in CNC programming and manufacturing
- ☁️ AWS, Kubernetes, Terraform expertise
- 🤖 Passion for automation and AI/ML
- 📍 Slovakia

**Why Volkswagen Group Services?**

The combination of my manufacturing domain expertise with cloud engineering skills makes me uniquely qualified to contribute to VW's Digital Production Platform and Connected Cars initiatives. I understand both sides - the factory floor reality and the cloud architecture that connects it.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Volkswagen Group for inspiring this project
- AWS for comprehensive documentation
- The open-source community for amazing tools

---

<p align="center">
  <i>Built with ❤️ for Volkswagen Group Services</i>
</p>
