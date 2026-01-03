import asyncio
from agent.graph.agent import MonteAzulAgent

async def test_memory():
    agent = MonteAzulAgent()
    thread_id = "test-session-1"
    
    print("--- First Turn ---")
    res1 = await agent.run("Who is Monte Azul Group?", thread_id=thread_id)
    print(f"Answer 1: {res1.get('answer')[:100]}...")
    
    print("\n--- Second Turn (Memory Check) ---")
    res2 = await agent.run("What was my last question?", thread_id=thread_id)
    print(f"Answer 2: {res2.get('answer')}")

if __name__ == "__main__":
    asyncio.run(test_memory())
