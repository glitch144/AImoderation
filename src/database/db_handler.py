import sqlite3
import logging
from datetime import datetime
from config.settings import DB_NAME, MAX_CONTEXT_LENGTH

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database with required tables"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # User context table
        c.execute('''CREATE TABLE IF NOT EXISTS user_context
                     (user_id INTEGER PRIMARY KEY,
                      chat_history TEXT,
                      last_updated TIMESTAMP)''')
        
        # Moderation log table
        c.execute('''CREATE TABLE IF NOT EXISTS moderation_log
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      chat_id INTEGER,
                      message_id INTEGER,
                      content TEXT,
                      decision TEXT,
                      timestamp TIMESTAMP)''')
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        conn.close()

def get_user_chat_history(user_id):
    """Retrieve chat history for a user"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT chat_history FROM user_context WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return eval(result[0]) if result else []
    except Exception as e:
        logger.error(f"Failed to get chat history: {str(e)}")
        return []
    finally:
        conn.close()

def update_user_chat_history(user_id, new_message):
    """Update chat history for a user"""
    try:
        history = get_user_chat_history(user_id)
        history.append(new_message)
        
        # Keep only last MAX_CONTEXT_LENGTH messages
        if len(history) > MAX_CONTEXT_LENGTH:
            history = history[-MAX_CONTEXT_LENGTH:]
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO user_context 
                     (user_id, chat_history, last_updated) 
                     VALUES (?, ?, ?)''',
                  (user_id, str(history), datetime.now()))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to update chat history: {str(e)}")
        raise
    finally:
        conn.close()

def clear_user_chat_history(user_id):
    """Clear chat history for a user"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM user_context WHERE user_id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to clear chat history: {str(e)}")
        raise
    finally:
        conn.close()

def log_moderation_action(user_id, chat_id, message_id, content, decision):
    """Log moderation actions"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO moderation_log 
                     (user_id, chat_id, message_id, content, decision, timestamp)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, chat_id, message_id, content, decision, datetime.now()))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log moderation action: {str(e)}")
        raise
    finally:
        conn.close()