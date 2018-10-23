import urllib.request
import sqlite3
from bs4 import BeautifulSoup
import hashlib
from nltk.util import everygrams
import re
import time
from random import random

REQUEST_DELAY = 1.0 #request delay in seconds
SEARCH_PARAMS = {"and":"analyst", #matches ANDed results
                 "phr":"", #matches exact phrase
                 "any":"", #matches ORed results
                 "not":"", #matches NOT results
                 "ttl":"", #matches in title
                 "cmp":"", #matches company
                 "jt":"all",  #job type (part time etc), default is all
                 "st":"",  #job source
                 "sal":"", #salary est
                 "rad":"15", #radius of x kilometers
                 "loc":"Waterloo%2C+ON", #from location
                 "age":"any", #15, 7, 3, any are most useful
                 "lim":"50", #50 is max
                 "sort":"date"} #default is sort="" for relevance sort
                 
            

def politelyWait():
    time.sleep(random()*REQUEST_DELAY)

#################################################
# Following function generates the URL to       #
# search jobs. Advanced search template is used #
# Search paramaters are set above               #
#################################################
def constructSearchURL():
    as_and=SEARCH_PARAMS["and"]
    as_phr=SEARCH_PARAMS["phr"]
    as_any=SEARCH_PARAMS["any"]
    as_not=SEARCH_PARAMS["not"]
    as_ttl=SEARCH_PARAMS["ttl"]
    as_cmp=SEARCH_PARAMS["cmp"]
    jt=SEARCH_PARAMS["jt"]
    st=SEARCH_PARAMS["st"]
    salary=SEARCH_PARAMS["sal"]
    radius=SEARCH_PARAMS["rad"]
    l=SEARCH_PARAMS["loc"]
    fromage=SEARCH_PARAMS["age"]
    limit=SEARCH_PARAMS["lim"]
    sort=SEARCH_PARAMS["sort"]
    
    url = ("https://www.indeed.ca/jobs?"
           "as_and={0}&"
           "as_phr={1}&"
           "as_any={2}&"
           "as_not={3}&"
           "as_ttl={4}&"
           "as_cmp={5}&"
           "jt=all{6}&"
           "st={7}&"
           "salary={8}&"
           "radius={9}&"
           "l={10}&"
           "fromage={11}&"
           "limit={12}&"
           "sort={13}&"
           "psf=advsrch&"
           "filter=0").format(as_and, as_phr, as_any, as_not, as_ttl, as_cmp, jt, st, salary, radius, l, fromage, limit, sort)
    
    return url


    
#################################################
# Following function grabs the URLs of the job  #
# listings and adds them to a queue             #
# Duplicates are not permitted                  #
#################################################
def grabListings(raw_html):

    url_list=[]
    
    soup = BeautifulSoup(raw_html, 'html.parser')
    listings = soup.findAll("div", {"data-tn-component":"organicJob"})

    for listing in listings: url_list.append(listing["data-jk"])
    
    return url_list

def getResultCount(raw_html):

    soup = BeautifulSoup(raw_html, 'html.parser')

    result_count = soup.find("div", {"id":"searchCount"}).contents[0].split()[-1]

    return(int(result_count.replace(",","")))

def getRawHTML(url):

    req = urllib.request.Request(url, headers={'User-Agent':'Googlebot'})
    with urllib.request.urlopen(req) as response:
        raw_html=response.read()#.decode('utf-8')

    return raw_html

### Data cleaning ###
# Turns raw HTML code from indeed into a simple job listing
# in the form
#   ['search term', 'title', 'company', 'listing text', 'listing hash']
# for exportation to a database
#################

def parseAd(raw_html):

    soup = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
    
    job_title = soup.find("h3", {"class":re.compile("JobInfoHeader-title")}).get_text()
    job_company = soup.find("div", {"class":re.compile("icl-u-lg-mr")}).get_text() 
    job_summary = soup.find("div", {"class":re.compile("JobComponent-description")}).get_text()

    #print(job_title, job_company, job_summary)
    return [SEARCH_PARAMS["and"], job_title, job_company, job_summary]

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
    
    init_search = constructSearchURL()
    url_list = []
    num_pages = 0
    
    monograms = []
    bigrams = []
    trigrams = []

    search_html=getRawHTML(init_search)

    url_list = grabListings(search_html)
    num_results =  getResultCount(search_html)
    
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

    print(len(monograms), len(bigrams), len(trigrams), len(quadgrams))

    #  input()
    getTopItems(monograms)
    #input()
    getTopItems(bigrams)
    #input()
    getTopItems(trigrams)
    #input()
    getTopItems(quadgrams)
    
    """
    input()
    print(monograms)
    input()
    print(bigrams)
    input()
    print(trigrams)
    input()
    print(quadgrams)
    """
    """
    for url in set(url_list):
        print("https://www.indeed.ca/viewjob?jk={0}".format(url))
    """

################################################################################
#breakpoint()
main()

"""
tdict = {'a':5, 'b':3}
testlst = ['a', 'b', 'c']

print(tdict)
tdict = aggregate(testlst, tdict)
print(tdict)
print(aggregate(testlst,tdict))
"""
