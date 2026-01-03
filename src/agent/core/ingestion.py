import logging
import os
from typing import List
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agent.core.config import get_settings

logger = logging.getLogger(__name__)

class WebsiteIndexer:
    """
    Handles scraping a website using Docling and indexing its content into ChromaDB.
    """
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = OpenAIEmbeddings(
            model=self.settings.EMBEDDING_MODEL,
            openai_api_key=self.settings.OPENAI_API_KEY
        )
        self.vector_store = None

    def _get_vector_store(self):
        """
        Initializes or retrieves the Chroma vector store.
        """
        if self.vector_store is None:
            self.vector_store = Chroma(
                collection_name=self.settings.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=self.settings.CHROMA_PATH
            )
        return self.vector_store

    def index_website(self, url: str = None):
        """
        Scrapes the website and indexes the content.
        """
        if url is None:
            url = self.settings.WEBSITE_URL

        logger.info(f"Starting ingestion for: {url}")
        
        # 1. Load documents using Docling
        # We use ExportType.DOC_CHUNKS to get pre-chunked documents with layout awareness
        loader = DoclingLoader(
            file_path=[url],
            export_type=ExportType.DOC_CHUNKS
        )
        
        docs = loader.load()
        logger.info(f"Loaded {len(docs)} chunks from Docling.")

        if not docs:
            logger.warning("No documents loaded from the URL.")
            return

        # 2. Add to Vector Store
        # ChromaDB handles persistence automatically when a persist_directory is provided
        vector_store = self._get_vector_store()
        
        # Filter metadata for ChromaDB compatibility
        filtered_docs = filter_complex_metadata(docs)
        vector_store.add_documents(filtered_docs)
        
        logger.info(f"Successfully indexed {len(filtered_docs)} chunks into {self.settings.CHROMA_PATH}")

    def clear_index(self):
        """
        Deletes the existing collection.
        """
        vector_store = self._get_vector_store()
        vector_store.delete_collection()
        self.vector_store = None
        logger.info("Cleared the vector store collection.")
