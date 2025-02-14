# greek_scraper/__init__.py
_language_config = {}

def config(language=None):
    """
    Configures the scraper for specific settings, e.g., language.
    """
    global _language_config
    _language_config['language'] = language
    print(f"[greek_scraper] Configured with language: {language}")

def get_config():
    """
    Returns the current configuration.
    """
    return _language_config

from .cli import main # Optionally re-export main function for direct import