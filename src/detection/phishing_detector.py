import re
import tldextract
from config.keywords import PHISHING_KEYWORDS, TRUSTED_DOMAINS, SHORTENER_DOMAINS

class PhishingDetector:
    def __init__(self):
        self.keyword_patterns = self._compile_patterns()
        
    def _compile_patterns(self):
        return [
            re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            for keyword in PHISHING_KEYWORDS
        ]

    def pre_analysis(self, text):
        text_lower = text.lower()
        
        # Keyword matching
        if any(pattern.search(text_lower) for pattern in self.keyword_patterns[:5]):  # Check first 5 as sample
            return True
            
        # URL analysis
        urls = re.findall(r'https?://\S+', text)
        if urls:
            for url in urls:
                try:
                    domain_info = tldextract.extract(url)
                    full_domain = f"{domain_info.domain}.{domain_info.suffix}"
                    
                    if full_domain in SHORTENER_DOMAINS:
                        return True
                        
                    if any(trusted in full_domain for trusted in TRUSTED_DOMAINS) and full_domain not in TRUSTED_DOMAINS:
                        return True
                        
                except Exception:
                    continue
                    
        return False