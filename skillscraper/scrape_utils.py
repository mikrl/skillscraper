import logging
import urllib.parse
import random
import time

from skillscraper.html_utils import IndeedSearchExtractor, IndeedPostInfoExtractor

def wait_plus_jitter(t):
    jitter = random.gauss()
    time.sleep(t+jitter)
    return t+jitter

class IndeedSite:
    
    def __init__(self, scheme, domain):
        self.scheme = scheme
        self.domain=domain
        self.next_page = 1

    def url_formatter(self, url):
        url = urllib.parse.quote(url, safe='=?&/:')
        url = url.replace(' ', '+')
        return url

    def get_search_url(self, job_title, location):
        search_url = f"{self.scheme}{self.domain}/jobs?q={job_title}&l={location}"
        return self.url_formatter(search_url)

    def get_job_post_url(self, job_key):
        # Will look something like jk=d4fb8e699210c7df
        job_post_url = f"{self.scheme}{self.domain}/viewjob?jk={job_key}"
        return self.url_formatter(job_post_url)
    
    def get_listings_from_search_page(self, raw_html):
        search_parser = IndeedSearchExtractor(raw_html)
        parsed = search_parser.get_listing_jk()
        logging.debug(f"Extracted these job keys: {' '.join(parsed)}")
        next_page_path = search_parser.get_next_page_url()
        self.next_page = f"{self.scheme}{self.domain}{next_page_path}"
        logging.info(f"Completed listing extraction and set next page to {self.next_page}")
        return parsed
    
    def parse_listing_to_dict(self, raw_html):
        listing_parser = IndeedPostInfoExtractor(raw_html)
        parsed = listing_parser.get_listing_dict() 
        logging.debug(f"Parsed job {parsed}")
        return parsed