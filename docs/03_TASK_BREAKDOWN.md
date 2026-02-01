# Task Breakdown & Implementation Order

## Recommended Agent Assignment

| Phase | Component | Recommended Agent | Estimated Time | Complexity |
|-------|-----------|-------------------|----------------|------------|
| 1 | CNC Simulator Core | Codex | 4-6 hours | High |
| 1 | G-code Parser | Codex | 2-3 hours | Medium |
| 1 | Failure Modes | Codex | 2-3 hours | Medium |
| 2 | Terraform VPC | Claude Code | 1-2 hours | Low |
| 2 | Terraform EKS | Claude Code | 2-3 hours | Medium |
| 2 | Terraform IoT | Claude Code | 2-3 hours | Medium |
| 2 | Terraform ES | Claude Code | 1-2 hours | Low |
| 3 | Anomaly Detection | Codex | 3-4 hours | High |
| 3 | Predictive Maintenance | Codex | 3-4 hours | High |
| 3 | Digital Twin API | Either | 3-4 hours | Medium |
| 3 | Helm Charts | Claude Code | 2-3 hours | Medium |
| 4 | GitHub Actions | Claude Code | 2-3 hours | Medium |
| 4 | Concourse CI | Claude Code | 2-3 hours | Medium |
| 5 | Kibana Dashboards | Claude Code | 2-3 hours | Medium |
| 5 | Ansible Playbooks | Claude Code | 2-3 hours | Medium |
| 6 | Documentation | Claude Code | 2-3 hours | Low |

**Total Estimated Time:** 35-50 hours

---

## Implementation Order

### 🟢 Day 1-2: Foundation (Start Here)

```
ORDER:
1. Create repository structure
2. CNC Simulator - Core classes
3. CNC Simulator - MQTT publishing
4. Terraform - VPC module
```

**Why this order:**
- Simulator can run locally without cloud
- VPC is dependency for everything else
- Quick visible progress

### 🟡 Day 3-4: Infrastructure

```
ORDER:
5. Terraform - EKS module
6. Terraform - IoT Core module
7. Terraform - Elasticsearch module
8. Terraform - Main configuration
9. Deploy infrastructure to AWS
```

**Why this order:**
- EKS needs VPC
- IoT and ES are independent
- Main config ties it together

### 🟠 Day 5-6: Microservices

```
ORDER:
10. Anomaly Detection service
11. Digital Twin API
12. Predictive Maintenance service
13. Helm charts for all services
14. Deploy to EKS
```

**Why this order:**
- Anomaly detection is core functionality
- API exposes the system
- Helm charts deploy everything

### 🔴 Day 7-8: Integration & Polish

```
ORDER:
15. CI/CD pipelines
16. Kibana dashboards
17. Ansible playbooks
18. Integration testing
19. Documentation
20. Demo video
```

---

## Detailed Task List

### TASK 1: Repository Structure
**Agent:** Either
**Time:** 15 minutes
**Prompt:**
```
Create the following directory structure:

vw-digital-twin-demo/
├── .github/workflows/
├── docs/
├── simulator/
│   ├── src/
│   └── tests/
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

Create empty .gitkeep files in each directory.
Create initial README.md with project title.
```

### TASK 2: CNC Simulator Core
**Agent:** Codex (better at Python algorithms)
**Time:** 4-6 hours
**Dependencies:** Task 1
**Prompt:** See PROMPTS.md > Phase 1 > Prompt 1.1

**Acceptance Criteria:**
- [ ] CNCMachine class initializes correctly
- [ ] Spindle RPM calculates with realistic physics
- [ ] Tool wear updates based on cutting parameters
- [ ] Telemetry JSON matches specified schema
- [ ] Simulator loop runs at configurable frequency
- [ ] Unit tests pass with >80% coverage

### TASK 3: MQTT Publisher
**Agent:** Either
**Time:** 1-2 hours
**Dependencies:** Task 2
**Prompt:**
```
Add MQTT publishing capability to the CNC simulator.

FILE: simulator/src/mqtt_publisher.py

REQUIREMENTS:
- Use paho-mqtt library
- Connect to configurable broker (localhost:1883 default)
- Publish to topic: dt/cnc/{machine_id}/telemetry
- Support TLS with certificate authentication (for AWS IoT)
- Reconnect on connection loss
- Buffer messages if disconnected

Add configuration in simulator/src/config.py:
- MQTT_BROKER
- MQTT_PORT
- MQTT_USE_TLS
- MQTT_CERT_PATH
- MQTT_KEY_PATH
- MQTT_CA_PATH

Test with local Mosquitto broker.
```

### TASK 4: G-code Parser
**Agent:** Codex
**Time:** 2-3 hours
**Dependencies:** Task 2
**Prompt:** See PROMPTS.md > Phase 1 > Prompt 1.3

### TASK 5: Failure Modes
**Agent:** Codex
**Time:** 2-3 hours
**Dependencies:** Tasks 2, 4
**Prompt:** See PROMPTS.md > Phase 1 > Prompt 1.2

### TASK 6: Simulator Dockerfile
**Agent:** Either
**Time:** 30 minutes
**Dependencies:** Tasks 2-5
**Prompt:**
```
Create Dockerfile for the CNC simulator.

FILE: simulator/Dockerfile

REQUIREMENTS:
- Base image: python:3.11-slim
- Create non-root user
- Install dependencies from requirements.txt
- Copy source code
- Set PYTHONPATH
- Health check using HTTP endpoint or process check
- Handle SIGTERM gracefully

Also create:
- simulator/.dockerignore
- simulator/docker-compose.yaml (for local testing with Mosquitto)
```

### TASK 7: Terraform VPC
**Agent:** Claude Code
**Time:** 1-2 hours
**Dependencies:** Task 1
**Prompt:** See PROMPTS.md > Phase 2 > Prompt 2.1

### TASK 8: Terraform EKS
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Task 7
**Prompt:** See PROMPTS.md > Phase 2 > Prompt 2.2

### TASK 9: Terraform IoT Core
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Task 1
**Prompt:** See PROMPTS.md > Phase 2 > Prompt 2.3

### TASK 10: Terraform Elasticsearch
**Agent:** Claude Code
**Time:** 1-2 hours
**Dependencies:** Task 7
**Prompt:** See PROMPTS.md > Phase 2 > Prompt 2.4

### TASK 11: Terraform Main Configuration
**Agent:** Claude Code
**Time:** 2 hours
**Dependencies:** Tasks 7-10
**Prompt:** See PROMPTS.md > Phase 2 > Prompt 2.5

### TASK 12: Anomaly Detection Service
**Agent:** Codex
**Time:** 3-4 hours
**Dependencies:** Task 1
**Prompt:** See PROMPTS.md > Phase 3 > Prompt 3.1

### TASK 13: Predictive Maintenance Service
**Agent:** Codex
**Time:** 3-4 hours
**Dependencies:** Task 1
**Prompt:** See PROMPTS.md > Phase 3 > Prompt 3.2

### TASK 14: Digital Twin API
**Agent:** Either
**Time:** 3-4 hours
**Dependencies:** Tasks 12, 13
**Prompt:** See PROMPTS.md > Phase 3 > Prompt 3.3

### TASK 15: Helm Charts
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Tasks 12-14
**Prompt:** See PROMPTS.md > Phase 3 > Prompt 3.4

### TASK 16: GitHub Actions
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Tasks 6, 15
**Prompt:** See PROMPTS.md > Phase 4 > Prompt 4.1

### TASK 17: Concourse CI
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Tasks 6, 15
**Prompt:** See PROMPTS.md > Phase 4 > Prompt 4.2

### TASK 18: Kibana Dashboards
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Task 10
**Prompt:** See PROMPTS.md > Phase 5 > Prompt 5.1

### TASK 19: Ansible Playbooks
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** Task 8
**Prompt:** See PROMPTS.md > Phase 5 > Prompt 5.2

### TASK 20: Documentation
**Agent:** Claude Code
**Time:** 2-3 hours
**Dependencies:** All above
**Prompt:** See PROMPTS.md > Phase 6 > Prompt 6.1

---

## Dependency Graph

```
                    ┌──────────────────┐
                    │  Task 1: Repo    │
                    │    Structure     │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Task 2: CNC    │  │ Task 7: TF VPC │  │ Task 9: TF IoT │
│ Simulator Core │  │                │  │                │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                   │
        ▼                   │                   │
┌────────────────┐          │                   │
│ Task 3: MQTT   │          │                   │
└───────┬────────┘          │                   │
        │                   │                   │
        ▼                   ▼                   │
┌────────────────┐  ┌────────────────┐          │
│ Task 4: G-code │  │ Task 8: TF EKS │          │
└───────┬────────┘  └───────┬────────┘          │
        │                   │                   │
        ▼                   ▼                   │
┌────────────────┐  ┌────────────────┐          │
│ Task 5: Fails  │  │ Task 10: TF ES │          │
└───────┬────────┘  └───────┬────────┘          │
        │                   │                   │
        ▼                   ▼                   ▼
┌────────────────┐  ┌─────────────────────────────┐
│ Task 6: Docker │  │ Task 11: TF Main Config     │
└───────┬────────┘  └─────────────┬───────────────┘
        │                         │
        │     ┌───────────────────┤
        │     │                   │
        ▼     ▼                   ▼
┌─────────────────────────┐     ┌────────────────┐
│ Tasks 12-14: Services   │     │ Tasks 18-19:   │
│ (Anomaly, Pred, API)    │     │ Kibana, Ansible│
└───────────┬─────────────┘     └────────────────┘
            │
            ▼
┌────────────────┐
│ Task 15: Helm  │
└───────┬────────┘
        │
        ▼
┌─────────────────┐
│ Tasks 16-17:    │
│ CI/CD Pipelines │
└───────┬─────────┘
        │
        ▼
┌────────────────┐
│ Task 20: Docs  │
└────────────────┘
```

---

## Parallel Execution Strategy

If you have both Codex and Claude Code available simultaneously:

### Sprint 1 (Parallel)
| Codex | Claude Code |
|-------|-------------|
| Task 2: CNC Core | Task 7: TF VPC |
| Task 3: MQTT | Task 9: TF IoT |
| Task 4: G-code | Task 10: TF ES |

### Sprint 2 (Parallel)
| Codex | Claude Code |
|-------|-------------|
| Task 5: Failures | Task 8: TF EKS |
| Task 6: Docker | Task 11: TF Main |

### Sprint 3 (Parallel)
| Codex | Claude Code |
|-------|-------------|
| Task 12: Anomaly | Task 15: Helm Charts |
| Task 13: Predictive | Task 16: GitHub Actions |
| Task 14: API | Task 17: Concourse |

### Sprint 4 (Parallel)
| Codex | Claude Code |
|-------|-------------|
| Integration Testing | Task 18: Kibana |
| Bug Fixes | Task 19: Ansible |

### Sprint 5 (Sequential)
| Agent |
|-------|
| Task 20: Documentation |
| Demo Video Recording |

---

## Quality Gates

### Before Moving to Next Phase

**After Phase 1 (Simulator):**
- [ ] Simulator runs locally for 1 hour without errors
- [ ] All unit tests pass
- [ ] Telemetry JSON validates against schema
- [ ] MQTT messages received by test broker

**After Phase 2 (Infrastructure):**
- [ ] Terraform plan shows no errors
- [ ] Terraform apply succeeds in dev environment
- [ ] EKS cluster accessible via kubectl
- [ ] IoT endpoint responds to MQTT test message

**After Phase 3 (Services):**
- [ ] All services build successfully
- [ ] All services pass unit tests
- [ ] Helm charts lint without errors
- [ ] Services deploy to EKS without errors

**After Phase 4 (CI/CD):**
- [ ] Pipeline runs on push
- [ ] All stages complete successfully
- [ ] Deployment updates running pods

**After Phase 5 (Monitoring):**
- [ ] Kibana dashboards load without errors
- [ ] Data appears in dashboards
- [ ] Alerts fire for test conditions

---

## Troubleshooting Common Issues

### Simulator Issues
| Problem | Solution |
|---------|----------|
| MQTT connection refused | Check broker is running, verify port |
| Import errors | Verify PYTHONPATH, check dependencies |
| Memory leak | Check for unbounded lists, add cleanup |

### Terraform Issues
| Problem | Solution |
|---------|----------|
| State lock error | Check DynamoDB, run `terraform force-unlock` |
| Permission denied | Check IAM policies, verify credentials |
| Resource already exists | Import existing resource or rename |

### Kubernetes Issues
| Problem | Solution |
|---------|----------|
| ImagePullBackOff | Check ECR permissions, image tag |
| CrashLoopBackOff | Check logs, verify env vars |
| Pending pods | Check node resources, PVC |

### ELK Issues
| Problem | Solution |
|---------|----------|
| No data in Kibana | Check index pattern, verify Logstash |
| Elasticsearch red | Check disk space, cluster health |
| Dashboard not loading | Check Kibana logs, clear cache |

---

*Use this document to track progress and coordinate work between agents.*
