import logging
import asyncio
from dotenv import load_dotenv
from agent.core.retrieval import RAGRetriever

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_retrieval():
    load_dotenv()
    
    retriever = RAGRetriever()
    
    query = "What services does Monte Azul Group provide?"
    logger.info(f"Testing retrieval for: {query}")
    
    results = retriever.retrieve(query)
    
    print("\n--- Retrieval Results ---")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")
    print("\n--- End of Results ---")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
