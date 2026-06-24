import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  approveJira,
  getInvestigation,
  investigateIncident,
  listInvestigations,
} from "../api/incidentApi";

export function Dashboard() {
  const [incidentId, setIncidentId] = useState("INC-500");
  const [result, setResult] = useState<any>(null);
  const [jiraResult, setJiraResult] = useState<any>(null);

  const investigationsQuery = useQuery({
    queryKey: ["investigations"],
    queryFn: listInvestigations,
  });

  const investigateMutation = useMutation({
    mutationFn: investigateIncident,
    onSuccess: (data) => {
      setResult(data);
      setJiraResult(null);
      investigationsQuery.refetch();
    },
  });

  const approveJiraMutation = useMutation({
    mutationFn: approveJira,
    onSuccess: (data) => {
      setJiraResult(data);
    },
  });

  const getInvestigationMutation = useMutation({
    mutationFn: getInvestigation,
    onSuccess: (data) => {
      setResult(data);
      setJiraResult(null);
    },
  });

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Incident Response Agent Platform
        </Typography>

        <Typography variant="body1" color="text.secondary" gutterBottom>
          Multi-agent incident investigation powered by FastAPI, LangGraph, and
          OpenRouter.
        </Typography>

        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Stack direction="row" spacing={2}>
              <TextField
                label="Incident ID"
                value={incidentId}
                onChange={(event) => setIncidentId(event.target.value)}
                fullWidth
              />

              <Button
                variant="contained"
                onClick={() => investigateMutation.mutate(incidentId)}
                disabled={investigateMutation.isPending}
              >
                Investigate
              </Button>
            </Stack>

            {investigateMutation.isError && (
              <Alert severity="error" sx={{ mt: 2 }}>
                Failed to investigate incident.
              </Alert>
            )}
          </CardContent>
        </Card>

        {result && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Stack direction="row" spacing={1} alignItems="center">
                <Typography variant="h5">Investigation Result</Typography>
                <Chip
                  label={result.resolved ? "Resolved" : "Unresolved"}
                  color={result.resolved ? "success" : "warning"}
                />
              </Stack>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6">Root Cause</Typography>
              <Typography>{result.rca_report.root_cause}</Typography>

              <Typography variant="h6" sx={{ mt: 2 }}>
                Confidence
              </Typography>
              <Typography>{result.rca_report.confidence}</Typography>

              <Typography variant="h6" sx={{ mt: 2 }}>
                Evidence
              </Typography>
              <ul>
                {result.rca_report.evidence.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>

              <Typography variant="h6" sx={{ mt: 2 }}>
                Recommended Actions
              </Typography>
              <ul>
                {result.action_plan.actions.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>

              <Button
                variant="outlined"
                sx={{ mt: 2 }}
                onClick={() => approveJiraMutation.mutate(result.incident_id)}
                disabled={approveJiraMutation.isPending}
              >
                Approve Jira
              </Button>

              {jiraResult && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  Jira ticket created: {jiraResult.jira_ticket.ticket_id}
                </Alert>
              )}
            </CardContent>
          </Card>
        )}

        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h5">Saved Investigations</Typography>

            <Divider sx={{ my: 2 }} />

            {investigationsQuery.data?.incident_ids?.length ? (
              <Stack direction="row" spacing={1} flexWrap="wrap">
                {investigationsQuery.data.incident_ids.map((id: string) => (
                  <Chip
                    key={id}
                    label={id}
                    clickable
                    onClick={() => getInvestigationMutation.mutate(id)}
                  />
                ))}
              </Stack>
            ) : (
              <Typography color="text.secondary">
                No investigations saved yet.
              </Typography>
            )}
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
}