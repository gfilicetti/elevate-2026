import pytest
from app.agent import root_agent
from app.sub_agents.it import it_agent, reconcile_delivery_date
from app.sub_agents.security import security_agent
from app.sub_agents.payroll import payroll_agent
from app.sub_agents.wiki import wiki_agent, search_onboarding_wiki
from app.sub_agents.image import image_agent, triage_badge_image


def test_root_agent_registration():
    assert root_agent.name == "launchpad"
    tool_names = [tool.name for tool in root_agent.tools]
    assert "it_agent" in tool_names
    assert "security_agent" in tool_names
    assert "payroll_agent" in tool_names
    assert "wiki_agent" in tool_names
    assert "image_agent" in tool_names
    assert len(root_agent.tools) == 5


def test_reconcile_delivery_date():
    result = reconcile_delivery_date("2026-07-03", "UPS")
    assert "reconciled_eta" in result
    assert result["adjusted"] is True
    assert len(result["delays"]) > 0


def test_search_onboarding_wiki():
    result = search_onboarding_wiki("badges")
    assert "documents" in result
    assert any("badges.md" in k for k in result["documents"].keys())


def test_triage_badge_image():
    result = triage_badge_image("EMP-1042", color_band="green", is_damaged=True, damage_description="Damaged clip")
    assert result["employee_id"] == "EMP-1042"
    assert "Security desk" in result["user_instructions"]
    assert result["escalation"] is not None


def test_sub_agents_instantiation():
    assert it_agent.name == "it_agent"
    assert security_agent.name == "security_agent"
    assert payroll_agent.name == "payroll_agent"
    assert wiki_agent.name == "wiki_agent"
    assert image_agent.name == "image_agent"
