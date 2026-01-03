import os
from langchain_core.tools import tool
from tavily import TavilyClient

@tool
def search_tavily(query: str) -> list:
    """
    Performs a broad web search using Tavily to find relevant information or URLs.
    Use this when you need to find general information or locate specific pages.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return ["Error: TAVILY_API_KEY not found."]
    
    try:
        client = TavilyClient(api_key=api_key)
        # Search for results
        response = client.search(query=query, max_results=5)
        return response.get("results", [])
    except Exception as e:
        return [f"Error searching Tavily: {str(e)}"]
