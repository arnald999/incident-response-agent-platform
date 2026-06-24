import axios from "axios";

const API_BASE_URL = "http://localhost:8010";

export async function investigateIncident(incidentId: string) {
  const response = await axios.post(
    `${API_BASE_URL}/incidents/${incidentId}/investigate`,
    {
      alert_details: {
        source: "dashboard",
        severity: "critical",
      },
    }
  );

  return response.data;
}

export async function listInvestigations() {
  const response = await axios.get(`${API_BASE_URL}/incidents`);
  return response.data;
}

export async function approveJira(incidentId: string) {
  const response = await axios.post(
    `${API_BASE_URL}/incidents/${incidentId}/approve-jira`
  );

  return response.data;
}

export async function getInvestigation(incidentId: string) {
  const response = await axios.get(`${API_BASE_URL}/incidents/${incidentId}`);
  return response.data;
}
