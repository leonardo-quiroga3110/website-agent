import asyncio
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

# Enable logging
logging.basicConfig(level=logging.DEBUG)

async def check():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    print(f"Connecting to {url}...")
    
    try:
        async with sse_client(url) as (read, write):
            print("SSE connected, creating session...")
            async with ClientSession(read, write) as session:
                print("Session created, initializing...")
                await session.initialize()
                print("Session initialized, loading tools...")
                tools = await load_mcp_tools(session)
                print(f"Tools loaded: {[t.name for t in tools]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
