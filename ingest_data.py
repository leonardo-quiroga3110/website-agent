import argparse
import logging
import asyncio
from agent.core.ingestion import WebsiteIndexer
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    parser = argparse.ArgumentParser(description="Ingest website content into the vector store.")
    parser.add_argument("--url", type=str, help="The URL to ingest (overrides .env WEBSITE_URL)")
    parser.add_argument("--clear", action="store_true", help="Clear the existing index before ingesting")
    
    args = parser.parse_args()
    
    load_dotenv()
    
    indexer = WebsiteIndexer()
    
    if args.clear:
        logger.info("Clearing existing index...")
        indexer.clear_index()
    
    logger.info(f"Starting ingestion process...")
    # index_website is not async in the current implementation, but we run it in a main async for future-proofing or if needed.
    # Actually WebsiteIndexer.index_website is synchronous based on view_file
    indexer.index_website(url=args.url)
    logger.info("Ingestion completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
