# greek_scraper/cli.py
import argparse
import os
from scrapy.crawler import CrawlerProcess
from greek_scraper.spider import ScraperSpider  # Import your spider from spider.py
from greek_scraper import get_config # Import get_config

def main():
    parser = argparse.ArgumentParser(description="Generic Web Scraper with Language Options and GPU Acceleration")

    # 1. Default Generic, Language Parameter for Greek
    parser.add_argument('--language', type=str, default=None, help='Target language for scraping (e.g., "gr" or "greek" for Greek). Default is generic scraping.')

    # 2. Accept 1 URL parameter or domains file
    group = parser.add_mutually_exclusive_group() # Make url and domains_file mutually exclusive
    group.add_argument('--url', type=str, help='URL to scrape directly (overrides --domains_file)')
    group.add_argument('--domains_file', default="", help='File path with comma-separated list of seed domains')

    # 3. Change jobdir preferences (default preserved)
    parser.add_argument('--jobdir', default='scraper_job', help='Directory to store job state for resuming (default: scraper_job)')

    # 4. Choose CPU or GPU (default GPU)
    parser.add_argument('--use_cpu', action='store_true', help='Force CPU usage instead of GPU (if cupy/CUDA issues occur). GPU is default.')

    # 5. Parameterize JSONL output path (default generic filename)
    parser.add_argument('--output_file', default='scraped_data_robust.jsonl', help='Path to save the JSONL output file (default: scraped_data_robust.jsonl in current directory)')

    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0') # Version argument

    args = parser.parse_args()

    language_config = get_config()
    language_param = args.language or language_config.get('language')
    language_display = language_param if language_param else "Generic (No Language Filtering)" # More explicit display

    seed_domains = []
    if args.url:
        seed_domains = [args.url]
        print(f"[Main] Scraping single URL: {args.url}")
    elif args.domains_file:
        if os.path.exists(args.domains_file):
            with open(args.domains_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                seed_domains = [d.strip() for d in content.split(',') if d.strip()]
            print(f"[Main] Loaded {len(seed_domains)} seed domains from {args.domains_file}")
        else:
            print(f"[Main] File not found: {args.domains_file}")
    else:
        print("[Main] WARNING: No domains file or URL provided. Scraping might not start unless seed domains are added programmatically. Please provide a --domains_file or --url argument to begin scraping.") # More actionable warning


    # Create worker arguments for the spider, passing the parameters
    worker_args = {
        'seed_domains': seed_domains,
        'autodiscover': False, # You can add --autodiscover to parser if needed
        'max_domains': 5000, # You can parameterize this too if needed with --max_domains
        'use_cpu': args.use_cpu, # Pass use_cpu flag to spider
        'output_file': args.output_file, # Pass output_file path
        'target_language': language_param # Pass target language
    }

    # Settings - inherit most from spider's custom_settings, override from command line
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'CONCURRENT_REQUESTS': 1000,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'DOWNLOAD_DELAY': 0.125,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 1.0,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'LOG_LEVEL': 'WARNING',
        'COOKIES_ENABLED': False,
        'DEPTH_LIMIT': 3,
        'ROBOTSTXT_OBEY': True,
        'ITEM_PIPELINES': {
            'greek_scraper.pipelines.TextPipeline': 300, # Use package-aware path
            'greek_scraper.pipelines.StoragePipeline': 400, # Use package-aware path
        },
        'JOBDIR': args.jobdir,
        'DOWNLOADER_MIDDLEWARES': {
            'greek_scraper.middlewares.RobustEncodingMiddleware': 543, # Use package-aware path
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'greek_scraper.middlewares.CustomRetryMiddleware': 544, # Use package-aware path
        }
    }

    print(f"[Main] Starting crawler with JOBDIR: {args.jobdir}, Output File: {args.output_file}, CPU Mode: {args.use_cpu}, Target Language: {language_display}, Worker args: {worker_args}")
    process = CrawlerProcess(settings=settings)
    process.crawl(ScraperSpider, **worker_args) # Use ScraperSpider class, pass worker_args
    process.start()
    print("[Main] Crawling finished. Data stored in JSON & JSONL.")

if __name__ == "__main__":
    main()