import asyncio
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from agent.graph.agent import MonteAzulAgent

async def run_test(agent, query, test_name):
    print(f"\n--- TEST: {test_name} ---")
    print(f"Query: {query}")
    try:
        result = await agent.run(query)
        print("-" * 50)
        print(f"Answer: {result.get('answer')}")
        print("-" * 50)
        print(f"Visited: {list(result.get('visited_urls', []))}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    load_dotenv()
    agent = MonteAzulAgent()
    
    # Test 1: Spanish Simple Query
    await run_test(agent, "¿De qué trata la empresa Monte Azul?", "Spanish Simple")
    
    # Test 2: English Complex Query
    await run_test(agent, "Detail the storage capabilities of the Mollendo terminal and explain its strategic importance for Southern Peru.", "English Complex")

if __name__ == "__main__":
    asyncio.run(main())
