from langgraph.graph import StateGraph, END
from agent.core.state import AgentState
from agent.graph.nodes.research_nodes import reflector, researcher, critic, responder

def should_continue(state: AgentState):
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

def create_alpha_codium_graph():
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
        should_continue,
        {
            "reflector": "reflector",
            "responder": "responder"
        }
    )
    
    workflow.add_edge("responder", END)
    
    # 4. Compile the graph
    return workflow.compile()

# Instance of the graph
graph = create_alpha_codium_graph()
