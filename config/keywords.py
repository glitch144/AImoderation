# Phishing keywords and patterns
PHISHING_KEYWORDS = [
    # Account & Verification
    "verify your account", "account suspension", "unusual login activity", 
    "security alert", "confirm your identity", "account deactivation",
    "unauthorized access", "reactivate your account", "action required",
    "account verification failed", "limited-time security check",
    "identity confirmation", "account restriction", "update account details",
    "expiring soon", "account locked", "verify immediately",
    "suspicious activity detected", "login credentials expired",
    "account access revoked",

    # Urgency & Fear
    "immediate action required", "urgent response needed", "deadline approaching",
    "last warning", "account termination", "legal action pending",
    "security breach", "critical alert", "failure to comply",
    "your attention is required", "time-sensitive", "overdue notice",
    "emergency update", "take action now", "restricted access",
    "immediate response necessary", "critical security measure",
    "act now to avoid penalties", "urgent account review",
    "security update pending", "24-hour notice", "final reminder",
    "immediate verification required",

    # Add more categories as needed...
]

# Trusted domains (whitelist)
TRUSTED_DOMAINS = {
    'yourcompany.com',  # Add your actual trusted domains
    'trusted-partner.org',
    'example.com'
}

# Known URL shorteners
SHORTENER_DOMAINS = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly',
    'shorte.st', 't.co', 'bit.do', 'mcaf.ee', 'rebrand.ly', 'linktr.ee'
}

# Urgency patterns (regex)
URGENCY_PATTERNS = [
    r'\b(immediate action required)\b',
    r'\b(account (verification|suspension))\b',
    r'\bwithin (24|48) hours\b'
]

# Export all variables
__all__ = [
    'PHISHING_KEYWORDS',
    'TRUSTED_DOMAINS',
    'SHORTENER_DOMAINS',
    'URGENCY_PATTERNS'
]