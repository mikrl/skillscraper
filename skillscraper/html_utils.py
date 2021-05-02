from bs4 import BeautifulSoup

import re
import string

class IndeedSearchExtractor:

    def listing_urls(self, raw_html):
        """
        Grabs the URLs of every job listing shown on a search.
        """
        self.url_list = []
    
        soup = BeautifulSoup(raw_html, 'html.parser')
        listings = soup.findAll("div", {"data-tn-component":"organicJob"})

        for listing in listings:
            jk = listing["data-jk"]
            listing_url = "https://ca.indeed.com/viewjob?jk={}".format(jk)
            self.url_list.append(listing_url)
        
        return self.url_list

    def get_result_count(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_count = soup.find("div", {"id":"searchCountPages"}).contents[0].split()
        if not (result_count[0] == 'Page' and
                result_count[1].isnumeric() and
                result_count[2] == 'of' and
                result_count[3].isnumeric() and
                result_count[4] == 'jobs'):                
            raise NotImplementedError("Format of result count changed. \
            Cannot parse total number of search results.")

        self.result_count = int(result_count[2].replace(",",""))
        return self.result_count
    
class IndeedPostInfoExtractor:

    def get_job_title(self, raw_html):
        soup = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
        job_title = soup.find(["h1", "h2", "h3"], {"class":re.compile("JobInfoHeader-title")}).get_text()
        job_title_clean = job_title.translate(str.maketrans('', '', string.punctuation))
        return job_title_clean

    def get_job_company(self, raw_html):
        soup = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
        job_company = soup.find("div", {"class":re.compile("icl-u-lg-mr")}).get_text()
        job_company_clean = job_company.translate(str.maketrans('', '', string.punctuation))
        return job_company_clean

    def get_job_description(self, raw_html):
        soup = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
        job_description_div = soup.find("div", {"class":re.compile("JobComponent-description")})
        job_description = " ".join([par.text for par in job_description_div.findAll('p')])
        job_description_clean = job_description.translate(str.maketrans('', '', string.punctuation))
        return job_description_clean

    def parse_html(self, raw_html:str) -> dict[str, str]:
        """ 
        Turns listing HTML into a dictionary representation of the listing,
        with the job title, company and job description.
        """
        return {"title": self.get_job_title(raw_html),
                "company": self.get_job_company(raw_html),
                "content": self.get_job_description(raw_html)}
