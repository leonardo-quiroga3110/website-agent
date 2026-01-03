import logging
import asyncio
import argparse
from dotenv import load_dotenv
from agent.core.ingestion import WebsiteIndexer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Index a website into ChromaDB using Docling.")
    parser.add_argument("--url", type=str, help="The URL to index (overrides config)")
    parser.add_argument("--clear", action="store_true", help="Clear the index before indexing")
    
    args = parser.parse_args()
    
    indexer = WebsiteIndexer()
    
    if args.clear:
        logger.info("Clearing existing index...")
        indexer.clear_index()
        
    logger.info("Starting indexing process...")
    # Since DoclingLoader.load() is synchronous in the current implementation, 
    # we don't need to await it unless we wrap it in a thread.
    indexer.index_website(url=args.url)
    logger.info("Indexing completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
