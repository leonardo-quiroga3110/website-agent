import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

async def test_mcp_adapter():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    
    # Configuration as a list of dicts (as per some docs)
    config = [
        {
            "name": "tavily",
            "url": url,
            "transport": "sse"
        }
    ]
    
    try:
        print("Loading tools...")
        tools = await load_mcp_tools(config)
        print(f"Success! Found {len(tools)} tools.")
        for tool in tools:
            print(f"- {tool.name}: {tool.description[:50]}...")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_adapter())
