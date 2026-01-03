import gradio as gr
import asyncio
from agent.graph.agent import agent
from agent.core.config import get_settings

settings = get_settings()

async def predict(message, history, session_id):
    """
    Connects the Gradio UI to the Agent's streaming execution.
    """
    if not session_id:
        session_id = "gradio-user"
        
    response_text = ""
    async for event in agent.stream_run(query=message, thread_id=session_id):
        # 1. Update with status updates (research progress)
        if "completed_steps" in event:
            latest_step = event["completed_steps"][-1]
            yield f"⏳ {latest_step}..."
            
        # 2. Final Answer
        if "answer" in event:
            response_text = event["answer"]
            yield response_text

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# 🤖 Monte Azul Website Agent")
        gr.Markdown("Expert research assistant for https://www.monteazulgroup.com/es")
        
        with gr.Row():
            session_id = gr.Textbox(
                label="Session ID / Name", 
                placeholder="Enter a unique ID to test memory",
                value="demo-user"
            )
        
        chat = gr.ChatInterface(
            fn=predict,
            additional_inputs=[session_id],
            examples=[
                ["¿Qué servicios ofrece Monte Azul?", "demo-user"],
                ["¿Quiénes son los directivos?", "demo-user"]
            ],
            cache_examples=False
        )
        
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())

if __name__ == "__main__":
    launch_ui()
