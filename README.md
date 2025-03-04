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
