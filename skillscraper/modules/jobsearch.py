import time
from random import random

class JobSearcher:
    userAg_ = 'Googlebot' #change ASAP
    
    request_delay_ = 1.0 #request delay in seconds
    search_params_ = {"and":"analyst", #matches ANDed results
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

    def delay_():
        """Causes the searcher to sleep for a noisy period of time"""
        time.sleep(random()*_request_delay)


    def constructSearchURL_():
        """From the search terms supplied to the searcher, return advanced search URL"""
        as_and=_search_params["and"]
        as_phr=_search_params["phr"]
        as_any=_search_params["any"]
        as_not=_search_params["not"]
        as_ttl=_search_params["ttl"]
        as_cmp=_search_params["cmp"]
        jt=_search_params["jt"]
        st=_search_params["st"]
        salary=_search_params["sal"]
        radius=_search_params["rad"]
        l=_search_params["loc"]
        fromage=_search_params["age"]
        limit=_search_params["lim"]
        sort=_search_params["sort"]
        
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
               "filter=0").format(as_and, as_phr,
                                  as_any, as_not,
                                  as_ttl, as_cmp,
                                  jt, st, salary,
                                  radius, l, fromage,
                                  limit, sort)
        return url


    def parseListingURL(raw_html):
        """From raw html,  return URLs of job listings"""
        
        soup = BeautifulSoup(raw_html, 'html.parser')
        url_list = [link["data-jk"] for link in soup.findAll("div", {"data-tn-component":"organicJob"})] 

        return url_list
   

    def resultCount_(raw_html):
        """From raw html, returns the number of listings as noted by the search bar """

        soup = BeautifulSoup(raw_html, 'html.parser')
        result_count = soup.find("div", {"id":"searchCount"}).contents[0].split()[-1]
        result_toi = int(result_count.replace(",","")) # need to transform input from "1,000" to 1000

        return result_toi


    def requestHTML_(url):
        """Wrapper for web request, returns html of the response"""
        req = urllib.request.Request(url, headers={'User-Agent': userAg_})
        with urllib.request.urlopen(req) as response:
            raw_html=response.read()#.decode('utf-8')

        return raw_html


    """
    Need methods that compose the above to return a 
    list of listing URLS
    
    """
##################################################################################
    #TODO: organize anything below here

    ### Data cleaning ###
    # Turns raw HTML code from indeed into a simple job listing
    # in the form
    #   ['search term', 'title', 'company', 'listing text', 'listing hash']
    # for exportation to a database
    #################
class JobParser:
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
        round3 =round2 #= re.sub(r'\\x..', "", round2) #removes byte encodings #testing without removing the encodings
        round4 = re.sub(r'\n', " ", round3) #removes pesky leftover newlines
        round5 = re.sub(r'[ ]{2,}', " ", round4)#replaces multiple spaces with one space

        out_string = round5
        #breakpoint()
    
        return out_string


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
