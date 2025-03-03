import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_NAME = os.getenv("DB_NAME", "chat_context.db")  # Default to 'chat_context.db' if not set
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 35))  # Default to 35 messages

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Required
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")  # Required for admin notifications

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Required
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-r1-distill-llama-70b:free")

# Moderation Configuration
PHISHING_CONFIDENCE_THRESHOLD = int(os.getenv("PHISHING_CONFIDENCE_THRESHOLD", 75))  # Default 75%
MODERATION_COOLDOWN = int(os.getenv("MODERATION_COOLDOWN", 15))  # Default 15 seconds

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default to INFO level logging