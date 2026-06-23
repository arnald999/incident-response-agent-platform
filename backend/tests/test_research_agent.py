import pytest

from backend.agents.research_agent import research_agent


@pytest.mark.asyncio
async def test_research_agent():
    result = await research_agent(
        {
            "incident_id": "INC-500"
        }
    )

    assert "research_findings" in result