import asyncio
import time
from agent.graph.agent import agent

async def benchmark():
    print("--- Performance Benchmark ---")
    start = time.time()
    
    # Simple query
    res = await agent.run("What is Monte Azul Group?")
    duration = time.time() - start
    
    print(f"Total Response Time: {duration:.2f}s")
    print(f"Answer: {res.get('answer')[:100]}...")

if __name__ == "__main__":
    asyncio.run(benchmark())
