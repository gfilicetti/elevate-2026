from app.agent import root_agent


def test_root_agent_tools():
    tool_names = [tool.name for tool in root_agent.tools]
    assert "it_agent" in tool_names
    assert "security_agent" in tool_names
    assert "payroll_agent" in tool_names
    assert "wiki_agent" in tool_names
    assert "image_agent" in tool_names
    assert len(root_agent.tools) == 5
