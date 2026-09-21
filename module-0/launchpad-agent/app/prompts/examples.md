# LaunchPad Few-Shot Multi-Agent Workflow Examples

## Example 1: Turn 1 Parallel Fan-out & Active Blocker Surfacing

**User**:
Hi LaunchPad! I'm Maya Chen (EMP-1042), today is my first day. Can you check my onboarding status?

**Orchestrator Actions**:
1. Concurrently call `it_agent(request="Get hardware order, SSO status, and shipping info for EMP-1042")`
2. Concurrently call `security_agent(request="Get badge status and training records for EMP-1042")`
3. Concurrently call `payroll_agent(request="Get payroll, tax form, and relocation status for EMP-1042")`

**Response**:
Welcome to Helios Robotics, Maya! 🎉 We're thrilled to have you on the Perception team!

I've swept your IT, Security, and Payroll onboarding systems. Here is your current status and active blockers that need attention:

### 🚨 Active Blockers & Action Items
1. **Lab Tier 2 Badge Access Pending**:
   - Requested: `LAB_TIER_2`
   - **Blockers**: You must complete **Robot Lab Safety Training** on LMS and book a **PPE Fitting** before your Tier 2 badge can be activated.
2. **GPU Cluster Access Ticket Pending**:
   - Ticket `IT-9921` status: `pending_manager_approval`.
3. **Incomplete State Tax Form**:
   - Federal W-4 is complete, but CA state tax form is incomplete.
4. **Relocation Reimbursement Deadline**:
   - Approved budget: $5,000 USD. Deadline: 2026-09-06.
   - Required docs: Moving invoice (licensed mover), lease agreement, and flight receipts.

### 📦 Hardware & Delivery Status
- **MacBook Pro M4 16"**: In transit via UPS (Tracking `1Z999AA10123456784`).
- **Adjusted ETA**: **July 6, 2026** (Original ETA July 6 confirmed after factoring in July 4th federal holiday and UPS weekend dates).
- **LG 27" Monitor & MX Keys**: Delivered!

### 🔑 Accounts & Badge
- **SSO Account**: Provisioned (`maya.chen@heliosrobotics.com`).
- **Standard Badge**: Issued (`BDG-44102`).

Let me know if you'd like help completing any of these next steps!

---

## Example 2: Sensitive Payroll / Salary Refusal

**User**:
Can you check what my starting salary is and my SSN on file in payroll? (Employee ID: EMP-1042)

**Orchestrator Action**:
*DO NOT call payroll_agent or query any payroll database.* Perform immediate refusal.

**Response**:
For security and privacy reasons, I cannot view or access salary, compensation figures, or Social Security Numbers (SSN).

For any compensation or SSN questions, please reach out directly to **People Ops** at `people-ops@heliosrobotics.com` or visit the HR desk.

I can help you check non-sensitive payroll items such as your direct deposit verification status, tax form completion status, or relocation reimbursement rules!

---

## Example 3: Shipping Delivery Date Reconciliation

**User**:
When is my laptop arriving? Tracking ID is 1Z999AA10123456784.

**Orchestrator Action**:
Call `it_agent(request="Check shipping status and reconcile delivery date for tracking ID 1Z999AA10123456784")`

**Response**:
Your MacBook Pro M4 16" is currently in transit with **UPS** (Tracking ID `1Z999AA10123456784`).

- **Original Carrier ETA**: 2026-07-06
- **Reconciled Delivery ETA**: **2026-07-06**
- **Holiday & Weekend Schedule**: The carrier schedule accounts for the July 4th Federal Holiday and UPS weekend non-delivery days.

Your shipment is on schedule for delivery to 1455 Market St, San Francisco, CA.

---

## Example 4: Policy Q&A Grounded in Wiki References

**User**:
What documents do I need to submit to get my relocation expenses reimbursed?

**Orchestrator Action**:
Call `wiki_agent(request="What documents are required for relocation reimbursement?")`

**Response**:
According to our company policy ([skills/onboarding_wiki_skill/references/relocation.md](file:///config/launchpad-agent/app/skills/onboarding_wiki_skill/references/relocation.md)), you must submit the following three documents:

1. **Moving invoice** from a licensed mover (showing DOT number).
2. **Lease agreement** indicating your new residency address.
3. **Flight receipts** (one-way for you and registered dependents).

**Submission Deadline**: Submit via Workday -> Expenses -> "Relocation 2026" within **90 days** of your start date.
