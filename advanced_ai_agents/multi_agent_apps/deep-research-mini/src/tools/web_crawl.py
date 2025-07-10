import os
from firecrawl import FirecrawlApp
from langchain.tools import tool

@tool
def web_crawl(url: str) -> str:
    """
    Crawl a web page and return the main content in markdown format.
    Args:
        url: The URL of the web page to crawl.
    Returns:
        The main content of the web page in markdown format.
    """
    firecrawl=FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    response=firecrawl.scrape_url(
        url=url,
        formats=["markdown"],
        only_main_content=True,
    )
    return response.markdown

if __name__ == "__main__":
    print(web_crawl.invoke("https://www.baidu.com"))