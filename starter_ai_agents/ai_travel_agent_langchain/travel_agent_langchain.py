import os
import time

from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import streamlit as st

st.title("AI Travel Planner ✈️ (LangChain 版)")
st.caption("用 LangChain + GPT-4o 智能规划你的旅行行程")

# 从环境变量读取 API Keys
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("请设置环境变量 OPENAI_API_KEY")
    st.stop()

# 搜索 API 选择
search_option = st.selectbox(
    "选择搜索 API",
    ["Tavily (推荐)", "SerpAPI", "Google Custom Search", "DuckDuckGo (免费)"],
    help="推荐使用 Tavily，LangChain 原生支持，搜索质量高",
)

# 根据选择获取对应的 API Key
if search_option == "Tavily (推荐)":
    search_api_key = os.getenv("TAVILY_API_KEY")
    if not search_api_key:
        st.error("请设置环境变量 TAVILY_API_KEY")
        st.stop()
elif search_option == "SerpAPI":
    search_api_key = os.getenv("SERPAPI_API_KEY")
    if not search_api_key:
        st.error("请设置环境变量 SERPAPI_API_KEY")
        st.stop()
elif search_option == "Google Custom Search":
    search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    if not search_api_key or not search_engine_id:
        st.error("请设置环境变量 GOOGLE_SEARCH_API_KEY 和 GOOGLE_SEARCH_ENGINE_ID")
        st.stop()
else:  # DuckDuckGo
    search_api_key = None
    search_engine_id = None


def search_with_serpapi(query, api_key):
    """使用 LangChain 封装的 SerpAPI 搜索"""
    try:
        search = SerpAPIWrapper(serpapi_api_key=api_key)
        results = search.run(query)
        print(results)
        return results if results else "未找到相关信息"
    except Exception as e:
        st.warning(f"SerpAPI 搜索出错: {str(e)}")
        return "搜索服务暂时不可用"


def search_with_tavily_langchain(query, api_key):
    """使用 LangChain 集成的 Tavily 搜索"""
    try:
        tavily_search = TavilySearch(api_key=api_key, max_results=3)
        results = tavily_search.invoke(query).get("results")
        print(results)
        formatted_results = []
        for result in results:
            title = result.get("title", "")
            content = result.get("content", "")
            formatted_results.append(f"{title}: {content}")

        return "\n".join(formatted_results) if formatted_results else "未找到相关信息"
    except Exception as e:
        st.warning(f"Tavily 搜索出错: {str(e)}")
        return "搜索服务暂时不可用"


def search_with_google(query, api_key, engine_id):
    """使用 LangChain 封装的 Google Custom Search"""
    try:
        search = GoogleSearchAPIWrapper(
            google_api_key=api_key, google_cse_id=engine_id)
        results = search.results(query, 3)
        print(results)
        formatted_results = []
        for result in results:
            formatted_results.append(
                f"{result.get('title', '')}: {result.get('snippet', '')}"
            )
        return "\n".join(formatted_results) if formatted_results else "未找到相关信息"
    except Exception as e:
        st.warning(f"Google 搜索出错: {str(e)}")
        return "搜索服务暂时不可用"


def get_search_results(destination, num_days):
    """获取搜索结果的函数，支持多种搜索 API"""
    search_terms = [
        f"{destination} 必去景点",
        f"{destination} {num_days}天 行程推荐",
        f"{destination} 住宿推荐",
    ]
    results = []

    for i, term in enumerate(search_terms):
        try:
            # 添加延迟避免速率限制
            if i > 0:
                time.sleep(1)

            if search_option == "Tavily (推荐)":
                result = search_with_tavily_langchain(term, search_api_key)
            elif search_option == "SerpAPI":
                result = search_with_serpapi(term, search_api_key)
            elif search_option == "Google Custom Search":
                result = search_with_google(
                    term, search_api_key, search_engine_id)
            else:  # DuckDuckGo
                search = DuckDuckGoSearchRun()
                result = search.run(term)

            results.append(f"【{term}】\n{result}")
            st.write(f"✓ 搜索完成: {term}")

        except Exception as e:
            st.warning(f"搜索 '{term}' 时出错: {str(e)}")
            results.append(f"【{term}】\n由于搜索限制，使用通用旅行建议。")

    if not results:
        results.append(f"【{destination} 旅行建议】\n基于通用旅行知识提供建议。")

    return "\n\n".join(results)


# 检查必要的 API Keys
required_keys = [openai_api_key]
if search_option != "DuckDuckGo (免费)":
    required_keys.append(search_api_key)
if search_option == "Google Custom Search":
    required_keys.append(search_engine_id)

if all(required_keys):
    destination = st.text_input("你想去哪里？")
    num_days = st.number_input("计划旅行几天？", min_value=1, max_value=30, value=7)

    if st.button("生成行程"):
        with st.spinner("正在搜索目的地信息..."):
            research_results = get_search_results(destination, num_days)
            st.write("✓ 搜索完成")

        with st.spinner("正在生成个性化行程..."):
            llm = ChatOpenAI(
                model="gpt-4o",
                api_key=openai_api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            prompt = PromptTemplate(
                input_variables=["destination",
                                 "num_days", "research_results"],
                template="""
You are an expert travel planner. Create a structured itinerary based on the destination, number of days, and search results provided.

Include:
- Daily schedule with timeframes
- Recommended attractions and activities
- Accommodation suggestions (budget, mid-range, luxury)
- Transportation recommendations
- Food and dining options
- Important travel tips

Format with clear headings and balance must-see attractions with unique local experiences.

## Input Format
destination: {destination}
num_days: {num_days}
research_results: {research_results}

## Output Format
# {destination}: {num_days}-Day Travel Itinerary

## Day 1: [Theme]
**上午:**
- Activities with times

**下午:**
- Activities with times

**晚上:**
- Activities with times

## 住宿建议：
- Options at different price points

## 交通建议：
- Key information about getting around

## 必吃美食：
- Local specialties

## 重要提示：
- Practical travel considerations

If search results are limited, please provide reasonable suggestions based on your travel knowledge.

## settings:
use_language: zh-CN
""",
            )

            # 使用 | 操作符创建 RunnableSequence
            chain = prompt | llm

            # 使用 invoke 方法替代 run
            response = chain.invoke(
                {
                    "destination": destination,
                    "num_days": num_days,
                    "research_results": research_results,
                }
            )
            st.write(response.content)
else:
    missing_keys = []
    if not openai_api_key:
        missing_keys.append("OpenAI API Key")
    if search_option != "DuckDuckGo (免费)" and not search_api_key:
        missing_keys.append(f"{search_option} API Key")
    if search_option == "Google Custom Search" and not search_engine_id:
        missing_keys.append("Search Engine ID")

    st.info(f"请填写: {', '.join(missing_keys)}")
