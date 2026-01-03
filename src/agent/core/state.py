import operator
from typing import Annotated, TypedDict, List, Any, Dict, Set
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of our autonomous website research agent.
    """
    # The user's original query or goal
    query: str
    
    # Internal flow control
    plan: List[str]            # Steps to be executed
    completed_steps: List[str] # Audit trail of what's already done
    reflection: str           # LLM's self-critique/reflection
    iterations: int            # Safety counter to prevent infinite loops
    is_sufficient: bool = False # Flag for iterative research completion
    
    # Data aggregation
    # research stores a list of dictionaries (e.g., {"url": "...", "content": "..."})
    research: List[Dict[str, Any]] 
    # track visited URLs to avoid redundant scraping or loops
    visited_urls: Set[str]
    
    # Final structured output or final answer
    answer: str | None
    
    # Standard LangGraph messages
    # Annotated with operator.add ensures that new messages are appended
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Error stores any error messages encountered during execution
    error: str | None
