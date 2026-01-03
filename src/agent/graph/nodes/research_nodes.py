from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from agent.core.llm import get_llm
from agent.core.state import AgentState
from agent.core.prompts import (
    REFLECTOR_SYSTEM_PROMPT, 
    CRITIC_SYSTEM_PROMPT, 
    RESPONDER_SYSTEM_PROMPT
)
from agent.core.retrieval import RAGRetriever
from agent.core.middleware import ObservabilityMiddleware
import json
from pydantic import BaseModel, Field

# --- Pydantic Models for Structured Output ---

class ReflectionPlan(BaseModel):
    reflection: str = Field(description="Self-critique of existing knowledge.")
    plan: List[str] = Field(description="List of specific search queries or URLs to research next.")

class ResearchSufficiency(BaseModel):
    is_sufficient: bool = Field(description="True if info is complete, False otherwise.")
    reasoning: str = Field(description="Explanation of why research is/isn't sufficient.")

# Initialize Retriever
retriever = RAGRetriever()

# --- Node Functions ---

@ObservabilityMiddleware.log_node_execution("reflector")
async def reflector(state: AgentState) -> Dict[str, Any]:
    llm = get_llm().with_structured_output(ReflectionPlan)
    
    # Summarize existing research
    research_summary = ""
    for r in state.get("research", []):
        research_summary += f"Chunk: {r['content'][:300]}...\nSource: {r['url']}\n\n"
    
    context = f"""
    Current Iteration: {state.get('iterations', 0)}
    Retrieved Context: {research_summary if research_summary else "No info retrieved yet."}
    """
    
    result = await llm.ainvoke([
        SystemMessage(content=REFLECTOR_SYSTEM_PROMPT),
        HumanMessage(content=f"User Query: {state['query']}\nContext: {context}")
    ])
    
    # In RAG mode, the plan consists of search queries for our local index
    return {
        "reflection": result.reflection,
        "plan": result.plan,
        "iterations": state.get("iterations", 0) + 1
    }

@ObservabilityMiddleware.log_node_execution("researcher")
async def researcher(state: AgentState) -> Dict[str, Any]:
    new_research = list(state.get("research", []))
    completed = list(state.get("completed_steps", []))
    import asyncio
    
    # If no plan, use the query itself
    queries = state["plan"] if state["plan"] else [state["query"]]
    
    # Define an async retrieval helper
    async def retrieve_query(q):
        try:
            # We wrap the non-async retrieve in an executor if it blocks, 
            # but since we want to be fast, we run them in parallel.
            # If retriever.retrieve is blocking (no ainvoke), we run it in a thread.
            loop = asyncio.get_event_loop()
            docs = await loop.run_in_executor(None, retriever.retrieve, q)
            return q, docs
        except Exception as e:
            print(f"DEBUG: Researcher error for {q}: {e}")
            return q, []

    # Run all queries in parallel
    results = await asyncio.gather(*[retrieve_query(q) for q in queries])
    
    for q, docs in results:
        for doc in docs:
            content_preview = doc.page_content[:100]
            if not any(content_preview in r['content'] for r in new_research):
                new_research.append({
                    "url": doc.metadata.get("source", "Monte Azul Website"),
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
        completed.append(f"Retrieved context for: {q}")
    
    # Early termination: if no new research found after first attempt
    is_sufficient = state.get("is_sufficient", False)
    if len(new_research) == len(state.get("research", [])) and state.get("iterations", 0) > 0:
        is_sufficient = True

    return {
        "research": new_research,
        "completed_steps": completed,
        "plan": [],
        "is_sufficient": is_sufficient
    }

@ObservabilityMiddleware.log_node_execution("critic")
async def critic(state: AgentState) -> Dict[str, Any]:
    # Optimization: Use a faster model for the critic (gpt-4o-mini) 
    # to reduce internal latency without sacrificing final answer quality.
    llm = get_llm(model_name="gpt-4o-mini").with_structured_output(ResearchSufficiency)
    
    # Since we only have one source, the critic mainly evaluates 
    # if the scraped content is enough for the specific question.
    research_meta = "\n".join([f"- {r['url']}" for r in state.get("research", [])])
    
    result = await llm.ainvoke([
        SystemMessage(content=CRITIC_SYSTEM_PROMPT),
        HumanMessage(content=f"Query: {state['query']}\nSource available: {research_meta}")
    ])
    
    return {
        "is_sufficient": result.is_sufficient,
        "reflection": f"Critic Evaluation: {result.reasoning}"
    }

@ObservabilityMiddleware.log_node_execution("responder")
async def responder(state: AgentState) -> Dict[str, Any]:
    llm = get_llm()
    from langchain_core.messages import AIMessage
    
    # Provide the full content of the official site since it's only one page
    context_data = []
    for r in state.get("research", []):
        context_data.append({
            "url": r["url"],
            "content": str(r["content"])[:8000] # Allow more content as it's the only source
        })
    
    # Construct message list: system + history + context/query
    messages = [
        SystemMessage(content=RESPONDER_SYSTEM_PROMPT),
        *state.get("messages", []),
        HumanMessage(content=f"Context and Query Details: {json.dumps(context_data)}")
    ]
    
    response = await llm.ainvoke(messages)
    
    return {
        "answer": response.content,
        "messages": [AIMessage(content=response.content)]
    }
