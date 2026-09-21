import pytest
from app.sub_agents.image import image_agent, triage_badge_image


def test_triage_badge_image_green_band():
    result = triage_badge_image(employee_id="EMP-1042", color_band="green", is_damaged=False)
    assert result["identified_tier"] == "STANDARD"
    assert result["is_damaged"] is False
    assert result["escalation"] is None


def test_triage_badge_image_blue_band():
    result = triage_badge_image(employee_id="EMP-1042", color_band="blue", is_damaged=False)
    assert result["identified_tier"] == "LAB_TIER_1"


def test_triage_badge_image_red_band_damaged():
    result = triage_badge_image(
        employee_id="EMP-1042",
        color_band="red",
        is_damaged=True,
        damage_description="Cracked plastic case",
    )
    assert result["identified_tier"] == "LAB_TIER_2"
    assert result["is_damaged"] is True
    assert result["escalation"] is not None
    assert result["escalation"]["status"] == "escalated"
    assert result["escalation"]["severity"] == "medium"
    assert result["escalation"]["suggested_owner"] == "badges_team"
    assert "return the damaged badge in person to the physical Security desk" in result["user_instructions"]


def test_image_agent_setup():
    assert image_agent.name == "image_agent"
    tool_names = [tool.__name__ for tool in image_agent.tools]
    assert "triage_badge_image" in tool_names
    assert "escalate_to_people_ops" in tool_names
