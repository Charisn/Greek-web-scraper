# greek_scraper/__init__.py

from .cli import run_scraper, run_multi_scraper

# Default configurations
_config = {
    'use_gpu': False,
    'output_path': 'scraped_data.jsonl',
    'language': 'greek',
    'threads': 1,
    'speed': 5,  # Default scraping speed (1-10)
    'separator': ',',
}

def scrape(domain):
    """Scrapes a single domain using the current config settings."""
    return run_scraper(
        domain,
        use_gpu=_config['use_gpu'],
        output_file=_config['output_path'],
        language=_config['language'],
        threads=_config['threads'],
        speed=_config['speed']
    )

def multi_scrape(domains, separator=','):
    """Scrapes multiple domains from an array."""
    if isinstance(domains, str):
        domains = domains.split(separator)
    return run_multi_scraper(
        domains,
        use_gpu=_config['use_gpu'],
        output_file=_config['output_path'],
        language=_config['language'],
        threads=_config['threads'],
        speed=_config['speed']
    )

def from_file(filepath, separator=','):
    """Reads domains from a file and scrapes them."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            domains = [line.strip() for line in f.read().split(separator) if line.strip()]
        return multi_scrape(domains, separator)
    except FileNotFoundError:
        print(f"[greek_scraper] ERROR: File '{filepath}' not found.")
        return None

def gpu(enabled):
    """Enable or disable GPU processing."""
    _config['use_gpu'] = bool(enabled)
    print(f"[greek_scraper] GPU Processing: {'Enabled' if enabled else 'Disabled'}")

def output_path(path):
    """Set the output file path."""
    _config['output_path'] = path
    print(f"[greek_scraper] Output Path Set: {path}")

def language(lang):
    """Set the scraping language (default: Greek)."""
    _config['language'] = lang
    print(f"[greek_scraper] Language Set: {lang}")

def threads(num):
    """Set the number of threads (1 thread = 1 domain)."""
    try:
        _config['threads'] = max(1, int(num))
        print(f"[greek_scraper] Threads Set: {_config['threads']}")
    except ValueError:
        print("[greek_scraper] ERROR: Invalid thread count. Must be an integer.")

def speed(value):
    """Scale the scraping speed (1-10)."""
    try:
        _config['speed'] = min(10, max(1, int(value)))
        print(f"[greek_scraper] Speed Set: {_config['speed']}")
    except ValueError:
        print("[greek_scraper] ERROR: Speed must be between 1 and 10.")
