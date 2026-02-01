# 🚀 QUICK START GUIDE

## How to Use These Documents

### For Codex (OpenAI)

1. **Start a new Codex session**
2. **Copy the Master Prompt** from `02_AI_AGENT_PROMPTS.md` (Section: MASTER PROMPT)
3. **Paste it as your first message**
4. **Then copy specific task prompts** from Phase 1, 2, etc.

**Best for:**
- CNC Simulator (Python algorithms)
- G-code Parser
- Anomaly Detection ML
- Predictive Maintenance

### For Claude Code (Anthropic)

1. **Open Claude Code**
2. **Copy the Master Prompt** from `02_AI_AGENT_PROMPTS.md`
3. **Then copy specific task prompts**

**Best for:**
- Terraform Infrastructure
- Kubernetes/Helm
- CI/CD Pipelines
- Documentation

---

## Recommended Workflow

### Day 1: Setup & Foundation

```
Morning:
1. Create GitHub repository
2. Set up project structure (see STARTER_CODE.md Section 1)
3. Initialize git, create .gitignore

Afternoon (Codex):
4. Start with CNC Simulator Core (Prompt 1.1)
5. Add MQTT Publisher (Prompt 1.3 reference in STARTER_CODE)

Evening (Claude Code):
6. Create Terraform VPC module (Prompt 2.1)
```

### Day 2: Continue Development

```
Codex:
- G-code Parser (Prompt 1.3)
- Failure Modes (Prompt 1.2)

Claude Code:
- Terraform EKS (Prompt 2.2)
- Terraform IoT (Prompt 2.3)
```

### Day 3-4: Services & Infrastructure

```
Codex:
- Anomaly Detection Service (Prompt 3.1)
- Predictive Maintenance (Prompt 3.2)

Claude Code:
- Terraform Elasticsearch (Prompt 2.4)
- Terraform Main Config (Prompt 2.5)
- Helm Charts (Prompt 3.4)
```

### Day 5: Integration & CI/CD

```
Claude Code:
- GitHub Actions (Prompt 4.1)
- Concourse CI (Prompt 4.2)
- Kibana Dashboards (Prompt 5.1)
```

### Day 6-7: Polish & Documentation

```
- Fix any issues
- Write final documentation
- Record demo video
- Final review
```

---

## Documents Overview

| File | Purpose |
|------|---------|
| `01_PROJECT_SPEC.md` | Complete project specification |
| `02_AI_AGENT_PROMPTS.md` | Ready-to-use prompts for AI agents |
| `03_TASK_BREAKDOWN.md` | Detailed tasks with dependencies |
| `04_README_TEMPLATE.md` | GitHub README template |
| `05_STARTER_CODE.md` | Copy-paste code templates |
| `06_QUICK_START.md` | This file - how to use everything |

---

## Tips for Success

### 1. Start Simple
Don't try to build everything at once. Start with the simulator running locally, then add cloud pieces.

### 2. Test Continuously
After each component, test it works before moving on.

### 3. Use Docker Compose Locally
The `docker-compose.yaml` in STARTER_CODE.md lets you test everything locally before deploying to AWS.

### 4. Document As You Go
Add comments and update README as you build. Don't leave it for the end.

### 5. Record Short Demo Clips
Record 30-second clips of each feature working. Compile into final video.

---

## AWS Cost Considerations

**Estimated Monthly Cost (Dev Environment):**

| Service | Configuration | ~Cost/Month |
|---------|--------------|-------------|
| EKS | 1 cluster | $73 |
| EC2 (nodes) | 3x t3.medium | $90 |
| Elasticsearch | t3.small.search x2 | $50 |
| IoT Core | <1M messages | <$5 |
| S3 | <10GB | <$1 |
| **Total** | | **~$220/month** |

**Cost Saving Tips:**
- Use `terraform destroy` when not working
- Use smaller instances for dev
- Set up billing alerts

---

## Common Issues & Solutions

### Codex Issues

**Problem:** Codex generates incomplete code
**Solution:** Ask it to continue, or break into smaller prompts

**Problem:** Code doesn't follow project structure
**Solution:** Re-paste the Master Prompt, emphasize directory structure

### Claude Code Issues

**Problem:** Terraform syntax errors
**Solution:** Run `terraform validate` and paste errors back

**Problem:** Helm chart issues
**Solution:** Run `helm lint` and ask Claude to fix

### AWS Issues

**Problem:** Permission denied
**Solution:** Check IAM policies, use `aws sts get-caller-identity`

**Problem:** EKS connection refused
**Solution:** Update kubeconfig, check security groups

---

## Final Checklist Before Submission

### Code Quality
- [ ] All tests pass
- [ ] No linting errors
- [ ] Code is well-commented
- [ ] No hardcoded secrets

### Documentation
- [ ] README is complete
- [ ] Architecture diagram included
- [ ] Setup instructions work

### Demo
- [ ] Video is <5 minutes
- [ ] Shows all key features
- [ ] Audio is clear

### Repository
- [ ] Clean commit history
- [ ] No large binary files
- [ ] LICENSE file present
- [ ] .gitignore is proper

---

## Contact

If you have questions about this project template, reach out to Claude!

---

**Good luck with the VW application! 🚗⚡**

*Remember: Your unique combination of CNC expertise + cloud skills is your competitive advantage. Make sure that comes through in everything you build.*
