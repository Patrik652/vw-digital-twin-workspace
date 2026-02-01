# 🎯 MASTER COORDINATION GUIDE

## How to Use This Workspace

### Folder Structure
```
vw-digital-twin-workspace/
├── docs/                        # Project documentation
│   ├── 01_PROJECT_SPEC.md
│   ├── 02_AI_AGENT_PROMPTS.md
│   ├── 03_TASK_BREAKDOWN.md
│   ├── 04_README_TEMPLATE.md
│   ├── 05_STARTER_CODE.md
│   └── 06_QUICK_START.md
├── PROMPT_FOR_CODEX.md          # 👉 Copy this to Codex
├── PROMPT_FOR_CLAUDE_CODE.md    # 👉 Copy this to Claude Code
└── MASTER_COORDINATION.md       # This file
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Open Two Terminals in tmux

```bash
# Create tmux session
tmux new-session -s vw-project

# Split window vertically
# Ctrl+b then %

# Left pane: Codex
# Right pane: Claude Code
```

### Step 2: Copy Workspace to Both Agents

Both agents need access to the docs folder. Point them to the same directory:

```bash
# In both terminals, navigate to workspace
cd /path/to/vw-digital-twin-workspace
```

### Step 3: Paste Prompts

**Left pane (Codex):**
```bash
cat PROMPT_FOR_CODEX.md
# Copy the content and paste into Codex
```

**Right pane (Claude Code):**
```bash
cat PROMPT_FOR_CLAUDE_CODE.md
# Copy the content and paste into Claude Code
```

### Step 4: Let Them Work!

Both agents will:
1. Read the documentation
2. Create TODO lists
3. Initialize Git repo (one of them)
4. Start working on their tasks

---

## 📊 Task Division

| Component | Codex | Claude Code |
|-----------|-------|-------------|
| Git Setup | ✅ | ✅ (backup) |
| CNC Simulator | ✅ | ❌ |
| Python Services | ✅ | ❌ |
| Terraform | ❌ | ✅ |
| Helm Charts | ❌ | ✅ |
| CI/CD | ❌ | ✅ |
| Documentation | ❌ | ✅ |

---

## 🔄 Workflow Timeline

### Hour 1-2: Foundation
```
CODEX                          CLAUDE CODE
├── Read docs                  ├── Read docs
├── Create git repo            ├── Verify repo exists
├── Start CNC Simulator        └── Start Terraform VPC
│   └── config.py
│   └── models.py
│   └── spindle.py
```

### Hour 3-4: Core Components
```
CODEX                          CLAUDE CODE
├── cnc_machine.py             ├── Terraform EKS
├── mqtt_publisher.py          ├── Terraform IoT
└── gcode_parser.py            └── Terraform ES
```

### Hour 5-6: Services & Deployment
```
CODEX                          CLAUDE CODE
├── failure_modes.py           ├── Terraform Main
├── Anomaly Detection          ├── Helm Charts
└── Predictive Maintenance     └── GitHub Actions
```

### Hour 7-8: Integration
```
CODEX                          CLAUDE CODE
├── Digital Twin API           ├── Concourse CI
├── Unit tests                 ├── Kibana Dashboards
└── Dockerfiles                └── README & Docs
```

---

## 🔗 Integration Points

### 1. ECR Repositories
**Claude Code creates** → **Codex uses**
```
terraform/outputs.tf:
  ecr_repositories = {
    "cnc-simulator" = "123456789.dkr.ecr.eu-central-1.amazonaws.com/vw-digital-twin-dev/cnc-simulator"
    ...
  }

Codex references in:
  services/*/Dockerfile
  .github/workflows/ci.yaml
```

### 2. Elasticsearch Endpoint
**Claude Code creates** → **Codex configures**
```
terraform/outputs.tf:
  elasticsearch_endpoint = "https://..."

Codex uses in:
  services/anomaly-detection/src/config.py
  services/predictive-maintenance/src/config.py
```

### 3. Helm Values
**Codex builds images** → **Claude Code deploys**
```
Codex creates:
  services/anomaly-detection/Dockerfile

Claude Code references:
  kubernetes/charts/digital-twin/values.yaml:
    anomaly-detection:
      image:
        repository: ${ECR_URL}/anomaly-detection
```

---

## 🛑 Handling Conflicts

If both agents try to edit the same file:

1. **Stop one agent**
2. **Let the other complete**
3. **Have the stopped agent pull changes:**
   ```bash
   git pull origin main
   ```
4. **Continue**

**Files likely to conflict:**
- `.github/workflows/ci.yaml` (both might touch)
- `README.md` (both might add sections)

**Solution:** Give Claude Code ownership of these files.

---

## ✅ Checkpoint Verification

### After Hour 2:
```bash
# Check simulator structure
ls simulator/src/
# Expected: config.py, models.py, spindle.py, cnc_machine.py

# Check Terraform
ls terraform/modules/vpc/
# Expected: main.tf, variables.tf, outputs.tf

# Validate Terraform
cd terraform/modules/vpc && terraform init && terraform validate
```

### After Hour 4:
```bash
# Test simulator
cd simulator && python -m pytest tests/ -v

# Check all Terraform modules
for module in vpc eks iot elasticsearch; do
  cd terraform/modules/$module
  terraform validate
  cd -
done
```

### After Hour 6:
```bash
# Lint Helm charts
helm lint kubernetes/charts/digital-twin/

# Check GitHub Actions syntax
# (use actionlint or validate in GitHub)

# Build Docker images
docker build -t cnc-simulator simulator/
```

### After Hour 8:
```bash
# Full integration test
docker-compose up -d

# Wait for services
sleep 30

# Check simulator
curl http://localhost:8080/health

# Check Kibana
curl http://localhost:5601/api/status
```

---

## 📝 Final Deliverables Checklist

- [ ] Git repository with clean history
- [ ] CNC Simulator running locally
- [ ] All Python tests passing (>80% coverage)
- [ ] Terraform validates without errors
- [ ] Helm charts lint successfully
- [ ] CI/CD pipeline defined
- [ ] README.md complete with screenshots
- [ ] Architecture diagram included
- [ ] Demo video recorded

---

## 🆘 Troubleshooting

### "Module not found" in Python
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/simulator/src"
```

### Terraform state issues
```bash
rm -rf .terraform
terraform init
```

### Docker build fails
```bash
# Check Dockerfile syntax
docker build --no-cache .
```

### Helm chart errors
```bash
helm template . --debug 2>&1 | head -50
```

---

## 💬 Commands to Check Progress

```bash
# See what's done
find . -name "*.py" -o -name "*.tf" -o -name "*.yaml" | wc -l

# Git log
git log --oneline -20

# TODO status
cat TODO_CODEX.md TODO_CLAUDE_CODE.md | grep -E "^\s*-\s*\[.\]"
```

---

**Good luck! You've got this! 🚀🚗**
