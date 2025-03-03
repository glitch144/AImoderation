import aiohttp
import json
import logging
from config import settings

logger = logging.getLogger(__name__)

class OpenRouterService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

    async def check_phishing(self, message_text: str) -> dict:
        """Check if message contains phishing attempts using OpenRouter API"""
        payload = {
            "model": settings.MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """Analyze this message for phishing indicators. Respond with JSON:
{
    "is_phishing": boolean,
    "confidence": 0-100,
    "reasons": [strings],
    "should_delete": boolean
}"""
                },
                {
                    "role": "user",
                    "content": message_text
                }
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    settings.OPENROUTER_URL,
                    json=payload,
                    headers=self.headers
                ) as response:
                    # Log the response status and body for debugging
                    response_text = await response.text()
                    logger.debug(f"OpenRouter Response: {response.status} - {response_text}")

                    # Check for empty response
                    if not response_text.strip():
                        logger.error("OpenRouter returned an empty response")
                        return None

                    # Parse JSON response
                    try:
                        data = json.loads(response_text)
                        # Extract the content field and parse it as JSON
                        content = data['choices'][0]['message']['content']
                        return json.loads(content)  # Parse the inner JSON string
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Failed to parse OpenRouter response: {str(e)}")
                        logger.error(f"Raw response: {response_text}")
                        return None

        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during phishing check: {str(e)}")
            return None

    async def get_summary(self, messages: list) -> str:
        """Generate a summary of the conversation using OpenRouter API"""
        payload = {
            "model": settings.MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """Summarize the following conversation in 5 bullet points:"""
                },
                {
                    "role": "user",
                    "content": "\n".join(messages)
                }
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    settings.OPENROUTER_URL,
                    json=payload,
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return "⚠️ Error generating summary. Please try again later."