import logging

import cloudscraper

from scrape_utils import IndeedSite, wait_plus_jitter
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
            logging.info(f"Processed listings on page {self.on_page} out of {self.max_pages}")
            self.on_page +=1    
        self.process_listings()

    def extract_listings_to_process(self, search_url):
        response = self.make_request(self.search_url)
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
            self.results.append(parsed_listing)




if __name__ == '__main__':
    job_title = "Software Developer" 
    location = "Waterloo,ON"
    logging.basicConfig(level=logging.INFO)
    spider = IndeedSpider(job_title, location)
    spider.crawl()
    for result in spider.results:
        print(result)
