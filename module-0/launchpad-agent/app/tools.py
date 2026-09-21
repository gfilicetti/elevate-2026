import json
import pathlib
from typing import Any, Dict, List, Optional

MOCK_DATA_DIR = pathlib.Path(__file__).parent.parent / "mock_data"


def _load_json_file(filename: str) -> Dict[str, Any]:
    """Load a JSON file from MOCK_DATA_DIR with error handling."""
    file_path = MOCK_DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Mock data file '{filename}' not found at {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(f"Expected top-level JSON object in '{filename}', got {type(data).__name__}")
        return data


def get_hardware_order(employee_id: str) -> Dict[str, Any]:
    """Retrieve hardware order information for a given employee ID."""
    try:
        data = _load_json_file("it_inventory.json")
    except Exception as err:
        return {"error": f"Failed to load IT inventory data: {str(err)}"}

    orders = data.get("orders")
    if not isinstance(orders, list):
        return {"error": "Invalid IT inventory data format: missing or invalid 'orders' list"}

    for order in orders:
        if isinstance(order, dict) and order.get("employee_id") == employee_id:
            return order

    return {"error": f"No hardware order found for employee ID: {employee_id}"}


def get_shipping_status(tracking_id: str) -> Dict[str, Any]:
    """Retrieve shipping status for a given package tracking ID."""
    try:
        data = _load_json_file("it_inventory.json")
    except Exception as err:
        return {"error": f"Failed to load IT inventory data: {str(err)}"}

    orders = data.get("orders")
    if not isinstance(orders, list):
        return {"error": "Invalid IT inventory data format: missing or invalid 'orders' list"}

    for order in orders:
        if isinstance(order, dict) and order.get("tracking_id") == tracking_id:
            return order

    return {"error": f"No shipping record found for tracking ID: {tracking_id}"}


def get_holiday_calendar() -> Dict[str, Any]:
    """Retrieve the company holiday calendar and carrier non-delivery dates."""
    try:
        return _load_json_file("holiday_calendar.json")
    except Exception as err:
        return {"error": f"Failed to load holiday calendar data: {str(err)}"}


def get_sso_status(employee_id: str) -> Dict[str, Any]:
    """Retrieve Single Sign-On (SSO) and account status for a given employee ID."""
    try:
        data = _load_json_file("it_inventory.json")
    except Exception as err:
        return {"error": f"Failed to load IT inventory data: {str(err)}"}

    accounts = data.get("sso_accounts")
    if not isinstance(accounts, list):
        return {"error": "Invalid IT inventory data format: missing or invalid 'sso_accounts' list"}

    for account in accounts:
        if isinstance(account, dict) and account.get("employee_id") == employee_id:
            return account

    return {"error": f"No SSO account found for employee ID: {employee_id}"}


def get_badge_status(employee_id: str) -> Dict[str, Any]:
    """Retrieve security badge status and related training records for a given employee ID."""
    try:
        data = _load_json_file("security_badges.json")
    except Exception as err:
        return {"error": f"Failed to load security badge data: {str(err)}"}

    badges = data.get("badges")
    if not isinstance(badges, list):
        return {"error": "Invalid security badge data format: missing or invalid 'badges' list"}

    badge_info = None
    for badge in badges:
        if isinstance(badge, dict) and badge.get("employee_id") == employee_id:
            badge_info = badge
            break

    if not badge_info:
        return {"error": f"No badge record found for employee ID: {employee_id}"}

    training_records = data.get("training_records", [])
    emp_trainings = [
        t for t in training_records if isinstance(t, dict) and t.get("employee_id") == employee_id
    ]

    result = dict(badge_info)
    result["training_records"] = emp_trainings
    return result


def get_payroll_status(employee_id: str) -> Dict[str, Any]:
    """Retrieve payroll, tax forms, and reimbursement status for a given employee ID."""
    try:
        data = _load_json_file("payroll.json")
    except Exception as err:
        return {"error": f"Failed to load payroll data: {str(err)}"}

    employees = data.get("employees")
    if not isinstance(employees, list):
        return {"error": "Invalid payroll data format: missing or invalid 'employees' list"}

    for emp in employees:
        if isinstance(emp, dict) and emp.get("employee_id") == employee_id:
            return emp

    return {"error": f"No payroll record found for employee ID: {employee_id}"}


def get_checklist(employee_id: str) -> Dict[str, Any]:
    """Retrieve onboarding checklist tasks for a given employee ID."""
    try:
        data = _load_json_file("checklist.json")
    except Exception as err:
        return {"error": f"Failed to load checklist data: {str(err)}"}

    if employee_id not in data:
        return {"error": f"No checklist found for employee ID: {employee_id}"}

    items = data[employee_id]
    return {"employee_id": employee_id, "checklist": items}


def escalate_to_people_ops(
    employee_id: str, summary: str, severity: str, suggested_owner: str
) -> Dict[str, Any]:
    """Mock an escalation page to People Ops human operators."""
    ticket_hash = abs(hash(f"{employee_id}-{summary}-{severity}")) % 10000
    ticket_id = f"ESC-{ticket_hash:04d}"

    return {
        "status": "escalated",
        "ticket_id": ticket_id,
        "employee_id": employee_id,
        "summary": summary,
        "severity": severity,
        "suggested_owner": suggested_owner,
        "message": f"Escalation successfully created ({ticket_id}) and paged to {suggested_owner}.",
    }
