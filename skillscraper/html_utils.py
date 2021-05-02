from bs4 import BeautifulSoup

import re


class IndeedURLExtractor:

    def listing_urls(raw_html):
        """
        Grabs the URLs of every job listing shown on a search.
        """
        url_list = []
    
        soup = BeautifulSoup(raw_html, 'html.parser')
        listings = soup.findAll("div", {"data-tn-component":"organicJob"})


        for listing in listings:
            jk = listing["data-jk"]
            listing_url = "https://ca.indeed.com/viewjob?jk={}".format(jk)
            url_list.append(listing_url)
        
        return url_list

    def get_result_count(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_count = soup.find("div", {"id":"searchCount"}).contents[0].split()[-1]
        return(int(result_count.replace(",","")))
    
class IndeedPostInfoExtractor:
    
    def parsed_ad(raw_html):
        """ 
        Turns listing HTML into a dictionary representation of the listing,
        with the job title, company and job description.
        """
        soup = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')

        job_title = soup.find("h3", {"class":re.compile("JobInfoHeader-title")}).get_text()
        job_company = soup.find("div", {"class":re.compile("icl-u-lg-mr")}).get_text() 
        job_description = soup.find("div", {"class":re.compile("JobComponent-description")}).get_text()

        return {"title": job_title,
                "company": job_company,
                "content": job_description}
