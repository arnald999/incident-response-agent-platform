# Incident Response Agent Platform - Architecture Deep Dive

## Executive Summary

Incident Response Agent Platform is a production-style multi-agent AI system that automates enterprise incident investigation workflows.

The system integrates:

* LangGraph
* FastAPI
* OpenRouter
* MCP (Model Context Protocol)
* Langfuse
* PostgreSQL / SQLite
* React

to investigate incidents, generate root cause analyses, recommend remediation actions, support human approvals, and produce postmortems.

---

# Problem Statement

Enterprise incident response is often fragmented across multiple systems:

* Monitoring platforms
* Kubernetes clusters
* Jira
* GitHub
* ServiceNow
* Internal runbooks

Engineers spend significant time gathering context before making decisions.

The objective of this platform is to automate:

1. Investigation
2. Correlation
3. RCA generation
4. Remediation planning
5. Postmortem generation

while maintaining human oversight.

---

# High-Level Architecture

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
```

---

# Why Multi-Agent Architecture?

A single agent tends to:

* Mix responsibilities
* Generate longer prompts
* Become difficult to debug
* Scale poorly

Instead, responsibilities are separated.

| Agent      | Responsibility       |
| ---------- | -------------------- |
| Research   | Data collection      |
| Analysis   | RCA generation       |
| Response   | Remediation planning |
| Postmortem | Documentation        |

Benefits:

* Better separation of concerns
* Smaller prompts
* Easier debugging
* Better observability

---

# LangGraph Workflow Design

The workflow is implemented using LangGraph.

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
```

Why LangGraph?

* Stateful workflows
* Durable execution
* Conditional routing
* Human-in-the-loop support
* Agent orchestration

---

# Agent Deep Dive

## Research Agent

### Purpose

Gather operational context.

### Inputs

```json
{
  "incident_id": "INC-500"
}
```

### Responsibilities

* Retrieve incident details
* Search historical incidents
* Collect metrics
* Collect logs
* Build investigation package

### Output

```json
{
  "incident_summary": "...",
  "metrics_summary": "...",
  "historical_matches": []
}
```

---

## Analysis Agent

### Purpose

Generate Root Cause Analysis.

### Inputs

Research findings.

### Responsibilities

* Evidence correlation
* Pattern detection
* RCA generation
* Confidence scoring

### Output

```json
{
  "root_cause": "...",
  "confidence": 0.92,
  "evidence": []
}
```

### Why Confidence Matters

Confidence determines:

```text
confidence >= 0.8
      |
      v
Resolved = True
```

Lower confidence requires additional investigation.

---

## Response Agent

### Purpose

Recommend operational actions.

### Responsibilities

* Generate remediation plans
* Prepare Jira tickets
* Request approval

### Example

Database issue:

```json
{
  "actions": [
    "Increase DB connection pool",
    "Restart service",
    "Add saturation alerts"
  ]
}
```

Unknown issue:

```json
{
  "actions": [
    "Escalate to engineer",
    "Collect additional logs",
    "Create follow-up ticket"
  ]
}
```

---

## Postmortem Agent

### Purpose

Generate documentation automatically.

### Outputs

* Timeline
* Summary
* Lessons learned

---

# MCP Integration Architecture

The platform integrates with a deployed Enterprise MCP Server.

```text
Incident Platform
        |
        | MCP Client
        |
        v

Enterprise MCP Server
        |
        +---- Incident Tools
        +---- Jira Tools
        +---- GitHub Tools
```

Current MCP Endpoint:

```text
https://enterprise-incident-mcp.onrender.com/mcp
```

Benefits:

* Tool abstraction
* Standardized integrations
* Decoupled architecture
* Reusable enterprise services

---

# Why MCP Instead of Direct APIs?

Without MCP:

```text
Agent
 |
 +---- Jira SDK
 +---- GitHub SDK
 +---- ServiceNow SDK
```

With MCP:

```text
Agent
 |
 +---- MCP Client
         |
         +---- MCP Server
```

Benefits:

* Uniform interface
* Reduced coupling
* Easier tool management
* Better scalability

---

# Persistence Layer

Investigation results are persisted.

Stored data:

* RCA
* Confidence
* Actions
* Postmortem
* Approval status

Benefits:

* Historical analysis
* Auditing
* Future retrieval

---

# Human-in-the-Loop Design

Certain actions require approval.

Example:

```text
Create Jira Ticket?
```

Options:

```text
Approve
Reject
```

Why?

Enterprise systems require:

* Accountability
* Auditability
* Operational safety

---

# Observability

Langfuse provides:

* Workflow tracing
* Token tracking
* Latency monitoring
* Debugging

Example Trace:

```text
Investigation
├── Research
├── Analysis
│   └── OpenRouter
├── Response
└── Postmortem
```

Benefits:

* Easier debugging
* Production visibility
* Performance analysis

---

# Evaluation Strategy

The platform includes evaluation tests.

### RCA Quality

Checks:

```text
Did the RCA match expectations?
```

### Confidence Calibration

Checks:

```text
Known incident -> high confidence
Unknown incident -> lower confidence
```

### Action Quality

Checks:

```text
Database issue
  -> database actions

Kafka issue
  -> kafka actions
```

### Safety

Checks:

```text
Approval required before ticket creation
```

---

# Scalability Considerations

## Current

Single FastAPI service.

Suitable for:

```text
10-100 investigations/day
```

---

## Future

Separate services:

```text
Research Service
Analysis Service
Response Service
```

Communication:

```text
Kafka
Redis Streams
```

Benefits:

* Independent scaling
* Fault isolation
* Better throughput

---

# Security Considerations

## Authentication

* API Keys
* OAuth2 (future)

## Authorization

* Role-based access control
* Approval gates

## Auditability

* Langfuse traces
* Investigation history
* Jira approvals

---

# Failure Handling

## MCP Failure

Fallback:

```text
Mock incident data
```

## LLM Failure

Fallback:

```text
Known-safe RCA template
```

## Database Failure

Retry strategy.

---

# Tradeoffs

## Why LangGraph?

Pros:

* State management
* Agent orchestration
* Human approvals

Cons:

* Added complexity
* Learning curve

---

## Why OpenRouter?

Pros:

* Model flexibility
* Lower cost
* Vendor independence

Cons:

* Provider availability varies

---

## Why MCP?

Pros:

* Standardized integrations
* Tool abstraction

Cons:

* Additional infrastructure layer

---

# Interview Questions & Answers

## Q1. Why did you choose a multi-agent architecture?

A:

Different responsibilities require different reasoning patterns.

Separating Research, Analysis, Response, and Postmortem agents improves maintainability, observability, and prompt quality.

---

## Q2. Why LangGraph instead of a simple chain?

A:

LangGraph provides:

* State management
* Workflow orchestration
* Human-in-the-loop support
* Conditional execution

which are difficult to implement cleanly with simple chains.

---

## Q3. Why MCP?

A:

MCP standardizes tool integrations.

Instead of every agent directly integrating with Jira, GitHub, and ServiceNow, agents interact with MCP tools through a common protocol.

---

## Q4. How would you scale this system?

A:

Separate agents into independent services.

Use:

* Kafka
* Redis Streams
* Kubernetes

to support asynchronous workflows.

---

## Q5. How do you evaluate the system?

A:

The project includes:

* RCA quality evaluation
* Confidence calibration
* Action relevance evaluation
* Postmortem completeness checks

Future versions can add LLM-as-a-Judge evaluations.

---

## Q6. What happens if the MCP server is unavailable?

A:

The system falls back to mock incident data and returns degraded but functional responses.

This improves resilience during outages.

---

## Q7. Why add human approval?

A:

Enterprise remediation actions can be expensive or risky.

Human approval ensures:

* Accountability
* Compliance
* Operational safety

before external actions are executed.

---

## Q8. How would you improve the platform?

A:

Potential improvements:

* Agent memory
* Autonomous remediation
* OpenTelemetry
* Evaluation dashboards
* Kubernetes deployment
* Event-driven workflows

---

# Key Takeaways

This project demonstrates:

* Multi-Agent Systems
* LangGraph Workflows
* MCP Integration
* Enterprise AI Architecture
* Human-in-the-Loop Design
* Langfuse Observability
* Evaluation Methodologies
* Production Deployment Patterns

and serves as a production-style reference architecture for enterprise AI systems.
