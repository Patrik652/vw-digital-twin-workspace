# 🚀 CLAUDE CODE KICKOFF PROMPT

Copy everything below this line and paste it into Claude Code:

---

# VW Digital Twin Project - CLAUDE CODE AGENT

You are the **PRIMARY INFRASTRUCTURE/DEVOPS AGENT** for building a CNC Machine Digital Twin demonstration project for a Volkswagen Group Services job application.

## 📋 YOUR MISSION

Build the **AWS Infrastructure**, **Kubernetes deployments**, **CI/CD pipelines**, and **Documentation** - the backbone that makes everything run. You handle all Terraform, Helm, YAML, and documentation.

## 📁 PROJECT DOCUMENTATION

**CRITICAL: Before doing ANYTHING, read these documents in ./docs/ folder:**

```
./docs/
├── 01_PROJECT_SPEC.md      # Full project specification - READ FIRST
├── 02_AI_AGENT_PROMPTS.md  # Detailed prompts for each task - YOUR TASK LIST
├── 03_TASK_BREAKDOWN.md    # Task dependencies and order
├── 04_README_TEMPLATE.md   # GitHub README template
├── 05_STARTER_CODE.md      # Copy-paste code templates (Terraform, Helm, CI/CD)
└── 06_QUICK_START.md       # Workflow guide
```

**Read them NOW in this order:**
1. `cat ./docs/01_PROJECT_SPEC.md` - Understand the project
2. `cat ./docs/03_TASK_BREAKDOWN.md` - See your assigned tasks
3. `cat ./docs/02_AI_AGENT_PROMPTS.md` - Get detailed prompts for each task

## 🎯 YOUR TASKS (Claude Code is responsible for these)

| Task # | Component | Priority |
|--------|-----------|----------|
| 1 | Repository Structure | 🔴 HIGH (if not done) |
| 7 | Terraform VPC Module | 🔴 HIGH |
| 8 | Terraform EKS Module | 🔴 HIGH |
| 9 | Terraform IoT Module | 🟡 MEDIUM |
| 10 | Terraform Elasticsearch Module | 🟡 MEDIUM |
| 11 | Terraform Main Configuration | 🟡 MEDIUM |
| 15 | Helm Charts | 🔴 HIGH |
| 16 | GitHub Actions CI/CD | 🟡 MEDIUM |
| 17 | Concourse CI Pipeline | 🟢 LOW |
| 18 | Kibana Dashboards | 🟢 LOW |
| 19 | Ansible Playbooks | 🟢 LOW |
| 20 | Documentation & README | 🔴 HIGH |

**Codex handles:** CNC Simulator, Python services, ML algorithms

## 🏁 STEP 1: CHECK/SETUP GIT REPOSITORY

First, verify the project structure exists. If not, create it:

```bash
# Check if repo exists
if [ -d "vw-digital-twin-demo/.git" ]; then
    echo "✅ Git repo already exists"
    cd vw-digital-twin-demo
else
    echo "Creating new repo..."
    mkdir -p vw-digital-twin-demo
    cd vw-digital-twin-demo
    git init
    
    # Create directory structure
    mkdir -p {simulator/src,simulator/tests,services/{anomaly-detection,predictive-maintenance,alerting-service,digital-twin-api,data-aggregator}/{src,tests},terraform/{modules/{vpc,eks,iot,elasticsearch,s3},environments/{dev,prod}},kubernetes/{charts/digital-twin/charts/{anomaly-detection,predictive-maintenance,alerting-service,digital-twin-api,data-aggregator}/templates,manifests},ansible/{playbooks,roles/{common,elasticsearch,kubernetes}/tasks},ci-cd/concourse,monitoring/{kibana-dashboards,grafana-dashboards},.github/workflows,docs}
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
venv/
.env

# Terraform
*.tfstate
*.tfstate.*
.terraform/
*.tfvars
!*.tfvars.example
.terraform.lock.hcl

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store

# Logs
*.log

# Secrets
*.pem
*.key
secrets/
EOF

    git add .
    git commit -m "Initial project structure"
fi

echo "Current directory: $(pwd)"
ls -la
```

## 🏁 STEP 2: CREATE YOUR TODO LIST

Create a TODO.md file tracking your progress:

```bash
cat > TODO_CLAUDE_CODE.md << 'EOF'
# Claude Code TODO List - CNC Digital Twin

## Phase 2: Terraform Infrastructure
- [ ] Task 7: VPC Module
  - [ ] main.tf - VPC, subnets, NAT, IGW
  - [ ] variables.tf
  - [ ] outputs.tf
- [ ] Task 8: EKS Module
  - [ ] main.tf - EKS cluster
  - [ ] iam.tf - IAM roles
  - [ ] node_groups.tf - Node groups
  - [ ] variables.tf, outputs.tf
- [ ] Task 9: IoT Core Module
  - [ ] main.tf - Thing, certificate, policy
  - [ ] rules.tf - IoT rules
  - [ ] variables.tf, outputs.tf
- [ ] Task 10: Elasticsearch Module
  - [ ] main.tf - ES domain
  - [ ] variables.tf, outputs.tf
- [ ] Task 11: Main Configuration
  - [ ] main.tf - Tie all modules together
  - [ ] variables.tf, outputs.tf
  - [ ] versions.tf, backend.tf
  - [ ] environments/dev/terraform.tfvars
  - [ ] environments/prod/terraform.tfvars

## Phase 3: Kubernetes
- [ ] Task 15: Helm Charts
  - [ ] Umbrella chart (digital-twin)
  - [ ] anomaly-detection chart
  - [ ] predictive-maintenance chart
  - [ ] alerting-service chart
  - [ ] digital-twin-api chart
  - [ ] data-aggregator chart
  - [ ] values.yaml, values-dev.yaml, values-prod.yaml

## Phase 4: CI/CD
- [ ] Task 16: GitHub Actions
  - [ ] ci.yaml - Lint, test, security
  - [ ] cd-dev.yaml - Deploy to dev
  - [ ] cd-prod.yaml - Deploy to prod
  - [ ] terraform.yaml - Infrastructure
- [ ] Task 17: Concourse CI
  - [ ] pipeline.yaml
  - [ ] Task definitions

## Phase 5: Monitoring & Config
- [ ] Task 18: Kibana Dashboards
  - [ ] machine-health-overview.ndjson
  - [ ] anomaly-detection.ndjson
  - [ ] predictive-maintenance.ndjson
- [ ] Task 19: Ansible Playbooks
  - [ ] setup-monitoring.yaml
  - [ ] configure-elk.yaml
  - [ ] deploy-services.yaml

## Phase 6: Documentation
- [ ] Task 20: Documentation
  - [ ] README.md (use template from docs/04_README_TEMPLATE.md)
  - [ ] docs/architecture.md
  - [ ] docs/setup-guide.md
  - [ ] CONTRIBUTING.md
  - [ ] LICENSE

## Current Status
- Started: [DATE]
- Current Task: Task 7
- Blockers: None
EOF

echo "✅ TODO list created!"
```

## 🏁 STEP 3: START BUILDING

Now start with **Task 7: Terraform VPC Module**.

Read the detailed prompt in `./docs/02_AI_AGENT_PROMPTS.md` under "Phase 2 > Prompt 2.1"

**Key Requirements for VPC:**
- CIDR: 10.0.0.0/16
- 3 public subnets (10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24)
- 3 private subnets (10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24)
- Internet Gateway, NAT Gateway
- Region: eu-central-1

**Start with these files:**
```
terraform/modules/vpc/
├── main.tf
├── variables.tf
└── outputs.tf
```

## 💡 TERRAFORM BEST PRACTICES

1. **Use consistent naming:**
   ```hcl
   locals {
     name_prefix = "${var.project_name}-${var.environment}"
   }
   ```

2. **Always add tags:**
   ```hcl
   tags = merge(var.tags, {
     Name = "${local.name_prefix}-resource"
   })
   ```

3. **Use data sources for dynamic values:**
   ```hcl
   data "aws_availability_zones" "available" {
     state = "available"
   }
   ```

4. **Validate with:**
   ```bash
   terraform fmt -recursive
   terraform validate
   ```

## 💡 HELM CHART BEST PRACTICES

1. **Use umbrella chart pattern:**
   ```
   charts/digital-twin/
   ├── Chart.yaml (dependencies listed)
   ├── values.yaml
   └── charts/
       ├── anomaly-detection/
       └── ...
   ```

2. **Include in every deployment:**
   - Resource limits/requests
   - Liveness/readiness probes
   - ServiceAccount
   - PodDisruptionBudget

3. **Validate with:**
   ```bash
   helm lint .
   helm template . --debug
   ```

## 🔄 COORDINATE WITH CODEX

**You build infrastructure. Codex builds applications.**

- When you finish Helm charts, Codex's services need to match the expected structure
- Your CI/CD pipelines will build and deploy Codex's Dockerfiles
- Your Terraform outputs (ECR URLs, ES endpoint) are needed by services

**Communication pattern:**
1. You create ECR repositories in Terraform
2. Output the repository URLs
3. Codex's Dockerfiles get pushed to those URLs
4. Your Helm charts reference those URLs

## 🚦 BEGIN NOW

1. Read the docs: `cat ./docs/01_PROJECT_SPEC.md`
2. Verify/create git repo with structure above
3. Create TODO_CLAUDE_CODE.md
4. Start Task 7: Terraform VPC Module
5. Update TODO as you complete tasks

**Recommended order:**
```
Task 7 (VPC) → Task 8 (EKS) → Task 11 (Main) → Task 15 (Helm) → Task 16 (CI/CD) → Task 20 (Docs)
```

Tasks 9, 10, 17, 18, 19 can be done in parallel or later.

**YOU HAVE SUPER POWER - USE IT WISELY! Build enterprise-grade infrastructure! 🏗️⚡**

---

End of prompt. Good luck!
