from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from agent.core.state import AgentState
from agent.graph.nodes.research_nodes import reflector, researcher, critic, responder
from agent.core.middleware import (
    ObservabilityMiddleware, 
    GuardrailMiddleware,
    EVENT_SESSION_START, 
    EVENT_SESSION_END
)
from typing import Dict, Any

class MonteAzulAgent:
    """
    Encapsulates the AlphaCodium Flow for researching Monte Azul Group.
    """
    def __init__(self):
        self.builder = self._build_graph_builder()
        self.graph = None # Will be compiled per request with checkpointer

    def _should_continue(self, state: AgentState):
        """
        Conditional edge to decide if we need more research.
        """
        # Safety break to avoid infinite loops
        if state.get("iterations", 0) >= 5:
            return "responder"
            
        # Check the critic's output
        if state.get("is_sufficient"):
            return "responder"
        
        return "reflector"

    def _build_graph_builder(self):
        # 1. Initialize the graph with our state
        workflow = StateGraph(AgentState)
        
        # 2. Add nodes
        workflow.add_node("reflector", reflector)
        workflow.add_node("researcher", researcher)
        workflow.add_node("critic", critic)
        workflow.add_node("responder", responder)
        
        # 3. Define the edges
        workflow.set_entry_point("reflector")
        
        workflow.add_edge("reflector", "researcher")
        workflow.add_edge("researcher", "critic")
        
        # Conditional edge from critic
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

    def get_graph_image(self):
        """
        Returns the PNG bytes of the graph visualization.
        """
        if not self.graph:
            # Fallback compile for visualization if not run yet
            self.graph = self.builder.compile()
        return self.graph.get_graph().draw_mermaid_png()

    async def run(self, query: str, thread_id: str = "default-thread") -> Dict[str, Any]:
        """
        Execute the agent with a query and thread_id for persistence.
        """
        from langchain_core.messages import HumanMessage
        
        # 1. Apply Input Guardrails (PII Redaction)
        safe_query = GuardrailMiddleware.apply_input_guardrails(query)
        
        ObservabilityMiddleware.log_event(EVENT_SESSION_START, {"query": safe_query, "thread_id": thread_id})
        
        import os
        db_path = "/app/data/checkpoints.sqlite" if os.path.exists("/app/data") else "checkpoints.sqlite"
        
        async with AsyncSqliteSaver.from_conn_string(db_path) as saver:
            # Compile graph with saver
            graph = self.builder.compile(checkpointer=saver)
            
            config = {"configurable": {"thread_id": thread_id}}
            initial_input = {
                "query": safe_query,
                "messages": [HumanMessage(content=safe_query)]
            }
            
            try:
                result = await graph.ainvoke(initial_input, config)
                
                # 2. Apply Output Guardrails (PII Redaction)
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
        # Use a persistent path for cloud deployments if available
        # Render Disks usually mount to /app/data or /data
        import os
        db_path = "/app/data/checkpoints.sqlite" if os.path.exists("/app/data") else "checkpoints.sqlite"
        
        async with AsyncSqliteSaver.from_conn_string(db_path) as saver:
            graph = self.builder.compile(checkpointer=saver)
            self.graph = graph
            
            config = {"configurable": {"thread_id": thread_id}}
            initial_input = {
                "query": safe_query,
                "messages": [HumanMessage(content=safe_query)]
            }
            
            async for event in graph.astream(initial_input, config, stream_mode="values"):
                yield event
            
            ObservabilityMiddleware.log_event(EVENT_SESSION_END, {"thread_id": thread_id, "status": "success_stream"})

# Instance for easy import
agent = MonteAzulAgent()
