import logging
import time
import json
import re
from datetime import datetime
from typing import Dict, Any, Callable, Awaitable, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from agent.core.state import AgentState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentMiddleware")

class ObservabilityMiddleware:
    """
    Handles logging, analytics, and performance tracking.
    """
    
    @staticmethod
    def log_node_execution(node_name: str):
        """
        Decorator for nodes to log their execution and timing.
        """
        def decorator(func: Callable[[AgentState], Awaitable[Dict[str, Any]]]):
            async def wrapper(state: AgentState) -> Dict[str, Any]:
                start_time = time.time()
                logger.info(f"[NODE START] {node_name} - Thread: {state.get('thread_id', 'unknown')}")
                
                try:
                    result = await func(state)
                    duration = time.time() - start_time
                    logger.info(f"[NODE END] {node_name} completed in {duration:.2f}s")
                    
                    return result
                except Exception as e:
                    logger.error(f"[NODE ERROR] {node_name} failed: {str(e)}")
                    raise e
            return wrapper
        return decorator

    @staticmethod
    def log_event(event_type: str, details: Dict[str, Any]):
        """
        Logs a generic event for analytics.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "details": details
        }
        logger.info(f"[EVENT] {json.dumps(log_entry)}")

class GuardrailMiddleware:
    """
    Handles security, privacy (PII), and usage limits.
    """
    PII_PATTERNS = {
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "phone": r"\+?\d{10,15}",
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
    }

    @staticmethod
    def redact_pii(text: str) -> str:
        """
        Redacts PII from the given text.
        """
        redacted_text = text
        for pii_type, pattern in GuardrailMiddleware.PII_PATTERNS.items():
            redacted_text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", redacted_text)
        return redacted_text

    @staticmethod
    def check_rate_limit(thread_id: str, history: List[Any], limit: int = 20) -> bool:
        """
        Simple rate limit check based on history size.
        """
        if len(history) > limit:
            logger.warning(f"[GUARDRAIL] Rate limit exceeded for thread: {thread_id}")
            return False
        return True

    @staticmethod
    def apply_input_guardrails(query: str) -> str:
        """
        Cleans and redacts PII from incoming user queries.
        """
        clean_query = GuardrailMiddleware.redact_pii(query)
        if clean_query != query:
            logger.info("[GUARDRAIL] PII redacted from input query")
        return clean_query

# Simple event types constants
EVENT_TOOL_CALL = "tool_call"
EVENT_LLM_INVOCATION = "llm_invocation"
EVENT_ERROR = "error"
EVENT_SESSION_START = "session_start"
EVENT_SESSION_END = "session_end"
