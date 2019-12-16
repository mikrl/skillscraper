import time
from random import random

class JobSearch:
    
    _request_delay = 1.0 #request delay in seconds
    _search_params = {"and":"analyst", #matches ANDed results
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

    def delay():
        time.sleep(random()*_request_delay)

    #################################################
    # Following function generates the URL to       #
    # search jobs. Advanced search template is used #
    # Search paramaters are set above               #
    #################################################
    def constructSearchURL_():
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
               "filter=0").format(as_and, as_phr, as_any, as_not, as_ttl, as_cmp,
                                  jt, st, salary, radius, l, fromage, limit, sort)
        return url
