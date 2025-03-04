# AI-Powered Telegram Moderation Bot

An advanced Telegram bot combining AI moderation, phishing detection, and conversation summarization using OpenRouter API.

## Table of Contents
1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Database Schema](#database-schema)
8. [Security Considerations](#security-considerations)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgments](#acknowledgments)

## Features
- **AI-Powered Moderation**
  - Two-stage phishing detection (rule-based + AI verification)
  - Automatic message deletion with admin alerts
  - Suspicious pattern logging
- **Conversation Management**
  - Context-aware summarization of last 35 messages
  - User-specific chat history storage
  - Manual context clearing
- **Security Focus**
  - Cybersecurity-specific analysis
  - Threat actor tactic identification
  - Mitigation strategy suggestions
- **Analytics**
  - SQLite-based moderation logs
  - Performance metrics tracking
  - Confidence threshold configuration

## Architecture

```
└── 📁AImoderation
    └── 📁config
        └── __init__.py
        └── keywords.py
        └── settings.py
    └── 📁src
        └── __init__.py
        └── 📁bot
            └── __init__.py
            └── handlers.py
        └── 📁database
            └── __init__.py
            └── db_handler.py
        └── 📁detection
            └── __init__.py
            └── phishing_detector.py
        └── 📁services
            └── __init__.py
            └── openrouter.py
    └── bot.log
    └── chat_context.db
    └── main.py
    └── README.md
    └── requirements.txt

```

### Key Files
- **config/**
  - `keywords.py`: Phishing patterns and domain lists
  - `settings.py`: Environment configurations
- **src/bot/**
  - `handlers.py`: Telegram command handlers
- **src/database/**
  - `db_handler.py`: Database operations
- **src/detection/**
  - `phishing_detector.py`: Phishing detection logic
- **src/services/**
  - `openrouter.py`: OpenRouter API integration
- **Root Files**
  - `main.py`: Application entry point
  - `requirements.txt`: Python dependencies
  - `chat_context.db`: SQLite database
  - `bot.log`: Application logs

## Installation

### Prerequisites
- Python 3.10+
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- OpenRouter API key
- Linux/Windows/macOS with 4GB+ RAM

### Setup
1. Clone repository:
```bash
git clone https://github.com/yourusername/ai-telegram-moderation.git
cd ai-telegram-moderation

```
2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```
3. install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```
## Configuration
### Environment Variables (.env)

```ini
TELEGRAM_BOT_TOKEN=your_bot_token
OPENROUTER_API_KEY=your_api_key
DB_NAME=chat_context.db
LOG_LEVEL=INFO
MODERATION_COOLDOWN=15
PHISHING_THRESHOLD=75
```

### Phishing Patterns (config/keywords.py)
 ```python
 PHISHING_KEYWORDS = [
    "verify your account",
    "urgent response needed",
    # add your list here
]

TRUSTED_DOMAINS = {
    'yourcompany.com',
    'trusted-partner.org'

}

SHORTENER_DOMAINS = {
    'bit.ly', 'goo.gl', 'tinyurl.com'
}
```
## Usage 
### Starting the bot
 ```bash 
 python main.py
 ```
### Commands

| Command       | Description                                  | Example                   |
|---------------|----------------------------------------------|---------------------------|
| `/start`      | Show introduction and capabilities          | `/start`                  |
| `/summarize`  | Generate security-focused summary           | `/summarize`              |
| `/clear`      | Reset conversation context                  | `/clear`                  |
| `/help`       | Show detailed usage instructions            | `/help`                   |
