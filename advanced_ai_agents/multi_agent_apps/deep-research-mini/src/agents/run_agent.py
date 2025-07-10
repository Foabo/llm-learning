import uuid

from langgraph.graph.state import CompiledStateGraph
from .researcher import researcher

def run_agent(agent: CompiledStateGraph, msg: str):
    """
    Run an agent with a message.
    Process data in stream mode.
    Args:
        agent: The agent to run.
        msg: The message to run the agent with.
    Returns:
        The response from the agent.
    """
    result = agent.stream(
        {
            "messages": [{"role": "user", "content": msg}],
        },
        stream_mode="values",
        config={"run_name": str(uuid.uuid4())},
    )
    for chunk in result:
        msgs = chunk["messages"]
        last_msg = msgs[-1]
        last_msg.pretty_print()

if __name__ == "__main__":
    run_agent(researcher, "什么是大模型里a2a技术")