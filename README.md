# Incident Response Agent Platform

## Overview

Incident Response Agent Platform is a multi-agent AI system designed to automate enterprise incident investigation and response workflows.

The platform leverages:

* LangGraph
* FastAPI
* OpenRouter / OpenAI-compatible models
* Multi-Agent Architecture
* PostgreSQL
* Docker
* Enterprise Tool Integrations

to create an intelligent operational assistant capable of:

* Investigating incidents
* Gathering operational context
* Producing root-cause analyses
* Recommending remediation actions
* Generating postmortems

---

# Features

## Multi-Agent Workflow

### Research Agent

Responsible for:

* Collecting incident details
* Gathering metrics
* Searching historical incidents
* Building investigation context

### Analysis Agent

Responsible for:

* Root Cause Analysis (RCA)
* Confidence scoring
* Evidence correlation
* Pattern detection

Powered by OpenRouter-compatible LLMs.

### Response Agent

Responsible for:

* Remediation recommendations
* Jira ticket preparation
* Human approval workflows

### Postmortem Agent

Responsible for:

* Timeline generation
* Incident summary creation
* Lessons learned generation

---

# Architecture

```text
                    +----------------------+
                    |      FastAPI API     |
                    +----------+-----------+
                               |
                               v

                    +----------------------+
                    |      LangGraph       |
                    |     Orchestrator     |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v

   Research Agent     Analysis Agent     Response Agent
          |
          +--------------------+
                               |
                               v

                     Postmortem Agent
                               |
                               v

                        Final Report
```

---

# Current Workflow

```text
Incident Request
       |
       v

Research Agent
       |
       v

Analysis Agent
       |
       v

Response Agent
       |
       v

Human Approval
       |
       v

Postmortem Agent
       |
       v

Persist Investigation
       |
       v

Return Report
```

---

# Technology Stack

## Backend

* Python 3.12
* FastAPI
* LangGraph
* LangChain Core

## AI Models

* OpenRouter
* OpenAI Compatible APIs

## Database

* PostgreSQL
* SQLAlchemy
* AsyncPG

## Infrastructure

* Docker
* Docker Compose

## Testing

* Pytest

---

# Project Structure

```text
incident-response-agent-platform/

├── backend/
│
├── agents/
│   ├── research_agent.py
│   ├── analysis_agent.py
│   ├── response_agent.py
│   └── postmortem_agent.py
│
├── api/
│   └── incident_routes.py
│
├── graph/
│   ├── workflow.py
│   └── state.py
│
├── repositories/
│   └── investigation_repository.py
│
├── models/
│   └── investigation.py
│
├── services/
│   └── llm.py
│
├── tools/
│   └── mcp_client.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# Setup

## Prerequisites

* Python 3.12+
* uv
* Docker Desktop

---

# Install Dependencies

```powershell
uv sync
```

---

# Environment Variables

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key_here

OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

MODEL_NAME=openrouter/free

DATABASE_URL=sqlite+aiosqlite:///./incident_platform.db
```

---

# Run Locally

```powershell
uv run uvicorn backend.main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# Run with Docker

```powershell
docker compose up --build
```

---

# API Examples

## Health Check

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/health `
  -Method GET
```

---

## Investigate Incident

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/incidents/INC-500/investigate `
  -Method POST |
ConvertTo-Json -Depth 10
```

Example Response:

```json
{
  "incident_id": "INC-500",
  "resolved": true,
  "research_findings": {},
  "rca_report": {},
  "action_plan": {},
  "postmortem": {}
}
```

---

## Get Investigation

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/incidents/INC-500 `
  -Method GET |
ConvertTo-Json -Depth 10
```

---

## List Investigations

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/incidents `
  -Method GET |
ConvertTo-Json -Depth 10
```

---

## Approve Jira Ticket

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/incidents/INC-500/approve-jira `
  -Method POST |
ConvertTo-Json -Depth 10
```

---

# Testing

Run tests:

```powershell
uv run pytest
```

Run a specific test file:

```powershell
uv run pytest backend/tests/test_incident_api.py
```

---

# Current MCP Integration

The current implementation contains a mocked MCP layer.

Supported operations:

```python
get_incident()

search_incidents()

create_jira_ticket()
```

Future versions will connect to a real MCP server.

---

# Example Investigation

Input:

```text
Investigate incident INC-500
```

Research Agent:

```text
DB connections 98%
Connection timeout errors observed
Historical matches found
```

Analysis Agent:

```json
{
  "root_cause": "Database connection pool exhaustion",
  "confidence": 0.93
}
```

Response Agent:

```json
{
  "severity": "critical",
  "actions": [
    "Restart pods",
    "Increase DB connection pool"
  ]
}
```

Postmortem Agent:

```text
Timeline
Lessons Learned
Incident Summary
```

---

# Roadmap

## Phase 2

* Real MCP Server Integration
* Langfuse Tracing
* OpenTelemetry
* Better Agent Memory

## Phase 3

* React Dashboard
* Investigation Timeline UI
* Human Approval UI

## Phase 4

* Evaluation Harness
* Golden Datasets
* Regression Testing

## Phase 5

* Autonomous Remediation
* Event-Driven Workflows
* Self-Healing Infrastructure

---

# Learning Outcomes

This project demonstrates:

* Multi-Agent Systems
* LangGraph Workflows
* Enterprise AI Architecture
* Human-in-the-Loop Design
* FastAPI Development
* OpenRouter Integration
* PostgreSQL Persistence
* Docker Deployment

---

# Portfolio Value

This project showcases:

* Agent Engineering
* Enterprise AI Integration
* LangGraph Expertise
* Operational Automation
* Production Backend Design

and serves as a strong portfolio project for Forward Deployed Engineer, AI Engineer, Platform Engineer, and Applied AI roles.
