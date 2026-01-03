import asyncio
from agent.graph.agent import MonteAzulAgent

async def test_guardrails():
    agent = MonteAzulAgent()
    thread_id = "guardrail-test"
    
    print("--- PII Input Test ---")
    query = "My email is test@example.com and phone is 1234567890. Who is Monte Azul?"
    res = await agent.run(query, thread_id=thread_id)
    print(f"Safe Query used: {res.get('query')}")
    print(f"Answer: {res.get('answer')[:100]}...")

    print("\n--- PII Output Test ---")
    # This assumes the analyst might repeat high risk info which we check in output
    query_2 = "Can you repeat my email back to me?"
    res_2 = await agent.run(query_2, thread_id=thread_id)
    print(f"Answer: {res_2.get('answer')}")

if __name__ == "__main__":
    asyncio.run(test_guardrails())
