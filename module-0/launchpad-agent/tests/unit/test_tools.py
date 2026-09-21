import pytest
from app.tools import (
    get_hardware_order,
    get_shipping_status,
    get_holiday_calendar,
    get_sso_status,
    get_badge_status,
    get_payroll_status,
    get_checklist,
    escalate_to_people_ops,
)


def test_get_hardware_order_success():
    result = get_hardware_order("EMP-1042")
    assert "error" not in result
    assert result["order_id"] == "ORD-2026-8841"
    assert result["employee_name"] == "Maya Chen"


def test_get_hardware_order_not_found():
    result = get_hardware_order("EMP-9999")
    assert "error" in result
    assert "EMP-9999" in result["error"]


def test_get_shipping_status_success():
    result = get_shipping_status("1Z999AA10123456784")
    assert "error" not in result
    assert result["carrier"] == "UPS"


def test_get_shipping_status_not_found():
    result = get_shipping_status("TRACKING-UNKNOWN")
    assert "error" in result


def test_get_holiday_calendar():
    result = get_holiday_calendar()
    assert "error" not in result
    assert "us_federal_holidays_2026" in result
    assert "carrier_no_delivery_dates" in result


def test_get_sso_status_success():
    result = get_sso_status("EMP-1042")
    assert "error" not in result
    assert result["sso_provisioned"] is True
    assert result["primary_email"] == "maya.chen@heliosrobotics.com"


def test_get_sso_status_not_found():
    result = get_sso_status("EMP-9999")
    assert "error" in result


def test_get_badge_status_success():
    result = get_badge_status("EMP-1042")
    assert "error" not in result
    assert result["badge_id"] == "BDG-44102"
    assert "training_records" in result
    assert len(result["training_records"]) > 0


def test_get_badge_status_not_found():
    result = get_badge_status("EMP-9999")
    assert "error" in result


def test_get_payroll_status_success():
    result = get_payroll_status("EMP-1042")
    assert "error" not in result
    assert result["direct_deposit"]["status"] == "verified"


def test_get_payroll_status_not_found():
    result = get_payroll_status("EMP-9999")
    assert "error" in result


def test_get_checklist_success():
    result = get_checklist("EMP-1042")
    assert "error" not in result
    assert result["employee_id"] == "EMP-1042"
    assert isinstance(result["checklist"], list)
    assert len(result["checklist"]) > 0


def test_get_checklist_not_found():
    result = get_checklist("EMP-9999")
    assert "error" in result


def test_escalate_to_people_ops():
    result = escalate_to_people_ops(
        employee_id="EMP-1042",
        summary="Laptop setup blocked due to missing GPU credentials",
        severity="high",
        suggested_owner="IT Support",
    )
    assert result["status"] == "escalated"
    assert "ticket_id" in result
    assert result["employee_id"] == "EMP-1042"
    assert result["severity"] == "high"
