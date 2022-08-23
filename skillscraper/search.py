from typing import Dict
import uuid
import logging
import requests
import urllib


class IndeedSearch:
    def __init__(self):
        self._search_params = {
            "and": "",  # matches ANDed results
            "phr": "",  # matches exact phrase
            "any": "",  # matches ORed results
            "not": "",  # matches NOT results
            "ttl": "",  # matches in title
            "cmp": "",  # matches company
            "jt": "",  # job type (part time etc), default is all
            "st": "",  # job source
            "sal": "",  # salary est
            "rad": "",  # radius of x kilometers
            "loc": "",  # from location
            "age": "",  # 15, 7, 3, any are most useful
            "lim": "",  # 50 is max
            "sort": "",
        }  # default is sort="" for relevance sort

    def do_search2022(self, title, loc):
        resource = "https://ca.indeed.com/jobs"
        url = f"{resource}?q={title}&l={loc}"
        logging.Logger("GET {url}")
        response = requests.get(url)
        return response

    @property
    def search_url(self) -> str:
        """
        Generates the url used to search for a job.

        Uses the advanced search and populates the parameters with saved
        values.
        """

        as_and = self._search_params["and"]
        as_phr = self._search_params["phr"]
        as_any = self._search_params["any"]
        as_not = self._search_params["not"]
        as_ttl = self._search_params["ttl"]
        as_cmp = self._search_params["cmp"]
        jt = self._search_params["jt"]
        st = self._search_params["st"]
        salary = self._search_params["sal"]
        radius = self._search_params["rad"]
        l = self._search_params["loc"]
        fromage = self._search_params["age"]
        limit = self._search_params["lim"]
        sort = self._search_params["sort"]

        url = (
            "https://www.indeed.ca/jobs?"
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
            "filter=0"
        ).format(
            as_and,
            as_phr,
            as_any,
            as_not,
            as_ttl,
            as_cmp,
            jt,
            st,
            salary,
            radius,
            l,
            fromage,
            limit,
            sort,
        )

        return url

    def get_search_url(self, search_dict: Dict[str, str]) -> str:
        self._search_params.update(search_dict)
        return self.search_url

    def get_search_html(self, search_dict: Dict[str, str]) -> str:
        search_url = self.get_search_url(search_dict)
        user_agent = str(uuid.uuid4())
        req = urllib.request.Request(search_url, headers={"User-Agent": user_agent})

        with urllib.request.urlopen(req) as response:
            raw_html = response.read()  # .decode('utf-8')

        return raw_html
