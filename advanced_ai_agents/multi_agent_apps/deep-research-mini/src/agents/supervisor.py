from langgraph_supervisor import create_supervisor
from src.models import chat_model
from src.prompts.template import apply_prompt_template
from src.agents import planner, researcher

supervisor = create_supervisor(
    [planner, researcher],
    model=chat_model,
    prompt=apply_prompt_template("supervisor"),
    supervisor_name="supervisor",  
).compile()

if __name__ == "__main__":
    supervisor.invoke({"messages": [{"role": "user", "content": "What is the latest news on AI?"}]})