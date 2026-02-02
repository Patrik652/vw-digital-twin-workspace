# Codex TODO List - CNC Digital Twin

## Phase 1: CNC Simulator
- [x] Task 2: CNC Machine Core Class
  - [x] cnc_machine.py - Main machine class
  - [x] spindle.py - Spindle dynamics with thermal modeling
  - [ ] axes.py - X, Y, Z axis simulation
  - [ ] tool_manager.py - Tool wear using Taylor's equation
  - [x] config.py - Configuration management
  - [x] models.py - Pydantic data models
- [x] Task 3: MQTT Publisher
  - [x] mqtt_publisher.py - Async MQTT client
  - [x] TLS support for AWS IoT
- [x] Task 4: G-code Parser
  - [x] gcode_parser.py - FANUC-style parser
  - [x] Sample G-code programs
- [x] Task 5: Failure Modes
  - [x] failure_modes.py - Failure injection system
  - [x] 5 failure types implemented
- [x] Task 6: Docker
  - [x] Dockerfile
  - [x] docker-compose.yaml for local testing

## Phase 3: Microservices
- [x] Task 12: Anomaly Detection
  - [x] Statistical detection (Z-score)
  - [x] ML detection (Isolation Forest)
  - [x] Rule-based detection
  - [x] FastAPI endpoints
  - [x] Dockerfile
- [x] Task 13: Predictive Maintenance
  - [x] Tool RUL prediction
  - [x] Spindle health assessment
  - [x] Maintenance scheduling
  - [x] FastAPI endpoints
  - [x] Dockerfile
- [x] Task 14: Digital Twin API
  - [x] REST endpoints
  - [x] WebSocket for real-time data
  - [x] Authentication
  - [x] Dockerfile

## Current Status
- Started: 2026-02-01
- Current Task: Final verification
- Blockers: None
