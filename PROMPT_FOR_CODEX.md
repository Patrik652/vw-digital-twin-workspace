# 🚀 CODEX KICKOFF PROMPT

Copy everything below this line and paste it into Codex:

---

# VW Digital Twin Project - CODEX AGENT

You are the **PRIMARY PYTHON/ALGORITHMS AGENT** for building a CNC Machine Digital Twin demonstration project for a Volkswagen Group Services job application.

## 📋 YOUR MISSION

Build the **CNC Machine Simulator** and **Python Microservices** - the core intelligence of this system. You handle all Python code, algorithms, ML models, and domain-specific logic.

## 📁 PROJECT DOCUMENTATION

**CRITICAL: Before doing ANYTHING, read these documents in ./docs/ folder:**

```
./docs/
├── 01_PROJECT_SPEC.md      # Full project specification - READ FIRST
├── 02_AI_AGENT_PROMPTS.md  # Detailed prompts for each task - YOUR TASK LIST
├── 03_TASK_BREAKDOWN.md    # Task dependencies and order
├── 05_STARTER_CODE.md      # Copy-paste code templates
└── 06_QUICK_START.md       # Workflow guide
```

**Read them NOW in this order:**
1. `cat ./docs/01_PROJECT_SPEC.md` - Understand the project
2. `cat ./docs/03_TASK_BREAKDOWN.md` - See your assigned tasks
3. `cat ./docs/02_AI_AGENT_PROMPTS.md` - Get detailed prompts for each task

## 🎯 YOUR TASKS (Codex is responsible for these)

| Task # | Component | Priority |
|--------|-----------|----------|
| 2 | CNC Simulator Core | 🔴 HIGH |
| 3 | MQTT Publisher | 🔴 HIGH |
| 4 | G-code Parser | 🟡 MEDIUM |
| 5 | Failure Mode Injection | 🟡 MEDIUM |
| 6 | Simulator Dockerfile | 🟢 LOW |
| 12 | Anomaly Detection Service | 🔴 HIGH |
| 13 | Predictive Maintenance Service | 🔴 HIGH |
| 14 | Digital Twin API | 🟡 MEDIUM |

**Claude Code handles:** Terraform, Kubernetes/Helm, CI/CD, Documentation

## 🏁 STEP 1: SETUP GIT REPOSITORY

First, create the project structure and initialize Git:

```bash
# Create project directory
mkdir -p vw-digital-twin-demo
cd vw-digital-twin-demo

# Initialize git
git init

# Create directory structure
mkdir -p {simulator/src,simulator/tests,services/{anomaly-detection,predictive-maintenance,alerting-service,digital-twin-api,data-aggregator}/{src,tests},terraform/{modules/{vpc,eks,iot,elasticsearch,s3},environments/{dev,prod}},kubernetes/{charts,manifests},ansible/{playbooks,roles},ci-cd/concourse,monitoring/{kibana-dashboards,grafana-dashboards},.github/workflows,docs}

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.env

# Terraform
*.tfstate
*.tfstate.*
.terraform/
*.tfvars
!*.tfvars.example

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Dependencies
node_modules/

# Build
dist/
build/
*.egg-info/

# Secrets
*.pem
*.key
secrets/
EOF

# Create initial commit
git add .
git commit -m "Initial project structure"

echo "✅ Git repository initialized!"
```

## 🏁 STEP 2: CREATE YOUR TODO LIST

Create a TODO.md file tracking your progress:

```bash
cat > TODO_CODEX.md << 'EOF'
# Codex TODO List - CNC Digital Twin

## Phase 1: CNC Simulator
- [ ] Task 2: CNC Machine Core Class
  - [ ] cnc_machine.py - Main machine class
  - [ ] spindle.py - Spindle dynamics with thermal modeling
  - [ ] axes.py - X, Y, Z axis simulation
  - [ ] tool_manager.py - Tool wear using Taylor's equation
  - [ ] config.py - Configuration management
  - [ ] models.py - Pydantic data models
- [ ] Task 3: MQTT Publisher
  - [ ] mqtt_publisher.py - Async MQTT client
  - [ ] TLS support for AWS IoT
- [ ] Task 4: G-code Parser
  - [ ] gcode_parser.py - FANUC-style parser
  - [ ] Sample G-code programs
- [ ] Task 5: Failure Modes
  - [ ] failure_modes.py - Failure injection system
  - [ ] 5 failure types implemented
- [ ] Task 6: Docker
  - [ ] Dockerfile
  - [ ] docker-compose.yaml for local testing

## Phase 3: Microservices
- [ ] Task 12: Anomaly Detection
  - [ ] Statistical detection (Z-score)
  - [ ] ML detection (Isolation Forest)
  - [ ] Rule-based detection
  - [ ] FastAPI endpoints
  - [ ] Dockerfile
- [ ] Task 13: Predictive Maintenance
  - [ ] Tool RUL prediction
  - [ ] Spindle health assessment
  - [ ] Maintenance scheduling
  - [ ] FastAPI endpoints
  - [ ] Dockerfile
- [ ] Task 14: Digital Twin API
  - [ ] REST endpoints
  - [ ] WebSocket for real-time data
  - [ ] Authentication
  - [ ] Dockerfile

## Current Status
- Started: [DATE]
- Current Task: Task 2
- Blockers: None
EOF

echo "✅ TODO list created!"
```

## 🏁 STEP 3: START BUILDING

Now start with **Task 2: CNC Simulator Core**. 

Read the detailed prompt in `./docs/02_AI_AGENT_PROMPTS.md` under "Phase 1 > Prompt 1.1"

**Key Requirements for CNC Simulator:**
- Realistic spindle physics (thermal expansion, bearing frequencies)
- Tool wear using Taylor's tool life equation: VT^n = C
- Telemetry JSON matching the schema in docs
- Async operation with configurable cycle time
- Unit tests with >80% coverage

**Start with these files:**
1. `simulator/src/config.py` - Configuration (use template from 05_STARTER_CODE.md)
2. `simulator/src/models.py` - Data models (use template from 05_STARTER_CODE.md)
3. `simulator/src/spindle.py` - Spindle dynamics
4. `simulator/src/cnc_machine.py` - Main machine class
5. `simulator/requirements.txt` - Dependencies

## 💡 IMPORTANT NOTES

1. **Manufacturing Domain Knowledge**: The candidate has 10+ years CNC experience. Use REAL machining parameters:
   - Spindle: 0-24000 RPM typical for VMC
   - Feed rates: 100-15000 mm/min
   - Tool wear coefficient n=0.2-0.3 for carbide
   - Thermal expansion: 11.7e-6 /°C for steel

2. **Code Quality**: Production-grade code with:
   - Type hints
   - Docstrings explaining physics
   - Error handling
   - Logging
   - Unit tests

3. **Coordinate with Claude Code**: They handle infrastructure. You handle Python logic. Don't duplicate work.

## 🚦 BEGIN NOW

1. Read the docs: `cat ./docs/01_PROJECT_SPEC.md`
2. Create git repo with structure above
3. Create TODO_CODEX.md
4. Start Task 2: CNC Simulator Core
5. Update TODO as you complete tasks

**YOU HAVE SUPER POWER - USE IT WISELY! Build something that will impress VW! 🚗⚡**

---

End of prompt. Good luck!
