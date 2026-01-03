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
        # We look for the 'answer' in the state updates
        if "answer" in event:
            response_text = event["answer"]
            yield response_text
        elif "messages" in event:
            # Optionally show research progress here
            pass

def launch_ui():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
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
            examples=["¿Qué servicios ofrece Monte Azul?", "¿Quiénes son los directivos?"],
            cache_examples=False
        )
        
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    launch_ui()
