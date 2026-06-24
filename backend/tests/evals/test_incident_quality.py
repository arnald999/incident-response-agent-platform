import pytest

from backend.agents.analysis_agent import normalize_confidence
from backend.agents.response_agent import build_actions
from backend.schemas.analysis import RCAReport
from backend.schemas.postmortem import Postmortem


def contains_any(text: str, terms: list[str]) -> bool:
    text = text.lower()
    return any(term.lower() in text for term in terms)


@pytest.mark.parametrize(
    "raw,expected",
    [
        (0.92, 0.92),
        (92, 0.92),
        (70, 0.70),
    ],
)
def test_confidence_normalization(raw, expected):
    assert normalize_confidence(raw) == expected


@pytest.mark.parametrize(
    "root_cause,expected_terms",
    [
        (
            "Database connection pool exhaustion caused request timeouts.",
            ["database", "connection"],
        ),
        (
            "Kafka consumer lag caused delayed message processing.",
            ["kafka", "consumer"],
        ),
        (
            "JWT validation service unavailable.",
            ["auth", "jwt"],
        ),
        (
            "Redis cache memory pressure caused evictions.",
            ["redis", "cache"],
        ),
        (
            "Infrastructure anomaly with limited evidence.",
            ["escalate", "logs", "traces"],
        ),
    ],
)
def test_context_aware_remediation_actions(root_cause, expected_terms):
    actions = " ".join(build_actions(root_cause))

    assert contains_any(actions, expected_terms)


def test_unknown_incident_confidence_policy():
    report = RCAReport(
        root_cause="Infrastructure anomaly with limited evidence.",
        confidence=normalize_confidence(70),
        evidence=[
            "Infrastructure anomaly detected",
            "No detailed logs available",
        ],
    )

    assert report.confidence < 0.8


def test_postmortem_shape_quality():
    postmortem = Postmortem(
        summary="Incident caused by database connection pool exhaustion.",
        timeline=[
            "Alert triggered",
            "Research agent gathered incident context",
            "Analysis agent identified probable root cause",
        ],
        lessons_learned=[
            "Alert earlier on DB connection pressure",
            "Review autoscaling and database pool limits",
        ],
    )

    assert postmortem.summary
    assert len(postmortem.timeline) >= 3
    assert len(postmortem.lessons_learned) >= 2