# Incident Response Agent Platform

## Overview

Incident Response Agent Platform is a production-grade multi-agent AI system designed to automate enterprise incident investigation and response workflows.

The platform combines:

* LangGraph
* FastAPI
* OpenRouter
* MCP (Model Context Protocol)
* Langfuse
* React
* PostgreSQL / SQLite
* Docker

to create an intelligent operational assistant capable of:

* Investigating incidents
* Gathering operational context
* Correlating evidence
* Producing Root Cause Analysis (RCA)
* Recommending remediation actions
* Supporting human approvals
* Generating postmortems

---

## Features

### Multi-Agent Workflow

#### Research Agent

Responsible for:

* Retrieving incident context from MCP tools
* Collecting metrics and logs
* Searching historical incidents
* Building investigation evidence

#### Analysis Agent

Responsible for:

* Root Cause Analysis (RCA)
* Confidence scoring
* Evidence correlation
* Pattern detection

Powered by OpenRouter-compatible LLMs.

#### Response Agent

Responsible for:

* Remediation recommendations
* Jira ticket preparation
* Human approval workflows
* Context-aware action planning

#### Postmortem Agent

Responsible for:

* Timeline generation
* Incident summary creation
* Lessons learned generation

---

## Architecture

```text
                         +----------------------+
                         |   React Dashboard    |
                         +----------+-----------+
                                    |
                                    v

                         +----------------------+
                         |       FastAPI        |
                         +----------+-----------+
                                    |
                                    v

                         +----------------------+
                         |      LangGraph       |
                         |     Orchestrator     |
                         +----------+-----------+
                                    |
       +----------------------------+----------------------------+
       |                            |                            |
       v                            v                            v

Research Agent            Analysis Agent              Response Agent
       |                         |                            |
       |                         |                            |
       +-------------------------+----------------------------+
                                    |
                                    v

                          Postmortem Agent
                                    |
                                    v

                           Investigation DB
                                    |
                                    v

                            Langfuse Tracing
                                    |
                                    v

                         Enterprise MCP Server
                                    |
       +----------------------------+----------------------------+
       |                            |                            |
       v                            v                            v

    Incidents                    Jira                       GitHub
```

---

## Workflow

```text
User Request
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

Return Investigation Report
```

---

## MCP Integration

This platform integrates with a deployed Enterprise MCP Server.

### MCP Endpoint

```text
https://enterprise-incident-mcp.onrender.com/mcp
```

### Available MCP Tools

* create_incident
* list_incidents
* get_incident
* update_incident
* assign_incident
* get_incident_timeline
* search_incidents
* find_similar_incidents
* generate_postmortem
* create_jira_ticket
* create_github_issue
* build_incident_context
* generate_incident_rca
* index_incident
* semantic_search
* investigate_incident

The platform consumes these tools through a real FastMCP client implementation.

---

## Human-in-the-Loop Support

The platform supports approval gates before taking remediation actions.

Example:

```text
Should I create a Jira ticket?

[Approve]
[Reject]
```

This mirrors real enterprise operational workflows where AI recommendations require human validation before execution.

---

## Observability

Langfuse is integrated for:

* Workflow tracing
* LLM observability
* Token tracking
* Latency monitoring
* Debugging and evaluation

Each investigation execution is captured as a trace.

---

## Frontend Dashboard

The React dashboard supports:

* Incident investigation
* Investigation history
* Investigation details
* Human approval workflows
* Jira approval actions

---

## Technology Stack

### Frontend

* React
* TypeScript
* Material UI
* React Query
* Axios

### Backend

* Python 3.12
* FastAPI
* LangGraph
* LangChain Core

### AI

* OpenRouter
* OpenAI-Compatible APIs

### Database

* PostgreSQL
* SQLite
* SQLAlchemy

### Infrastructure

* Docker
* Docker Compose

### Observability

* Langfuse

### Testing

* Pytest

---

## Project Structure

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
├── observability/
│   └── langfuse.py
│
├── frontend/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Setup

### Prerequisites

* Python 3.12+
* uv
* Docker Desktop

---

## Install Dependencies

```powershell
uv sync
```

---

## Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=google/gemma-3n-e4b-it:free

DATABASE_URL=sqlite+aiosqlite:///./incident_platform.db

USE_REAL_MCP=true
MCP_SERVER_URL=https://enterprise-incident-mcp.onrender.com/mcp

LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
LANGFUSE_TRACING_ENVIRONMENT=incident-response-dev
```

---

## Run Backend

```powershell
uv run uvicorn backend.main:app --port 8010 --reload
```

Swagger UI:

```text
http://localhost:8010/docs
```

---

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Run with Docker

```powershell
docker compose up --build
```

---

## API Examples

### Health Check

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8010/health `
  -Method GET
```

---

### Investigate Incident

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8010/incidents/INC-500/investigate `
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

### Get Investigation

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8010/incidents/INC-500 `
  -Method GET |
ConvertTo-Json -Depth 10
```

---

### List Investigations

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8010/incidents `
  -Method GET |
ConvertTo-Json -Depth 10
```

---

### Approve Jira Ticket

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8010/incidents/INC-500/approve-jira `
  -Method POST |
ConvertTo-Json -Depth 10
```

---

## Example Investigation

### Input

```text
Investigate incident INC-500
```

### Research Agent Output

```text
DB connections at 98%
Connection timeout errors observed
Historical matches found
```

### Analysis Agent Output

```json
{
  "root_cause": "Database connection pool exhaustion",
  "confidence": 0.92
}
```

### Response Agent Output

```json
{
  "severity": "critical",
  "actions": [
    "Restart affected service pods",
    "Increase database connection pool size",
    "Add alert for DB connection usage above 85%"
  ]
}
```

### Postmortem Output

```text
Timeline
Lessons Learned
Incident Summary
```

---

## Evaluation Strategy

The platform can be evaluated using:

* RCA quality
* Confidence calibration
* Resolution quality
* Investigation latency
* Tool success rate

Metrics are observable through Langfuse traces.

---

## Security

### Authentication

* API Keys
* Environment-based configuration

### Authorization

* Human approval workflow
* MCP tool access controls

### Auditability

* Investigation persistence
* Langfuse trace history
* Jira approval tracking

---

## Testing

Run all tests:

```powershell
uv run pytest
```

Run a specific test file:

```powershell
uv run pytest backend/tests/test_incident_api.py
```

---

## Current Status

### Completed

* Multi-Agent Workflow
* LangGraph Orchestration
* OpenRouter Integration
* React Dashboard
* Investigation Persistence
* Human Approval Workflow
* Real MCP Integration
* Langfuse Observability
* Docker Support
* Automated Testing

### Planned Enhancements

* Agent-Level Langfuse Spans
* Evaluation Harness
* OpenTelemetry Integration
* Kubernetes Deployment
* Autonomous Remediation

---

## Learning Outcomes

This project demonstrates:

* Multi-Agent Systems
* Agent Orchestration
* LangGraph Workflows
* MCP Integration
* Enterprise AI Architecture
* Human-in-the-Loop Design
* FastAPI Development
* OpenRouter Integration
* Langfuse Observability
* Production Deployment Patterns

---

## Portfolio Value

This project showcases:

* Agent Engineering
* Enterprise AI Integration
* MCP Expertise
* LangGraph Expertise
* Operational Automation
* Production Backend Design
* AI Observability

and serves as a flagship portfolio project for:

* Forward Deployed Engineer (FDE)
* AI Engineer
* Platform Engineer
* Applied AI Engineer
* AI Solutions Architect
* Enterprise AI Consultant
