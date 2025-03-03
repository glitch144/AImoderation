import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import settings
from src.database.db_handler import init_db
from src.bot.handlers import (
    handle_start,
    handle_summarize,
    handle_clear,
    handle_help,
    handle_message
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.LOG_LEVEL,
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('bot.log')  # Log to file
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Validate environment variables
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set!")
        return
    if not settings.ADMIN_GROUP_ID:
        logger.error("ADMIN_GROUP_ID is not set!")
        return

    # Initialize database
    init_db()

    try:
        # Create Telegram application
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Register handlers
        handlers = [
            CommandHandler("start", handle_start),
            CommandHandler("summarize", handle_summarize),
            CommandHandler("clear", handle_clear),
            CommandHandler("help", handle_help),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        ]
        
        for handler in handlers:
            application.add_handler(handler)

        logger.info("Starting bot...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()