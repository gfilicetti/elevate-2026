from typing import Any, Dict
from google.adk.agents import LlmAgent
from app.tools import escalate_to_people_ops


def triage_badge_image(
    employee_id: str, color_band: str, is_damaged: bool = False, damage_description: str = ""
) -> Dict[str, Any]:
    """Analyze a badge photo visual state, identify role tier based on color band, and handle physical damage escalations.

    Helios Robotics badge color band mappings:
    - Green band: STANDARD
    - Blue band: LAB_TIER_1
    - Red band: LAB_TIER_2

    Args:
        employee_id: Employee ID (e.g. 'EMP-1042').
        color_band: Observed color band on badge ('green', 'blue', or 'red').
        is_damaged: True if physical damage (cracks, broken clip/stripe, physical wear) is detected.
        damage_description: Details of physical damage if present.

    Returns:
        Dict containing analysis, tier classification, escalation record, and instructions.
    """
    color_normalized = color_band.lower().strip()
    tier_mapping = {
        "green": "STANDARD",
        "blue": "LAB_TIER_1",
        "red": "LAB_TIER_2",
    }
    identified_tier = tier_mapping.get(color_normalized, "UNKNOWN")

    escalation_result = None
    if is_damaged:
        summary = f"Physical badge damage reported: {damage_description or 'Cracked/damaged physical badge'}"
        escalation_result = escalate_to_people_ops(
            employee_id=employee_id,
            summary=summary,
            severity="medium",
            suggested_owner="badges_team",
        )

    user_instructions = (
        "Your badge shows physical damage. Please return the damaged badge in person to the physical Security desk."
        if is_damaged
        else f"Badge visual check complete. Role tier: {identified_tier}. No physical damage detected."
    )

    return {
        "employee_id": employee_id,
        "color_band": color_band,
        "identified_tier": identified_tier,
        "is_damaged": is_damaged,
        "damage_description": damage_description,
        "escalation": escalation_result,
        "user_instructions": user_instructions,
    }


def build_image_agent() -> LlmAgent:
    instruction = """You are the Multimodal Image Specialist (`image_agent`) for Helios Robotics onboarding.

Your responsibilities:
1. Analyze uploaded badge photos and visual badge state.
2. Identify the role tier based on the color band:
   - Green band: `STANDARD`
   - Blue band: `LAB_TIER_1`
   - Red band: `LAB_TIER_2`
3. Check the badge image for physical damage (cracks, broken clips, damaged stripes/chips).
4. If physical damage is detected:
   - Trigger `escalate_to_people_ops(employee_id=..., summary=..., severity='medium', suggested_owner='badges_team')` directly or via `triage_badge_image`.
   - Inform the user to return the damaged badge in person to the physical Security desk.
5. If no physical damage is detected, confirm the identified tier access level and badge status.
"""
    return LlmAgent(
        name="image_agent",
        description="Multimodal vision specialist for inspecting badge photos, identifying role tiers via color bands (green=STANDARD, blue=LAB_TIER_1, red=LAB_TIER_2), detecting physical damage, and escalating badge replacements to badges_team.",
        model="gemini-3.6-flash",
        instruction=instruction,
        tools=[triage_badge_image, escalate_to_people_ops],
    )


image_agent = build_image_agent()
