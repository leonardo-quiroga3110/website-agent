import logging
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from agent.core.config import get_settings

logger = logging.getLogger(__name__)

class RAGRetriever:
    """
    Handles hybrid retrieval using ChromaDB (semantic) and BM25 (keyword).
    """
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = OpenAIEmbeddings(
            model=self.settings.EMBEDDING_MODEL,
            openai_api_key=self.settings.OPENAI_API_KEY
        )
        self.vector_store = Chroma(
            collection_name=self.settings.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=self.settings.CHROMA_PATH
        )
        self.ensemble_retriever = self._build_ensemble_retriever()

    async def ingest_url(self, url: str):
        """
        Scrapes a URL using Docling and adds it to ChromaDB.
        """
        from langchain_docling import DoclingLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        logger.info(f"Ingesting URL using Docling: {url}")
        loader = DoclingLoader(file_path=[url])
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        # Add to vector store
        self.vector_store.add_documents(splits)
        logger.info(f"Successfully ingested {len(splits)} chunks from {url}")

    def _build_ensemble_retriever(self):
        """
        Builds an EnsembleRetriever combining Chroma and BM25.
        """
        # 1. Setup Chroma retriever
        chroma_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )

        all_docs = self.vector_store.get()
        if not all_docs or not all_docs['documents']:
            logger.warning("No documents found in ChromaDB. Ingestion required.")
            # We return a placeholder or just the chroma_retriever which will return empty
            return chroma_retriever

        documents = [
            Document(page_content=content, metadata=meta)
            for content, meta in zip(all_docs['documents'], all_docs['metadatas'])
        ]
        
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 5

        # 3. Create Ensemble Retriever
        ensemble = EnsembleRetriever(
            retrievers=[chroma_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )
        return ensemble

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieves relevant documents for a given query.
        """
        logger.info(f"Retrieving for query: {query}")
        return self.ensemble_retriever.invoke(query)
