import logging
import random
import time

import cloudscraper

from html_utils import IndeedPostInfoExtractor, IndeedSearchExtractor
from scrape_utils import IndeedSite, debug_requests


def wait_plus_jitter(t):
    jitter = random.gauss()
    time.sleep(t+jitter)
    return t+jitter

class SimpleSpider:
    def __init__(self, job_title, location, field=None, *args, **kwargs):
        self.indeed = IndeedSite('https://', 'ca.indeed.com')

        
        self.search_url = self.indeed.get_search_url(job_title, location)
        self.listing_urls = set({})
        self.results = []

        self.max_pages = 1
        self.on_page = 0


        IOS_FIREFOX = {"browser":"firefox",
                "mobile": False,
                "desktop": True,
                "platform": "windows",
                }

        self.scraper = cloudscraper.create_scraper(browser=IOS_FIREFOX)  # returns a CloudScraper instance

    def crawl(self):
        while self.on_page < self.max_pages:
            response = self.make_request(self.search_url)
            self.extract_listings(response)
            self.on_page +=1    
        
        self.process_listings()

    def make_request(self, url):
        with debug_requests(logging.INFO):
            response = self.scraper.get(url)
        wait_plus_jitter(5)
        return response

    def extract_listings(self, response):
        search_parser = IndeedSearchExtractor(response.content)
        listing_jk =  search_parser.get_listing_jk()
        self.listing_urls |= {self.indeed.get_job_post_url(jk) for jk in listing_jk}
        self.search_url = search_parser.get_next_page()        

    def process_listings(self):
        for url in self.listing_urls:
            response = self.make_request(url)
            listing_parser = IndeedPostInfoExtractor(response.content)
            parsed_listing = listing_parser.get_listing_dict()
            print(parsed_listing)
            self.results.append(parsed_listing)



if __name__ == '__main__':
    job_title = "Software Developer" 
    location = "Waterloo,ON"
    
    spider = SimpleSpider(job_title, location)
    spider.crawl()
    for result in spider.results:
        print(result)
