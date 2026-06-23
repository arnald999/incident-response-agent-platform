from langgraph.graph import END, StateGraph

from backend.agents.analysis_agent import analysis_agent
from backend.agents.postmortem_agent import postmortem_agent
from backend.agents.research_agent import research_agent
from backend.agents.response_agent import response_agent
from backend.graph.state import IncidentState


def build_workflow():
    graph = StateGraph(IncidentState)

    graph.add_node("research", research_agent)
    graph.add_node("analysis", analysis_agent)
    graph.add_node("response", response_agent)
    graph.add_node("postmortem", postmortem_agent)

    graph.set_entry_point("research")

    graph.add_edge("research", "analysis")
    graph.add_edge("analysis", "response")
    graph.add_edge("response", "postmortem")
    graph.add_edge("postmortem", END)

    return graph.compile()


incident_workflow = build_workflow()