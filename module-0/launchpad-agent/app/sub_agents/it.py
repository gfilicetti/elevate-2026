from datetime import datetime, timedelta
import pathlib
from typing import Any, Dict
from google.adk.agents import LlmAgent
from app.tools import (
    get_hardware_order,
    get_shipping_status,
    get_sso_status,
    get_holiday_calendar,
)


def reconcile_delivery_date(carrier_eta: str, carrier: str) -> Dict[str, Any]:
    """Reconcile carrier ETA dates taking into account federal holidays and carrier non-delivery days."""
    calendar = get_holiday_calendar()
    if "error" in calendar:
        return {
            "carrier": carrier,
            "original_eta": carrier_eta,
            "reconciled_eta": carrier_eta,
            "notes": "Unable to load holiday calendar.",
        }

    fed_holidays = set(calendar.get("us_federal_holidays_2026", []))
    carrier_no_deliv = set(calendar.get("carrier_no_delivery_dates", {}).get(carrier, []))
    blocked_dates = fed_holidays.union(carrier_no_deliv)

    try:
        curr_date = datetime.strptime(carrier_eta, "%Y-%m-%d").date()
        adjusted = False
        delays = []

        # Check if current ETA or immediate period is impacted by holiday/no-delivery dates
        while curr_date.strftime("%Y-%m-%d") in blocked_dates or curr_date.weekday() >= 5:
            date_str = curr_date.strftime("%Y-%m-%d")
            if date_str in fed_holidays:
                delays.append(f"Federal Holiday on {date_str}")
            elif date_str in carrier_no_deliv:
                delays.append(f"{carrier} non-delivery date on {date_str}")
            elif curr_date.weekday() >= 5:
                delays.append(f"Weekend day on {date_str}")
            curr_date += timedelta(days=1)
            adjusted = True

        reconciled_eta = curr_date.strftime("%Y-%m-%d")
        return {
            "carrier": carrier,
            "original_eta": carrier_eta,
            "reconciled_eta": reconciled_eta,
            "adjusted": adjusted,
            "delays": delays,
            "status_summary": (
                f"Adjusted delivery date from {carrier_eta} to {reconciled_eta} due to: {', '.join(delays)}"
                if adjusted
                else f"ETA {carrier_eta} confirmed with no holiday conflicts."
            ),
        }
    except ValueError:
        return {
            "carrier": carrier,
            "original_eta": carrier_eta,
            "reconciled_eta": carrier_eta,
            "notes": "Invalid date format provided for ETA.",
        }


def build_it_agent() -> LlmAgent:
    instruction = """You are the IT Support Specialist for Helios Robotics onboarding.

Your responsibilities:
1. Track hardware orders, laptop shipments, and equipment delivery statuses for new hires.
2. Check Single Sign-On (SSO) account setup, primary email, and GPU cluster access tickets.
3. Reconcile shipping delivery ETAs when carrier dates overlap with federal holidays (e.g. July 4th) or carrier non-delivery days using `reconcile_delivery_date`.
4. Clearly report any pending IT blockers, such as pending manager approvals for GPU access or delayed hardware shipments.
"""
    return LlmAgent(
        name="it_agent",
        description="IT Support Specialist handling hardware orders, shipping tracking, SSO account status, and delivery date reconciliation.",
        model="gemini-3.6-flash",
        instruction=instruction,
        tools=[
            get_hardware_order,
            get_shipping_status,
            get_sso_status,
            get_holiday_calendar,
            reconcile_delivery_date,
        ],
    )


it_agent = build_it_agent()
