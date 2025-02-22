# greek_scraper/middlewares.py
import chardet
from urllib.parse import urlparse
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import DNSLookupError

class RobustEncodingMiddleware:
    def process_response(self, request, response, spider):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore').lower()
        is_text = any(x in content_type for x in ['text/html', 'text/plain', 'application/xml', 'application/xhtml+xml'])
        if is_text:
            if not response.encoding or response.encoding.lower() not in ['utf-8', 'utf8']:
                try:
                    decoded = response.body.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        detected = chardet.detect(response.body)['encoding'] or 'utf-8'
                        decoded = response.body.decode(detected, errors='replace')
                    except Exception as e:
                        return response.replace(body=b'', encoding='utf-8')
                return response.replace(body=decoded.encode('utf-8'), encoding='utf-8')
        return response

class CustomRetryMiddleware:
    def process_spider_exception(self, response, exception, spider):
        req = response.request

        if isinstance(exception, DNSLookupError):
            domain = urlparse(req.url).netloc
            spider.blocked_domains.add(domain)  # Add domain to blocked list
            return  # Do not retry DNS errors, move on to the next request

        # For other exceptions, let Scrapy's default retry mechanism handle them (or your custom retry logic if needed)
        return