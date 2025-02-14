# greek_scraper/cli.py

from scrapy.crawler import CrawlerProcess
from greek_scraper.spider import ScraperSpider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, threads
import time

def run_scraper(domain, use_gpu=False, output_file="scraped_data.jsonl", language="greek", threads=1, speed=5):
    """Runs the scraper on a single domain."""
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': threads,  # Threads affect per-domain concurrency
        'DOWNLOAD_DELAY': max(0.05, 1.0 / speed),  # Adjust delay based on speed (lower is faster)
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 1.0,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'LOG_LEVEL': 'ERROR',
        'ITEM_PIPELINES': {
            'greek_scraper.pipelines.TextPipeline': 300,
            'greek_scraper.pipelines.StoragePipeline': 400,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'greek_scraper.middlewares.RobustEncodingMiddleware': 543,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'greek_scraper.middlewares.CustomRetryMiddleware': 544,
        }
    })

    worker_args = {
        'seed_domains': [domain],
        'use_cpu': not use_gpu,
        'output_file': output_file,
        'target_language': language
    }

    process.crawl(ScraperSpider, **worker_args)
    process.start()

def run_multi_scraper(domains, use_gpu=False, output_file="scraped_data.jsonl", language="greek", threads_per_domain=2, batch_size=10, speed=5):
    """Runs the scraper on multiple domains in parallel, efficiently handling concurrency."""
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': threads_per_domain,  # threading per domain
        'DOWNLOAD_DELAY': max(0.05, 1.0 / speed),  # Prevents excessive requests
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 1.0,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'LOG_LEVEL': 'ERROR',
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'greek_scraper.pipelines.TextPipeline': 300,
            'greek_scraper.pipelines.StoragePipeline': 400,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'greek_scraper.middlewares.RobustEncodingMiddleware': 543,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'greek_scraper.middlewares.CustomRetryMiddleware': 544,
        }
    })

    worker_args = {
        'use_cpu': not use_gpu,
        'output_file': output_file,
        'target_language': language
    }

    def run_batch(start_index=0):
        """Process domains in batches to prevent overload."""
        batch = domains[start_index:start_index + batch_size]
        if not batch:
            return

        for domain in batch:
            process.crawl(ScraperSpider, seed_domains=[domain], **worker_args)

        reactor.callLater(10, run_batch, start_index + batch_size)  # Delay next batch to prevent overload

    reactor.callWhenRunning(run_batch)  # Start batch processing when Scrapy initializes
    threads.deferToThread(process.start)  # Run Scrapy in a separate thread to prevent blocking