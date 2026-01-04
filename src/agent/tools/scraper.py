from langchain_core.tools import tool
from langchain_docling import DoclingLoader
from langchain_docling.interfaces import ExportType

@tool
def scrape_website(url: str) -> str:
    """
    Scrapes the clean text content from a specific URL using the Docling high-quality engine.
    This converts complex HTML/Webpages into structured Markdown, preserving tables and lists.
    """
    try:
        # Initialize the Docling Loader
        # ExportType.MARKDOWN ensures we get the best format for LLM reasoning
        loader = DoclingLoader(
            file_path=[url],
            export_type=ExportType.MARKDOWN
        )
        
        # Load the content
        docs = loader.load()
        
        if docs and len(docs) > 0:
            # Join content if multiple results (unlikely for a single URL)
            content = "\n\n".join([doc.page_content for doc in docs])
            if not content.strip():
                return "The website was loaded but no text content could be extracted via Docling."
            return content
        else:
            return f"Docling failed to extract content from {url}. No documents returned."
            
    except Exception as e:
        return f"An error occurred while scraping with Docling: {str(e)}"
