import asyncio
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))
from dotenv import load_dotenv
from agent.tools.scraper import scrape_website

async def debug_scrape():
    load_dotenv()
    url = "https://www.monteazulgroup.com/es"
    print(f"Scraping {url}...")
    content = await scrape_website.ainvoke({"url": url})
    print("-" * 50)
    print(str(content)[:2000])
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(debug_scrape())
