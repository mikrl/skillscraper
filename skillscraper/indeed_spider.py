import logging
import json

import cloudscraper

from skillscraper.scrape_utils import IndeedSite, wait_plus_jitter
class IndeedSpider:
    def __init__(self, job_title, location, max_pages=1, field=None, *args, **kwargs):
        self.indeed = IndeedSite('https://', 'ca.indeed.com')

        
        self.search_url = self.indeed.get_search_url(job_title, location)
        self.listing_urls = set({})
        self.results = []

        self.max_pages = max_pages
        self.on_page = 0


        IOS_FIREFOX = {"browser":"firefox",
                "mobile": False,
                "desktop": True,
                "platform": "windows",
                }

        self.scraper = cloudscraper.create_scraper(browser=IOS_FIREFOX)  # returns a CloudScraper instance

    def crawl(self):
        while self.on_page < self.max_pages:
            self.extract_listings_to_process(self.search_url)
            logging.info(f"Processed listings on page {self.on_page + 1} out of {self.max_pages}")
            self.on_page +=1    
        self.process_listings()

    def extract_listings_to_process(self, url):
        response = self.make_request(url)
        self.extract_listings(response)

    def make_request(self, url):
        response = self.scraper.get(url)
        logging.info(f"HTTP [{response.status_code}] {response.reason} {response.url}")
        wait_plus_jitter(5)
        return response

    def extract_listings(self, response):
        listing_jk = self.indeed.get_listings_from_search_page(response.content)
        self.listing_urls |= {self.indeed.get_job_post_url(jk) for jk in listing_jk}
        self.search_url = self.indeed.next_page       

    def process_listings(self):
        logging.debug(f"Processing the following: {' '.join(self.listing_urls)}")
        for url in self.listing_urls:
            response = self.make_request(url)
            parsed_listing = self.indeed.parse_listing_to_dict(response.content)
            logging.info(f"Extracted {parsed_listing.get('title')} at {parsed_listing.get('company')} at {url}")
            self.results.append({"url": url} | parsed_listing)

    def get_serialized_results(self, *args, **kwargs):
        return json.dumps(self.results, *args, **kwargs)
    
    def save(self, filename):
        results = self.get_serialized_results(indent=4)
        with open(filename, 'w') as result_file:
            result_file.write(results)
        logging.info(f"Wrote results to {filename}")


if __name__ == '__main__':
    job_title = "Software Developer" 
    location = "Waterloo,ON"
    logging.basicConfig(level=logging.INFO)
    spider = IndeedSpider(job_title, location)
    spider.crawl()
    spider.save('./swe_waterloo_poc.json')