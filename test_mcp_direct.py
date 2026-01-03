import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

async def test():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    try:
        # Some versions of load_mcp_tools take a URL directly for SSE
        tools = await load_mcp_tools(url)
        print(f"Success: {len(tools)} tools found.")
        for t in tools:
            print(f"- {t.name}")
    except Exception as e:
        print(f"Failed with URL directly: {e}")
        
if __name__ == "__main__":
    asyncio.run(test())
