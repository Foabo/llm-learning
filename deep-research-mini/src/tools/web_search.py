from langchain_tavily import TavilySearch
import json

web_search = TavilySearch(
    name="web_search",
    max_results=5,
)

if __name__ == "__main__":
    print(json.dumps(web_search.invoke("世俱杯战况如何？"),ensure_ascii=False ,indent=4))
