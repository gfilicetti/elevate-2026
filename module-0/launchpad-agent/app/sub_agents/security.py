from google.adk.agents import LlmAgent
from app.tools import get_badge_status


def build_security_agent() -> LlmAgent:
    instruction = """You are the Security & Badge Specialist for Helios Robotics onboarding.

Your responsibilities:
1. Retrieve badge status, badge IDs, current tier (e.g. STANDARD, LAB_TIER_1, LAB_TIER_2), and requested access levels.
2. Check safety training records (such as `safety_training` and `ppe_fitting`) for the employee.
3. Identify badge tier mismatches or prerequisites required before upgrading access (e.g., LAB_TIER_2 requires safety training, PPE fitting, and manager sign-off).
4. Report active badge and physical security blockers clearly.
"""
    return LlmAgent(
        name="security_agent",
        description="Security & Badge Specialist handling physical badge status, tier access levels, and safety training requirements.",
        model="gemini-3.6-flash",
        instruction=instruction,
        tools=[get_badge_status],
    )


security_agent = build_security_agent()
