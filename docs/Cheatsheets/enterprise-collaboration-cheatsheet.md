# Enterprise Collaboration Cheatsheet

## Jira Workflows & Querying (JQL)

Jira Query Language (JQL) is used to find, organize, and filter tasks.

```jql
-- 1. Find all active SRE/DevOps bugs in the current Sprint
project = "SRE" AND issuetype = Bug AND status IN ("In Progress", "Code Review") AND sprint in openSprints()

-- 2. Find high priority items overdue / not updated in the last 7 days
priority in (Highest, High) AND updatedDate < -7d AND resolution = Unresolved

-- 3. Filter by specific custom labels or epic links
"Epic Link" = SRE-452 AND label = "infrastructure-cost"
```

---

## ServiceNow (ITIL Administration)

ServiceNow is the industry-standard IT Service Management (ITSM) platform for Incident, Problem, Change, and Configuration Management.

- **Incident State Flow:** `New` -> `In Progress` -> `On Hold` (requires holds cause) -> `Resolved` -> `Closed`.
- **Change Management Types:**
  - **Standard Change:** Pre-approved, low-risk, repetitive (e.g., adding disk space to a development VM).
  - **Normal Change:** Requires full CAB (Change Advisory Board) review and approval cycle.
  - **Emergency Change:** Initiated due to an active high-severity incident; approved quickly by ECAB.
- **REST API Endpoint Example:**
  ```http
  GET https://your-instance.service-now.com/api/now/table/incident?sysparm_limit=10&sysparm_query=active=true^priority=1
  ```
