from langgraph.prebuilt import create_react_agent
from src.models import chat_model
from langchain.prompts import PromptTemplate

from src.prompts.template import apply_prompt_template
from src.tools import web_crawl, web_search

researcher = create_react_agent(
    chat_model,
    tools=[web_crawl, web_search],
    prompt=apply_prompt_template("researcher"),
    name="researcher",
)
