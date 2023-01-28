import time
from random import random
import logging

import sqlite3

from aggregator import map_ngrams, reduce_ngrams
from listing import IndeedListing
from html_utils import IndeedPostInfoExtractor, IndeedSearchExtractor
from search import IndeedSearch
from storage import ListingCache, Caches

CACHE_LISTINGS = True
CACHE_NGRAMS = True
PROCESS_SERIAL = True
PROCESS_ASYNC = not PROCESS_SERIAL

REQUEST_DELAY = 1.0 #request delay in seconds
LOGGER = logging.getLogger("main")

def politely_wait():
    time.sleep(random()*REQUEST_DELAY)


def getTopItems(inp_dict, topN=20): #given input dict, return list of top N items (default 20)
    outp_list=sorted(inp_dict, key=inp_dict.get  , reverse=True)
    for i in range(topN):
        print(outp_list[i], inp_dict[outp_list[i]])
        
    return outp_list[:topN]

def main():
    breakpoint()
    print("[*]Initializing search")

    results_per_page = 15
    
    search = IndeedSearch()
    waterloo_search = {"and": "software+engineer",
                       "jt": "all",
                       "rad": "15",
                       "loc": "Waterloo%2C+ON",
                       "age": "any",
                       "lim": str(results_per_page),
                       "sort": "date"}

    first_page_search_html = search.get_search_html(waterloo_search)    
    url_list = IndeedSearchExtractor().get_listing_urls(raw_html=first_page_search_html)
    num_results = IndeedSearchExtractor().get_result_count(raw_html=first_page_search_html)


    if CACHE_LISTINGS:
        listing_cache = ListingCache()
        cached = [listing_cache.cache_listing(listing_url)
                  for listing_url in url_list]
        unique_listings = [cached_url[0] for cached_url in zip(url_list, cached) if cached_url[1]]
    
        if len(cached) > len(unique_listings):
            LOGGER.info("Ignored %s cached listings." % len(cached) - len(unique_listings))

        url_list = unique_listings

    breakpoint()
    url_batch_size = len(url_list)
    if url_batch_size != results_per_page:
        LOGGER.warning("{0} URLs retrieved but lim={1}.".format(url_batch_size,
                                                             results_per_page))
        LOGGER.info("Reducing results_per_page to {0} from {1}".format(url_batch_size,
                                                                       results_per_page))
        results_per_page = url_batch_size
    # Only search the first page for now
    print("[*]{0} results reported. Searched the first {1}".format(num_results, url_batch_size))

    if PROCESS_SERIAL:
        listings_serial = []
        for listing_url in url_list:
            politely_wait()
            listing_html = IndeedListing().get_listing_html(listing_url)
            listing_dict = IndeedPostInfoExtractor().parse_html(listing_html)
        
            listings_serial.append({'url':listing_url, 'data':listing_dict})

            
        if CACHE_NGRAMS:
            # cache it here
            pass
        ngram_dict = {}
        for listing_text in listings_serial:
            listing_1grams = map_ngrams(listing_text)
            ngram_dict.update(reduce_ngrams(listing_1grams))

    elif PROCESS_ASYNC:
        pass
    

    breakpoint()

    # Code for setting up SQLite database
    #database = sqlite3.connect('../data/results.db')
    database = sqlite3.connect(':memory:')
    db = database.cursor()
    db.execute('''CREATE TABLE raw_listings (title TEXT, company TEXT, listing TEXT, lhash BLOB)''')
    print("[*] Database created ")
    breakpoint()


if __name__ == "__main__":
    main()
