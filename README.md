# 🚁 DroneAgent - Autonomous Drone Control System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AutoGen](https://img.shields.io/badge/AutoGen-LLM_Agents-orange.svg)](https://microsoft.github.io/autogen/)
[![MavSDK](https://img.shields.io/badge/MavSDK-Drone_Control-green.svg)](https://mavsdk.mavlink.io/)
[![PX4 Autopilot](https://img.shields.io/badge/PX4-Autopilot-blueviolet.svg)](https://px4.io/)

## 🌟 Advanced Embodied AI for Unmanned Aerial Vehicles

**DroneAgent** is an advanced, hierarchical multi-agent system designed to bridge the gap between large language models (LLMs) and programmatic flight hardware. By leveraging the **Microsoft AutoGen** framework in tandem with **MavSDK** and **PX4 Autopilot**, this architecture translates complex, unstructured natural language queries into deterministic, parameterized flight commands.

This repository serves as a foundational architecture for deploying embodied AI agents capable of high-level reasoning, spatial planning, and hardware-in-the-loop (SITL) execution.

---

## 🏗️ Hierarchical Agent Architecture

The system utilizes a dual-agent paradigm to ensure strict safety and operational compliance:
1. **The Planner LLM:** Synthesizes the user's natural language goal, reasons through spatial and operational constraints, and formulates a step-by-step execution plan using available MavSDK function primitives.
2. **The Executor Agent:** Safely executes the compiled Python function calls directly against the MavSDK server, providing real-time telemetry and state feedback to the Planner.

```mermaid
---
title: DroneAgent Translation & Execution Pipeline
---
flowchart TD;
    User([User Natural Language Query]) --> TextProcessing[NLP / Speech-to-Text Interface];
    TextProcessing --> PlannerLLM[AutoGen Planner Agent];
    
    subgraph Agent Interaction Loop
        PlannerLLM <-->|Formulates Plan & Code| Executor[AutoGen Executor Agent];
        Executor <-->|Telemetry & State Feedback| PlannerLLM;
    end
    
    Executor --> MavSDK[MavSDK Python API];
    
    subgraph Simulation & Hardware Execution
        MavSDK --> SITL[Gazebo SITL (PX4)];
        MavSDK --> Hardware[HolyBro x500 Drone Framework];
    end
```

---

## 🚀 Core Capabilities & Skills

The agent is equipped with a library of strongly-typed Python functions (skills) that map directly to MavSDK control primitives. The LLM understands these capabilities via Python `Annotated` typing.

### Current Flight Primitives
- 🛫 **Automated Takeoff & Landing**: Precision altitude targeting.
- 📍 **Waypoint Navigation**: `fly_to_coordinates(x, y, z)`.
- 🔄 **Spatial Maneuvers**: `circle_point(radius, velocity)`, `rotate_yaw(degrees)`.
- 🛑 **Safety Protocols**: `hover_in_place()`, `return_to_launch()`.

### Example LLM Reasoning Chains
**User Prompt:** *"Takeoff to 12 meters, go to coordinates (2, 6) at that same altitude, complete a circle maneuver, and return to launch."*
**Agent Action:** The Planner LLM decomposes this into sequential `takeoff(12)`, `fly_to_coordinates(2, 6, 12)`, `circle_point(...)`, and `return_to_launch()` API calls, executing them synchronously while monitoring PX4 state margins.

---

## 🛠️ System Requirements & Deployment

### Dependencies
- **OS**: Ubuntu 22.04 LTS (Native or via WSL2)
- **Python**: 3.9+
- **Flight Stack**: PX4 Autopilot & Gazebo Classic (SITL)
- **Libraries**: `pyautogen`, `mavsdk`, `openai`

### Installation Setup

```bash
# 1. Clone the environment
git clone https://github.com/zok213/Drone-Agents.git
cd Drone-Agents

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. PX4 & Gazebo Setup (Assuming Ubuntu 22.04)
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh

# 4. Launch the SITL Simulator
cd PX4-Autopilot
make px4_sitl gazebo
```

### Execution

To run the agent interaction loop, you must run the MavSDK server and the agent script concurrently.

```bash
# Terminal 1: Start MavSDK Server
mavsdk_server udp://:14540

# Terminal 2: Initialize the LLM Agent Framework
cd Agent-Drone
python3 main.py
```

---

## 🔮 Research Roadmap

To push the boundaries of embodied drone intelligence, the following features are actively being researched:
1. **Multi-Modal Visual State Injection**: Integrating ROS2 bridging to pipe real-time Gazebo camera feeds (RGB-D) into a Vision-Language Model (VLM) for spatial awareness and object-centric navigation.
2. **Dynamic Obstacle Avoidance**: Upgrading the Executor Agent with reactive state machines to override Planner commands if onboard telemetry detects collision hazards.
3. **End-to-End Voice Telemetry**: Integrating low-latency STT (Speech-to-Text) models directly into the agent pipeline for hands-free tactical field operations.

---

## 📚 Academic Citation & Collaboration

If you utilize this embodied agent framework in your research, please cite:
```bibtex
@software{drone_agent_2025,
  author = {Mai Phuoc Minh Tai},
  title = {DroneAgent: LLM-Driven Autonomous Drone Control System},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/zok213/Drone-Agents}
}
```

### Technical Support & Contact
- **GitHub**: [zok213](https://github.com/zok213)
- **Academic Support**: FPT University, Da Nang, Vietnam
- **License**: MIT License
