# greek_scraper/spider.py
import scrapy
import cupy as cp
import re
import json
import os
import numpy as np
import argparse
import html
import chardet
import unicodedata
from urllib.parse import urlparse, urljoin
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from trafilatura import extract  # robust text extraction
from tldextract import extract as tld_extract
from bs4 import BeautifulSoup  # For alternative text extraction (if needed)
from twisted.internet.error import DNSLookupError
from twisted.internet.threads import deferToThread
from scrapy.dupefilters import RFPDupeFilter

from greek_scraper.gpu_processor import GPUTextProcessor # Import GPU Processor - ensure correct relative import

class ScraperSpider(scrapy.Spider): # Renamed class to ScraperSpider
    name = "generic_greek_scraper_json_output" # Generic spider name
    target_tlds = [] # Target TLDs will be dynamically set
    custom_settings = {
        # Aggressive global concurrency, but we limit domain seeds to 100 concurrently.
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Allow a few concurrent requests within each domain
        'DOWNLOAD_DELAY': 0.125,
        'HTTPCACHE_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.5,
        'AUTOTHROTTLE_MAX_DELAY': 2.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'LOG_LEVEL': 'ERROR',
        'COOKIES_ENABLED': False,
        'REDIRECT_MAX_TIMES': 2,
        'AJAXCRAWL_ENABLED': False,
        'DEPTH_LIMIT': 10,
        'ROBOTSTXT_OBEY': True,
        'ITEM_PIPELINES': {
            'greek_scraper.pipelines.TextPipeline': 300, # Package aware path
            'greek_scraper.pipelines.StoragePipeline': 400, # Package aware path
        },
        'JOBDIR': None,  # Will be overridden from command-line args.
        'DOWNLOADER_MIDDLEWARES': {
            'greek_scraper.middlewares.RobustEncodingMiddleware': 543, # Package aware path
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'greek_scraper.middlewares.CustomRetryMiddleware': 544, # Package aware path
        }
    }

    def __init__(self, seed_domains=[], autodiscover=False, max_domains=5000, use_cpu=False, output_file='scraped_data_robust.jsonl', target_language=None, **kwargs): # Added target_language
        super().__init__(**kwargs)
        self.autodiscover = autodiscover
        self.max_domains = max_domains
        self.discovered_domains = set()
        self.processed_urls = set()
        self.blocked_domains = set()
        self.pending_domains = list(seed_domains)
        self.active_domains = set()
        self.concurrent_domain_limit = 100
        self.use_cpu = use_cpu
        self.output_file = output_file
        self.target_language = target_language # Store target language

        if self.target_language == 'gr' or self.target_language == 'greek':
            self.target_tlds = ['.gr'] # Set Greek TLDs if language is greek
        else:
            self.target_tlds = [] # Scrape all TLDs if no language specified (generic)

    def start_requests(self):
        # Schedule up to concurrent_domain_limit seed domains.
        count = 0
        while self.pending_domains and count < self.concurrent_domain_limit:
            domain = self.pending_domains.pop(0).strip()
            if domain:
                url = self._normalize_url(domain)
                self.discovered_domains.add(urlparse(url).netloc)
                self.active_domains.add(urlparse(url).netloc)
                yield scrapy.Request(url, callback=self.parse, errback=self.handle_error, dont_filter=True)
                count += 1

    def parse(self, response):
        current_domain = urlparse(response.url).netloc
        item = {'url': response.url, 'text': '', 'links': []}

        # --- Check Content Type ---
        try:
            content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore').lower()
            if not any(x in content_type for x in ['text/html', 'text/plain', 'application/xml', 'application/xhtml+xml']):
                return  # Skip non-text responses
        except Exception:
            return

        # --- Extract Cleaned Text ---
        try:
            extracted_text = extract(response.text) or ""
            item['text'] = unicodedata.normalize('NFKC', extracted_text).strip()
        except Exception:
            item['text'] = ""

        # --- Extract and Process Links ---
        try:
            links = response.css('a::attr(href)').getall()
        except Exception:
            links = []

        for link in links:
            try:
                full_url = response.urljoin(link)
                parsed = urlparse(full_url)
                if parsed.scheme in ['http', 'https'] and parsed.netloc == current_domain:
                    yield scrapy.Request(full_url, callback=self.parse, errback=self.handle_error)
                    item['links'].append(full_url)
            except Exception:
                continue

        print(f"✅ Domain successfully crawled: {current_domain}")
        yield item

    def _normalize_url(self, domain):
        if not domain.startswith("http"):
            return f"https://{domain}"
        return domain

    def handle_error(self, failure):
        request = failure.request
        # You could add more sophisticated error handling and retries here.

    def _is_target_domain(self, domain):
        if self.target_tlds: # Check TLDs only if target_tlds are specified (e.g., for Greek)
            return any(domain.endswith(tld) for tld in self.target_tlds)
        return True # If no target_tlds, then it's a generic scraper, accept all domains

    # --------------- Spider Idle Signal Handler ----------------
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ScraperSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)

        # Pass parameters to pipelines
        settings = crawler.settings
        pipelines = settings.getdict('ITEM_PIPELINES')

        if 'greek_scraper.pipelines.TextPipeline' in pipelines:
            pipelines['greek_scraper.pipelines.TextPipeline'] = cls.create_text_pipeline(spider, settings)
        if 'greek_scraper.pipelines.StoragePipeline' in pipelines:
            pipelines['greek_scraper.pipelines.StoragePipeline'] = cls.create_storage_pipeline(spider, settings)

        return spider

    @classmethod
    def create_text_pipeline(cls, spider, settings):
        return {
            'class': 'greek_scraper.pipelines.TextPipeline',
            'priority': 300,
            'kwargs': {'use_cpu': spider.use_cpu, 'target_language': spider.target_language} # Pass target_language to TextPipeline
        }

    @classmethod
    def create_storage_pipeline(cls, spider, settings):
        return {
            'class': 'greek_scraper.pipelines.StoragePipeline',
            'priority': 400,
            'kwargs': {'jobdir': settings.get('JOBDIR'), 'output_file': spider.output_file}
        }

    def spider_idle(self):
        """
        When the spider is idle, check if there are still seed domains waiting.
        If yes and we are below our concurrent domain limit, schedule a new one and
        prevent the spider from closing.
        """
        if self.pending_domains and len(self.active_domains) < self.concurrent_domain_limit:
            domain = self.pending_domains.pop(0).strip()
            if domain:
                url = self._normalize_url(domain)
                netloc = urlparse(url).netloc
                if netloc not in self.discovered_domains and len(self.discovered_domains) < self.max_domains:
                    self.discovered_domains.add(netloc)
                    self.active_domains.add(netloc)
                    req = scrapy.Request(url, callback=self.parse, errback=self.handle_error)
                    self.crawler.engine.crawl(req, self)
                    raise DontCloseSpider("Scheduling new seed domain")
        # If no pending seed domain, let the spider close normally.