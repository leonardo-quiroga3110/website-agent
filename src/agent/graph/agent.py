from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from agent.core.state import AgentState
from agent.graph.nodes.research_nodes import reflector, researcher, critic, responder
from agent.core.middleware import (
    ObservabilityMiddleware, 
    GuardrailMiddleware,
    EVENT_SESSION_START, 
    EVENT_SESSION_END
)
from agent.core.config import get_settings
from typing import Dict, Any

settings = get_settings()

class MonteAzulAgent:
    """
    Encapsulates the AlphaCodium Flow for researching Monte Azul Group.
    """
    def __init__(self):
        self.builder = self._build_graph_builder()
        self.graph = None 

    def _should_continue(self, state: AgentState):
        """
        Conditional edge to decide if we need more research.
        """
        if state.get("iterations", 0) >= 5:
            return "responder"
        if state.get("is_sufficient"):
            return "responder"
        return "reflector"

    def _build_graph_builder(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("reflector", reflector)
        workflow.add_node("researcher", researcher)
        workflow.add_node("critic", critic)
        workflow.add_node("responder", responder)
        
        workflow.set_entry_point("reflector")
        workflow.add_edge("reflector", "researcher")
        workflow.add_edge("researcher", "critic")
        
        workflow.add_conditional_edges(
            "critic",
            self._should_continue,
            {
                "reflector": "reflector",
                "responder": "responder"
            }
        )
        workflow.add_edge("responder", END)
        return workflow

    async def run(self, query: str, thread_id: str = "default-thread") -> Dict[str, Any]:
        """
        Execute the agent with a query and thread_id for persistence.
        """
        from langchain_core.messages import HumanMessage
        
        # 1. Apply Input Guardrails
        safe_query = GuardrailMiddleware.apply_input_guardrails(query)
        ObservabilityMiddleware.log_event(EVENT_SESSION_START, {"query": safe_query, "thread_id": thread_id})
        
        # Determine checkpointer based on available configuration
        if settings.DATABASE_URL:
            async with AsyncConnectionPool(conninfo=settings.DATABASE_URL, max_size=20) as pool:
                saver = AsyncPostgresSaver(pool)
                # Setup tables if they don't exist
                await saver.setup()
                graph = self.builder.compile(checkpointer=saver)
                return await self._execute(graph, safe_query, thread_id)
        else:
            # Fallback to no memory or setup local SQLite for testing
            from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
            async with AsyncSqliteSaver.from_conn_string("checkpoints.sqlite") as saver:
                graph = self.builder.compile(checkpointer=saver)
                return await self._execute(graph, safe_query, thread_id)

    async def _execute(self, graph, query, thread_id):
        from langchain_core.messages import HumanMessage
        config = {"configurable": {"thread_id": thread_id}}
        initial_input = {
            "query": query,
            "messages": [HumanMessage(content=query)]
        }
        try:
            result = await graph.ainvoke(initial_input, config)
            if "answer" in result and result["answer"]:
                result["answer"] = GuardrailMiddleware.redact_pii(result["answer"])
            ObservabilityMiddleware.log_event(EVENT_SESSION_END, {"thread_id": thread_id, "status": "success"})
            return result
        except Exception as e:
            ObservabilityMiddleware.log_event("error", {"thread_id": thread_id, "error": str(e)})
            raise e

    async def stream_run(self, query: str, thread_id: str = "default-thread"):
        """
        Stream the agent execution for real-time updates.
        """
        from langchain_core.messages import HumanMessage
        
        safe_query = GuardrailMiddleware.apply_input_guardrails(query)
        ObservabilityMiddleware.log_event(EVENT_SESSION_START, {"query": safe_query, "thread_id": thread_id, "mode": "streaming"})
        
        if settings.DATABASE_URL:
             async with AsyncConnectionPool(conninfo=settings.DATABASE_URL, max_size=20) as pool:
                saver = AsyncPostgresSaver(pool)
                await saver.setup()
                graph = self.builder.compile(checkpointer=saver)
                async for event in graph.astream({"query": safe_query, "messages": [HumanMessage(content=safe_query)]}, {"configurable": {"thread_id": thread_id}}, stream_mode="values"):
                    yield event
        else:
            from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
            async with AsyncSqliteSaver.from_conn_string("checkpoints.sqlite") as saver:
                graph = self.builder.compile(checkpointer=saver)
                async for event in graph.astream({"query": safe_query, "messages": [HumanMessage(content=safe_query)]}, {"configurable": {"thread_id": thread_id}}, stream_mode="values"):
                    yield event
            
        ObservabilityMiddleware.log_event(EVENT_SESSION_END, {"thread_id": thread_id, "status": "success_stream"})

# Instance for easy import
agent = MonteAzulAgent()
