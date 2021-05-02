from .aggregate import Aggregator
from .html_utils import IndeedPostInfoExtractor, IndeedURLExtractor
from .search import IndeedSearch


import sqlite3
import hashlib
from nltk.util import everygrams
import re
import time
from random import random

REQUEST_DELAY = 1.0 #request delay in seconds

def politelyWait():
    time.sleep(random()*REQUEST_DELAY)


# Following function cleans the job  post       #
# for n-gram analysis                           #

def cleanText(inp_string):

    round1 = re.sub(r'[^a-zA-Z0-9\n\\]', " ", inp_string) #removes non alphanumeric chars
    round2 = round1.lower() #sends text to lowercase
    round3 =round2 #= re.sub(r'\\x..', "", round2) #removes pesky byte encodings #testing without removing the encodings
    round4 = re.sub(r'\n', " ", round3) #removes pesky leftover newlines
    round5 = re.sub(r'[ ]{2,}', " ", round4)#replaces multiple spaces with one space

    out_string = round5
    #breakpoint()
    
    return out_string
#################
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

    search = IndeedSearch()
    waterloo_search = {"and": "software+engineer",
                       "jt": "all",
                       "rad": "15",
                       "loc": "Waterloo%2C+ON",
                       "age": "any",
                       "lim": "50",
                       "sort": "date"}

    search_html = search.get_search_html(waterloo_search)
    
    url_list = IndeedURLExtractor.listing_urls(search_html)
    num_results =  IndeedURLExtractor.get_result_count(search_html)
    
    monograms = []
    bigrams = []
    trigrams = []
    
    if num_results>1000:
        
        print("[*]{0} results found, searching first 1000".format(num_results))
        num_results=951

    else:
        
        print("[*]{0} results found".format(num_results))

    for itr, result in enumerate(range(50, num_results, 50)):

        print("[*]Grabbing results {0} through {1}".format(result, result+50))
        if itr !=0: politelyWait()
        search_html = getRawHTML(init_search+"&start={0}".format(result))
        url_list+= grabListings(search_html)
    
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
