import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def list_mcp_tools():
    # The URL provided by the user
    mcp_url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    
    # Configure the client
    # Note: Using transport="http" or similar as per docs
    async with MultiServerMCPClient() as client:
        await client.connect_sse(mcp_url)
        tools = await client.get_tools()
        print(f"Connected to MCP Server: {mcp_url}")
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description[:100]}...")

if __name__ == "__main__":
    asyncio.run(list_mcp_tools())
