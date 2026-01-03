import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv
from agent.tools.scraper import scrape_website

def test_scraper():
    # Load environment variables from .env
    load_dotenv()
    
    # Check for API Key
    if not os.environ.get("TAVILY_API_KEY"):
        print("Please set TAVILY_API_KEY in your .env file before running this test.")
        return

    # test URL
    url = "https://www.monteazulgroup.com/es"  # Replace with the user's link if known
    print(f"--- Testing Scraper Tool with URL: {url} ---")
    
    try:
        content = scrape_website.invoke({"url": url})
        print("\nExtracted Content (First 500 characters):")
        print("-" * 40)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 40)
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_scraper()
