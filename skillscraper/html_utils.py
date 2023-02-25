import logging
import re

from bs4 import BeautifulSoup

class IndeedSearchExtractor:

    def __init__(self, raw_html):
        self.parser = BeautifulSoup(raw_html, 'lxml')
        self.url_list = []

    def get_listing_jk(self):
        """
        Grabs the URLs of every job listing shown on a search.
        """
    
        soup = self.parser
        all_links = soup.find_all('a')
        jk_tags  = [link.attrs.get('data-jk') for link in all_links]
        return [jk for jk in jk_tags if jk is not None]

    def get_total_jobs(self):
        total_jobs_tag = re.compile('^(\d*\.?\d+|\d{1,3}(,\d{3})*(\.\d+)?) jobs$')
        soup = self.parser
        total_jobs = soup.find(text = total_jobs_tag).split()[0]
        return total_jobs

    def get_current_page_number(self):
        soup = self.parser
        current_page = soup.find("button", {'data-testid':'pagination-page-current'}).get_text()
        return current_page

    def get_next_page_url(self):
        soup = self.parser
        next_page = soup.find('a', {'aria-label':'Next Page'}).attrs.get('href')

        if next_page is None:
            logging.warning("Failure in get_next_page_url parsing!")

        return next_page
    
class IndeedPostInfoExtractor:

    def __init__(self, raw_html):
        self.parser = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
        self.title = self.get_job_title()
        self.company = self.get_job_company()
        self.content = self.get_job_description()

    def get_job_title(self):
        soup = self.parser
        job_title = soup.find('span', role='text').get_text()

        if job_title is None:
            logging.warning("Failure in get_job_title parsing!")

        return job_title

    def get_job_company(self):
        soup = self.parser
        job_company = soup.find('div', {'data-company-name':'true'}).get_text()

        if job_company is None:
            logging.warning("Failure in get_job_company parsing!")

        return job_company

    def get_job_description(self):
        soup = self.parser
        job_description = soup.find('div', id="jobDescriptionText").get_text()
        
        if job_description is None:
            logging.warning("Failure in get_job_description parsing!")
        
        return job_description

    def get_listing_dict(self) -> dict[str, str]:
        """ 
        Turns listing HTML into a dictionary representation of the listing,
        with the job title, company and job description.
        """
        return {"title": self.title,
                "company": self.company,
                "content": self.content}
