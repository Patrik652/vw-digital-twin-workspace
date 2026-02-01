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
- Started: 2026-02-01
- Current Task: Task 2
- Blockers: None
