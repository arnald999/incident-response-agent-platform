from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_investigate_incident():
    response = client.post(
        "/incidents/INC-500/investigate",
        json={
            "alert_details": {
                "source": "prometheus",
                "severity": "critical",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["incident_id"] == "INC-500"
    assert "research_findings" in data
    assert "rca_report" in data
    assert "action_plan" in data
    assert "postmortem" in data
    assert data["resolved"] is True


def test_approve_jira_after_investigation():
    client.post("/incidents/INC-500/investigate")

    response = client.post("/incidents/INC-500/approve-jira")

    assert response.status_code == 200

    data = response.json()

    assert data["incident_id"] == "INC-500"
    assert data["status"] == "approved"
    assert data["jira_ticket"]["ticket_id"] == "JIRA-100"