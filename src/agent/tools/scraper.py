import os
from langchain_core.tools import tool
from tavily import TavilyClient

@tool
def scrape_website(url: str) -> str:
    """
    Scrapes the clean text content from a specific URL using Tavily's extraction engine.
    This is best used when you already have a specific link (like a product page) 
    and need the full text content/data from that page.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not found in environment. Please add it to your .env file."
    
    try:
        # Initialize the Tavily client
        client = TavilyClient(api_key=api_key)
        
        # Use the extract method to get content from the URL
        # We only pass one URL in the list
        response = client.extract(urls=[url])
        
        if response and "results" in response and len(response["results"]) > 0:
            # Get the raw content from the first (and only) result
            content = response["results"][0].get("raw_content", "")
            if not content:
                return "The website was loaded but no content could be extracted."
            return content
        else:
            return f"Failed to extract content from {url}. No results returned."
            
    except Exception as e:
        return f"An error occurred while scraping the website: {str(e)}"
