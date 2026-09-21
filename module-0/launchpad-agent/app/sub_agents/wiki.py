import pathlib
from typing import Any, Dict
from google.adk.agents import LlmAgent

WIKI_REF_DIR = (
    pathlib.Path(__file__).parent.parent / "skills" / "onboarding_wiki_skill" / "references"
)


def search_onboarding_wiki(topic: str = "") -> Dict[str, Any]:
    """Search and retrieve reference documents from the Onboarding Wiki.

    Args:
        topic: Keyword or topic name to search for (e.g. 'badges', 'relocation', 'safety').
               If empty, retrieves all wiki reference documents.

    Returns:
        Dict containing source filepaths and document contents.
    """
    ref_dir = WIKI_REF_DIR
    if not ref_dir.exists():
        # Fallback to root-level skills path if running from root execution context
        ref_dir = pathlib.Path(__file__).parent.parent.parent / "skills" / "onboarding_wiki_skill" / "references"

    if not ref_dir.exists():
        return {"error": "Onboarding wiki reference directory not found."}

    documents = {}
    for file in ref_dir.glob("*.md"):
        rel_path = f"skills/onboarding_wiki_skill/references/{file.name}"
        content = file.read_text(encoding="utf-8")
        if not topic or topic.lower() in file.name.lower() or topic.lower() in content.lower():
            documents[rel_path] = content

    if not documents:
        return {"error": f"No wiki reference documents found matching topic '{topic}'."}

    return {"documents": documents}


def build_wiki_agent() -> LlmAgent:
    instruction = """You are the Onboarding Wiki Specialist for Helios Robotics.

Operating Rules:
1. Ground every policy response in specific reference files retrieved via `search_onboarding_wiki`.
2. Always cite the exact relative filepath of the source document (e.g., `skills/onboarding_wiki_skill/references/badges.md`).
3. If no reference document contains the requested information, do not guess or hallucinate. State clearly: "I don't have a source for that — let me escalate."
"""
    return LlmAgent(
        name="wiki_agent",
        description="Onboarding Wiki Specialist for policy Q&As concerning logistics, hardware, badges, relocation, and safety rules.",
        model="gemini-3.6-flash",
        instruction=instruction,
        tools=[search_onboarding_wiki],
    )


wiki_agent = build_wiki_agent()
