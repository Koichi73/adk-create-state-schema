import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext
from google.adk.apps import App

from .plugins import CreateStateSchema

def get_current_time(tool_context: ToolContext) -> dict:
    """Get the current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    tool_context.state["current_time"] = current_time  # State Update
    return {"status": "success", "current_time": current_time}

root_agent = Agent(
    model="gemini-3-flash-preview",
    name='root_agent',
    description="Greet the user with the current time.",
    instruction="Get the current time using the tool, then greet the user.",
    tools=[get_current_time],
    output_key="greeting",  # State Update
)

app = App(
    name="sample_agent",
    root_agent=root_agent,
    plugins = [CreateStateSchema()]
)
