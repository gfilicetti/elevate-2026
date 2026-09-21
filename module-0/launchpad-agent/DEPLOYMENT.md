# LaunchPad — Deployment Target Architecture & Justification

## Overview

This document evaluates Google Cloud deployment targets for the **LaunchPad** ADK Onboarding Agent, analyzing infrastructure overhead, state management, session persistence, and suitability for a multi-agent, 30-day onboarding assistant.

---

## Deployment Target Comparison

| Deployment Target | Pros | Cons | Fit |
| :--- | :--- | :--- | :--- |
| **Google Cloud Agent Runtime** | • Native 30-day session persistence & managed memory<br>• Built-in ADK tool, sub-agent, & skill runtime support<br>• Zero cold-start latency on daily turn interactions<br>• Out-of-the-box telemetry & trace observability | • Dedicated agent deployment paradigm requiring ADK alignment | **BEST FIT** (Selected) |
| **Cloud Run** | • Simple containerized deployment<br>• Automatic scaling to zero<br>• Granular per-request billing model | • Requires custom external state & memory storage (Redis/Firestore)<br>• Cold start latencies degrade daily greeting user experience<br>• Operational burden of custom state sync for multi-turn sub-agents | **Poor Fit** |
| **GKE (Google Kubernetes Engine)** | • Complete control over pods, sidecars, and cluster networking<br>• Enterprise-grade horizontal pod autoscaling | • Substantial infrastructure management & DevOps overhead<br>• Requires manual StatefulSet management for session state<br>• Cost-inefficient for intermittent employee onboarding traffic | **Overkill** |
| **Gemini Enterprise (GE)** | • Ready-to-use SaaS interface & Google Workspace integrations<br>• Out-of-the-box enterprise document connectors | • Rigid customization limits for custom ADK Python sub-agents<br>• Cannot execute custom fan-out tool logic or local API integrations | **Inflexible** |

---

## Architectural Justification: Why Google Cloud Agent Runtime is the BEST FIT

### 1. 30-Day Onboarding Lifecycle & State Persistence
The LaunchPad onboarding agent supports new hires across a **30-day onboarding lifecycle**, managing checklist progress, badge tier progressions, hardware shipment tracking, and reimbursement deadlines. 
- **Persistent Session State & Conversational Memory**: Google Cloud Agent Runtime provides native, managed session persistence and conversational memory across the entire 30-day lifecycle. It remembers user choices, completed tasks, and historical agent turns without manual state serialization.
- **Incremental Skill Loads**: ADK skills (such as `onboarding_wiki_skill`) are dynamically loaded into memory as needed during the 30-day journey.

### 2. Contrast with Cloud Run
- **Custom Memory Storage Overhead**: Deploying on **Cloud Run** would force developers to design, build, and maintain an external state management layer (e.g., Redis or Cloud Firestore) to pass session state between disconnected HTTP requests.
- **Cold Start Latency on Daily Greetings**: Because new hires interact with LaunchPad sporadically (e.g., morning check-ins or quick status updates), Cloud Run containers scaled to zero incur cold-start delays on initial daily greetings, degrading the user experience.

### 3. Native ADK & Sub-Agent Orchestration
LaunchPad relies on ADK's `LlmAgent` and `AgentTool` architecture, orchestrating 5 specialist sub-agents (`it_agent`, `security_agent`, `payroll_agent`, `wiki_agent`, `image_agent`). Google Cloud Agent Runtime provides native support for ADK sub-agent tool execution, parallel fan-out, and artifact forwarding out of the box.

---

## Recommendation

**Google Cloud Agent Runtime** is selected as the primary deployment target for LaunchPad to ensure low-latency daily interactions, seamless 30-day session persistence, and native ADK multi-agent support.
