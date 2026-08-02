---
layout: default
title: "Enterprise Collaboration Cheatsheet"
---

# Enterprise Collaboration Cheatsheet

---

## 1. Jira Query Language (JQL) & Workflows

Jira Query Language (JQL) is used to find, organize, and filter tasks across teams and projects.

```jql
-- 1. Find all active SRE/DevOps bugs in the current Sprint
project = "SRE" AND issuetype = Bug AND status IN ("In Progress", "Code Review") AND sprint in openSprints()

-- 2. Find high priority items overdue / not updated in the last 7 days
priority in (Highest, High) AND updatedDate < -7d AND resolution = Unresolved

-- 3. Filter by specific custom labels or epic links
"Epic Link" = SRE-452 AND label = "infrastructure-cost"

-- 4. Advanced: Find issues assigned to you that were resolved in the last 14 days
assignee = currentUser() AND status changed TO Resolved BY currentUser() during (-14d, now())

-- 5. SLA breaches tracking for service desk projects
project = "ITSD" AND "Time to first response" = elapsed() AND "Time to resolution" = breached()
```

### Jira Workflow Automation JSON Payload Model
When automating Jira transitions using webhooks, Jira sends/receives standard structures:
```json
{
  "transition": {
    "id": "101",
    "name": "Move to In Progress"
  },
  "fields": {
    "assignee": {
      "id": "5b10ac8d82e05b22cc7d4ef5"
    },
    "comment": [
      {
        "add": {
          "body": "Automated transition triggered by Jenkins CI/CD pipeline completion."
        }
      }
    ]
  }
}
```

---

## 2. ServiceNow (ITIL Administration)

ServiceNow is the industry-standard IT Service Management (ITSM) platform for Incident, Problem, Change, and Configuration Management.

- **Incident State Flow:** `New` (1) -> `In Progress` (2) -> `On Hold` (3) (requires hold reason) -> `Resolved` (6) -> `Closed` (7).
- **Change Management Types:**
  - **Standard Change:** Pre-approved, low-risk, repetitive (e.g., adding disk space to a development VM).
  - **Normal Change:** Requires full CAB (Change Advisory Board) review and approval cycle.
  - **Emergency Change:** Initiated due to an active high-severity incident; approved quickly by ECAB.

### ServiceNow Server-Side GlideRecord Query (Javascript)
Used in Script Includes or Business Rules to query records:
```javascript
var gr = new GlideRecord('incident');
gr.addActiveQuery();
gr.addQuery('priority', '1');
gr.addQuery('state', '!=', '3'); // Not on hold
gr.query();
while (gr.next()) {
    gs.log('Active Priority 1 Incident: ' + gr.number + ' - ' + gr.short_description);
}
```

### REST API Endpoint Example:
```http
GET https://your-instance.service-now.com/api/now/table/incident?sysparm_limit=10&sysparm_query=active=true^priority=1
Headers:
  Accept: application/json
  Authorization: Basic <base64encoded_credentials>
```

---

## 3. Confluence Cloud REST API v2

Manage Confluence pages, spaces, and content programmatically using raw HTTP requests.

### Retrieve Page with Storage Format (HTML):
```http
GET https://your-domain.atlassian.net/wiki/api/v2/pages/123456789?body-format=storage
Headers:
  Authorization: Bearer <your_token>
```

### Create a New Page:
```http
POST https://your-domain.atlassian.net/wiki/api/v2/pages
Headers:
  Content-Type: application/json
  Authorization: Bearer <your_token>

{
  "spaceId": "851969",
  "status": "current",
  "title": "SRE On-Call Runbook: Database Failover",
  "parentId": "123456",
  "body": {
    "representation": "storage",
    "value": "<p>This is the official database failover runbook. In case of failure:</p><ac:structured-macro ac:name=\"info\"><ac:parameter ac:name=\"title\">Alert</ac:parameter><ac:rich-text-body><p>Do not run manual commands without checking logs first!</p></ac:rich-text-body></ac:structured-macro>"
  }
}
```

---

## 4. Slack Webhooks & Block Kit

Integrate automation bots directly with Slack to output rich formatted messages and interactive layouts.

### Incoming Webhook JSON Payload (Block Kit Format):
```json
{
  "channel": "#alerts-ops",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 Production Incident Detected",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Severity:*\nCritical (P1)"
        },
        {
          "type": "mrkdwn",
          "text": "*Service:*\nAuth-API Gateway"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Error logs count exceeded 500/min.* Click below to inspect in Datadog."
      },
      "accessory": {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "Inspect Logs",
          "emoji": true
        },
        "value": "click_me_123",
        "url": "https://datadog.example.com/incidents/123",
        "action_id": "button-action"
      }
    }
  ]
}
```

---

## 5. Microsoft Teams Adaptive Cards

Adaptive Cards are standard JSON-serialized card layouts used to post notifications to MS Teams.

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "🚀 Deployment Completed Successfully",
      "weight": "Bolder",
      "size": "Medium",
      "color": "Good"
    },
    {
      "type": "FactSet",
      "facts": [
        {
          "title": "Environment:",
          "value": "Production-US-East"
        },
        {
          "title": "Version:",
          "value": "v2.14.0"
        },
        {
          "title": "Deployer:",
          "value": "Github Actions (run #481)"
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View Release Notes",
      "url": "https://github.com/org/repo/releases/tag/v2.14.0"
    }
  ]
}
```
