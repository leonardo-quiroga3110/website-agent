import logging
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse
from agent.core.config import get_settings
from agent.graph.agent import agent
from agent.core.whatsapp_client import whatsapp_client
from agent.core.middleware import ObservabilityMiddleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI")
settings = get_settings()

app = FastAPI(title="Monte Azul Website Agent - WABA")

@app.get("/")
async def root():
    return {"status": "online", "agent": "Monte Azul Website Agent"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Handles Meta's webhook verification (GET challenge).
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully!")
        return PlainTextResponse(content=challenge)
    
    logger.warning("Webhook verification failed. Token mismatch.")
    raise HTTPException(status_code=403, detail="Verification failed")

async def process_agent_response(sender_id: str, query: str):
    """
    Background task to process the agent logic and send the response back.
    """
    try:
        # thread_id is the user's phone number for persistent individual memory
        result = await agent.run(query=query, thread_id=sender_id)
        answer = result.get("answer", "Lo siento, no pude procesar tu solicitud.")
        
        # Send back to WhatsApp
        await whatsapp_client.send_text_message(to=sender_id, text=answer)
    except Exception as e:
        logger.error(f"Error in background agent processing: {str(e)}")
        # Optionally send an error message to the user
        await whatsapp_client.send_text_message(to=sender_id, text="Tuvimos un problema técnico. Por favor intenta más tarde.")

@app.post("/webhook")
async def handle_message(request: Request, background_tasks: BackgroundTasks):
    """
    Handles incoming messages from WhatsApp.
    """
    try:
        data = await request.json()
        logger.info(f"Incoming Webhook: {data}")

        # Meta WABA payload extraction
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no_messages"}

        message = messages[0]
        sender_id = message.get("from") # User's WhatsApp ID (phone number)
        message_type = message.get("type")

        if message_type == "text":
            query = message.get("text", {}).get("body")
            message_id = message.get("id")
            logger.info(f"Received message from {sender_id} (ID: {message_id}): {query}")
            
            # 1. Mark as read immediately (shows blue checks to user)
            if message_id:
                background_tasks.add_task(whatsapp_client.mark_as_read, message_id)

            # 2. Run agent in the background to avoid Meta's 10s timeout
            background_tasks.add_task(process_agent_response, sender_id, query)
            
            return {"status": "processing"}

        return {"status": "unsupported_type"}

    except Exception as e:
        logger.error(f"Error handling webhook post: {str(e)}")
        # Always return 200 OK to Meta to acknowledge receipt, even if logic fails
        return {"status": "error", "message": "logged"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
