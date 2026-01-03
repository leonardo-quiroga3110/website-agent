import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from agent.graph.agent import agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def respond(message, history):
    """
    Handles the chat response from the LangGraph agent.
    """
    try:
        logger.info(f"Processing query: {message}")
        result = await agent.run(message)
        answer = result.get("answer", "I'm sorry, I couldn't find an answer to your question.")
        return answer
    except Exception as e:
        logger.error(f"Error in responder: {e}")
        return f"An error occurred: {str(e)}"

# Define the Gradio Interface
demo = gr.ChatInterface(
    fn=respond,
    title="Monte Azul Expert Agent",
    description="I am an expert agent specialized in Corporación Monte Azul. Ask me anything about our services and projects.",
    examples=["What is Monte Azul Group?", "What is Prado?", "How can I contact sales?"],
)

if __name__ == "__main__":
    # Ensure the app runs correctly in local and HF environments
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
