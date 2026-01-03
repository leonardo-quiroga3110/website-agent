import httpx
import logging
from agent.core.config import get_settings

logger = logging.getLogger("WhatsAppClient")
settings = get_settings()

class WhatsAppClient:
    """
    Client for interacting with the WhatsApp Business API.
    """
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"

    async def send_text_message(self, to: str, text: str):
        """
        Sends a simple text message back to the user.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Message sent successfully to {to}")
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to send message: {e.response.text}")
                raise e
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                raise e

# Instance for easy use
whatsapp_client = WhatsAppClient()
