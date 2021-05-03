#from .aggregate import Aggregator
from listing import IndeedListing
from html_utils import IndeedPostInfoExtractor, IndeedSearchExtractor
from search import IndeedSearch


import sqlite3
import hashlib
from nltk.util import everygrams
import re
import time
from random import random

REQUEST_DELAY = 1.0 #request delay in seconds

def politelyWait():
    time.sleep(random()*REQUEST_DELAY)


def aggregate(inp_str, inp_dict):

    outp_dict = inp_dict
    
    if inp_str in inp_dict:
        
        outp_dict[inp_str]+=1

    else:
        
        outp_dict[inp_str]=1

    return outp_dict

def getTopItems(inp_dict, topN=20): #given input dict, return list of top N items (default 20)
    outp_list=sorted(inp_dict, key=inp_dict.get  , reverse=True)
    for i in range(topN):
        print(outp_list[i], inp_dict[outp_list[i]])
        
    return outp_list[:topN]

def main():
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
    breakpoint()
    url_batch_size = len(url_list)
    if url_batch_size != results_per_page:
        print("[!] {0} URLs retrieved but lim={1}".format(url_batch_size, results_per_page))
        results_per_page = url_batch_size

    print("[*]{0} results reported. Searched the first {1}".format(num_results, url_batch_size))

    listings_serial = []
    for listing_url in url_list:
        politelyWait()
        listing_html = IndeedListing().get_listing_html(listing_url)
        listing_dict = IndeedPostInfoExtractor().parse_html(listing_html)
        
        listings_serial.append({'url':listing_url, 'data':listing_dict})
        # cache it here
    breakpoint()
    # # Disable repetition logic for now. Search first page only
    # if num_results>1000:
    #     print("[*]{0} results found, searching first 1000".format(num_results))
    #     num_results=951

    # else:
        
    #     print("[*]{0} results found".format(num_results))

    # for itr, result in enumerate(range(50, num_results, 50)):

    #     print("[*]Grabbing results {0} through {1}".format(result, result+50))
    #     if itr !=0: politelyWait()
    #     search_html = getRawHTML(init_search+"&start={0}".format(result))
    #     url_list+= grabListings(search_html)
    
    total_links = len(url_list)
    url_list = set(url_list)
    unique_links = len(url_list)
    discarded_links = total_links-unique_links
    
    listing_hashes = []
    duplicates = 0
    
    monograms = {}
    bigrams = {}
    trigrams = {}
    quadgrams = {}

    print("[*]{0} overlapping search results found and discarded".format(discarded_links))
    
    # Code for setting up SQLite database
    #database = sqlite3.connect('../data/results.db')
    database = sqlite3.connect(':memory:')
    db = database.cursor()
    db.execute('''CREATE TABLE raw_listings (title TEXT, company TEXT, listing TEXT, lhash BLOB)''')
    print("[*] Database created ")
    breakpoint()
    for idx, url in enumerate(url_list):

        if idx !=0: politelyWait()
        listing_html = getRawHTML("https://www.indeed.ca/viewjob?jk={0}".format(url))

        if idx%20 == 0:
            print("[*]Processing listing {0} of {1}".format(idx+1, unique_links))
    
        ad_datum = parseAd(listing_html) #store this to a database
        #print(ad_datum)
        
        cleaned_text = cleanText(ad_datum[3])
        #breakpoint()
        listing_hash = hashlib.md5(cleaned_text.encode('utf-8')).hexdigest()

        if listing_hash not in listing_hashes:

            listing_hashes.append(listing_hash)
        
            ngrams = everygrams(cleaned_text.split(), max_len=4)

            for el in ngrams:

                ngram = " ".join(el)
                
                if len(el)==1:
                    monograms = aggregate(ngram, monograms)
                    
                elif len(el)==2:
                    bigrams = aggregate(ngram, bigrams)
                    
                elif len(el)==3:
                    trigrams = aggregate(ngram, trigrams)

                elif len(el)==4:
                    quadgrams = aggregate(ngram, quadgrams)
        else:
            
            duplicates+=1
            continue

        
    plural = lambda p: "" if duplicates==1 else "s"

    print("[*]Processed {0} listings".format(unique_links))
    print("[*]{0} duplicate{1} found and ignored".format(duplicates, plural(duplicates)))

    getTopItems(monograms)
    getTopItems(bigrams)
    getTopItems(trigrams)
    getTopItems(quadgrams)
    
    print(monograms, '/n',
          bigrams, '/n',
          trigrams, '/n',
          quadgrams)
    """
    for url in set(url_list):
        print("https://www.indeed.ca/viewjob?jk={0}".format(url))
    """


main()
