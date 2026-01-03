import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def list_tools():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    print(f"Connecting to MCP at {url}...")
    
    # Configuration for the server
    # Note: Transport is SSE/HTTP
    config = {
        "tavily": {
            "url": url,
            "transport": "sse" # or "http"
        }
    }
    
    async with MultiServerMCPClient(config) as client:
        # Get the tools
        tools = await client.get_tools()
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"- {tool.name}")

if __name__ == "__main__":
    asyncio.run(list_tools())
