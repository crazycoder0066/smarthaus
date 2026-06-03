from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from app import tools
from app.schemas import ActionResult, ToolCall

# temperature=0 for repeatability. llama3.1:8b is tool-capable.
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

SYSTEM = """
You control a smart home. To handle a command:
1) If you don't know a device id, call list_devices first. NEVER invent ids.
2) If the command depends on a condition (e.g. 'if it's cold'), read the sensor first.
3) Make the needed set_device calls, then STOP.
Respond with a short summary of exactly what you changed.
"""

agent = create_react_agent(
    llm,
    tools=[tools.list_devices, tools.get_sensor, tools.set_device],
    prompt=SYSTEM,
)

async def run_command(text: str) -> ActionResult:
    result = await agent.ainvoke({"messages": [HumanMessage(content=text)]})
    messages = result["messages"]

    # The final assistant message holds the agent's summary.
    final = messages[-1]
    reply = final.content if isinstance(final.content, str) else str(final.content)

    # Walk the whole trace and collect every tool the agent invoked.
    tool_calls = [
        ToolCall(name=tc["name"], args=tc.get("args", {}))
        for msg in messages
        for tc in (getattr(msg, "tool_calls", None) or [])
    ]

    return ActionResult(reply=reply, tool_calls=tool_calls)
