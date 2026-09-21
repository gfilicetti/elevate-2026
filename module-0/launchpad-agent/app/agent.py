import pathlib
from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.tools import AgentTool
from app.sub_agents.it import it_agent
from app.sub_agents.security import security_agent
from app.sub_agents.payroll import payroll_agent
from app.sub_agents.wiki import wiki_agent
from app.sub_agents.image import image_agent


def build_root() -> LlmAgent:
    prompt_path = pathlib.Path(__file__).parent / "prompts" / "orchestrator.md"
    system_prompt = prompt_path.read_text()

    return LlmAgent(
        name="launchpad",
        model="gemini-3.6-flash",
        instruction=system_prompt,
        tools=[
            AgentTool(it_agent),
            AgentTool(security_agent),
            AgentTool(payroll_agent),
            AgentTool(wiki_agent),
            AgentTool(image_agent),
        ],
    )


root_agent = build_root()
app = App(name="launchpad", root_agent=root_agent)
