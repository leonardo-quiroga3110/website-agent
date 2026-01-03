import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

async def test():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    
    # Trying different config structures
    try:
        print("Trying config as dict of dicts...")
        config = {
            "tavily": {
                "url": url,
                "transport": "sse"
            }
        }
        # In some versions, load_mcp_tools might take this
        tools = await load_mcp_tools(config)
        print(f"Success! {len(tools)} tools.")
    except Exception as e:
        print(f"Failed with dict of dicts: {e}")

if __name__ == "__main__":
    asyncio.run(test())
