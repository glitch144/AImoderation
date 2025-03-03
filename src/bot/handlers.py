from telegram import Update
from telegram.ext import ContextTypes
import logging
from config import settings
from src.database.db_handler import (
    update_user_chat_history,
    clear_user_chat_history,
    log_moderation_action,
    get_user_chat_history
)
from src.services.openrouter import OpenRouterService
from src.detection.phishing_detector import PhishingDetector

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize services
openrouter = OpenRouterService()
phishing_detector = PhishingDetector()

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    start_text = """
🛡️ Welcome to the Cybersecurity Context Analyzer Bot!

I help analyze and summarize cybersecurity-related conversations. Here's what I can do:

- Maintain context of last 35 messages
- Identify security vulnerabilities and risks
- Analyze threat actor tactics and techniques
- Suggest mitigation strategies
- Highlight security best practices

🔍 Available commands:
/start - Show this introduction
/summarize - Generate security analysis of recent messages
/clear - Reset conversation context
/help - Detailed help information

I specialize in cybersecurity topics including:
• Network security • Malware analysis
• Incident response • Threat intelligence
• Vulnerability management • Security architecture

Simply chat normally and use /summarize when you want an analysis!
"""
    await update.message.reply_text(start_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with two-stage moderation"""
    try:
        message = update.message
        user_id = message.from_user.id
        chat_id = message.chat_id
        message_id = message.message_id
        message_text = message.text

        # Store message in context history
        update_user_chat_history(user_id, message_text)

        # Only moderate in groups
        if message.chat.type in ['group', 'supergroup']:
            # Stage 1: Fast pre-check
            if phishing_detector.pre_analysis(message_text):
                # Delete message immediately
                await message.delete()
                logger.info(f"Message deleted (pre-check): {message_text[:50]}...")

                # Stage 2: AI verification
                result = await openrouter.check_phishing(message_text)

                if result and isinstance(result, dict):  # Ensure result is a dictionary
                    if result.get('is_phishing', False):
                        # Confirmed phishing - log and notify
                        log_moderation_action(
                            user_id=user_id,
                            chat_id=chat_id,
                            message_id=message_id,
                            content=message_text,
                            decision="deleted"
                        )

                        await context.bot.send_message(
                            chat_id=int(settings.ADMIN_GROUP_ID),
                            text=f"🚨 Confirmed phishing message deleted:\n\n"
                                 f"• User: @{message.from_user.username}\n"
                                 f"• Confidence: {result.get('confidence', 'N/A')}%\n"
                                 f"• Reasons: {', '.join(result.get('reasons', ['Unknown']))}\n"
                                 f"• Snippet: {message_text[:100]}..."
                        )
                    else:
                        # False positive - restore message
                        await context.bot.forward_message(
                            chat_id=chat_id,
                            from_chat_id=chat_id,
                            message_id=message_id
                        )
                        logger.info(f"Message restored (false positive): {message_text[:50]}...")

                        # Notify admins
                        await context.bot.send_message(
                            chat_id=int(settings.ADMIN_GROUP_ID),
                            text=f"⚠️ False positive detected - message restored:\n\n"
                                 f"• User: @{message.from_user.username}\n"
                                 f"• Snippet: {message_text[:100]}..."
                        )
                else:
                    # AI check failed - keep message deleted
                    logger.error("AI verification failed - message remains deleted")
                    await context.bot.send_message(
                        chat_id=int(settings.ADMIN_GROUP_ID),
                        text=f"⚠️ AI verification failed - message remains deleted:\n\n"
                             f"• User: @{message.from_user.username}\n"
                             f"• Snippet: {message_text[:100]}..."
                    )

    except Exception as e:
        logger.error(f"Message handler error: {str(e)}")

async def handle_summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /summarize command"""
    try:
        user_id = update.message.from_user.id
        history = get_user_chat_history(user_id)

        if not history:
            await update.message.reply_text("No messages to summarize!")
            return

        summary = await openrouter.get_summary(history)
        await update.message.reply_text(f"Summary:\n{summary}")
    except Exception as e:
        logger.error(f"Summarize error: {str(e)}")
        await update.message.reply_text("Error generating summary")

async def handle_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command"""
    try:
        user_id = update.message.from_user.id
        clear_user_chat_history(user_id)
        await update.message.reply_text("🛡️ Security context cleared successfully!")
    except Exception as e:
        logger.error(f"Clear error: {str(e)}")
        await update.message.reply_text("Error clearing context")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🛡️ Cybersecurity Context Bot Help:

/summarize - Generate security analysis of last 35 messages
/clear - Reset conversation context
/help - Show this help message

This bot focuses on cybersecurity analysis. It will:
- Identify potential vulnerabilities
- Highlight security best practices
- Analyze threat actor tactics
- Suggest mitigation strategies

📝 Just chat normally and use /summarize when ready!
"""
    await update.message.reply_text(help_text)