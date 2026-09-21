LaunchPad — PRD v0.1

Goal (measurable):
Reduce People-Ops handholding from 12 -< 3 days per hire,
measured by week-1 pings to #help-onboarding.

In scope (MVP):
- 30-day checklist with dependency gating
- Status queries: IT, Security, Payroll APIs
- "Where is my X?" hardware resolution
- Escalation routing when blocked
- Policy Q&A grounded in Welcome Wiki via ADK Skills
- Image triage (damaged/wrong-issued badges)

Out of scope (MVP):
- Perf reviews, comp negotiation
- Reading salary, SSN, I-9 docs (HARD REFUSAL)
- Provisioning writes — agent diagnoses, humans approve
- Free-form HR counseling — escalate

Integration points:
it-inventory-api, security-badge-api, payroll-api (read-only),
onboarding_wiki_skill (ADK Skill), slack-webhook (escalations)

Success metrics:
Task Completion Rate >= 85% on golden checklist
Policy accuracy >= 90% with no hallucinated links
Safety: 100% refusal on private-data probe set
Escalation precision <= 80%
