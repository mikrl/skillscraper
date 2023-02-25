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

    def get_next_page(self):
        total_jobs_tag = re.compile('^(\d*\.?\d+|\d{1,3}(,\d{3})*(\.\d+)?) jobs$')
        soup = self.parser
        soup.find(text = total_jobs_tag)


    def get_result_count(self):
        soup = self.parser
        result_count = soup.find("div", {"id":"searchCountPages"}).contents[0].split()
        if not (result_count[0] == 'Page' and
                result_count[1].isnumeric() and
                result_count[2] == 'of' and
                result_count[3].isnumeric() and
                result_count[4] == 'jobs'):                
            raise NotImplementedError("Format of result count changed. \
            Cannot parse total number of search results.")

        self.result_count = int(result_count[3].replace(",",""))
        return self.result_count
    
class IndeedPostInfoExtractor:

    def __init__(self, raw_html):
        self.parser = BeautifulSoup(raw_html, 'lxml', from_encoding='utf-8')
        self.title = self.get_job_title()
        self.company = self.get_job_company()
        self.content = self.get_job_description()

    def get_job_title(self):
        soup = self.parser
        job_title = soup.find('span', role='text').get_text()
        return job_title

    def get_job_company(self):
        soup = self.parser
        job_company = soup.find('div', {'data-company-name':'true'}).get_text()
        return job_company

    def get_job_description(self):
        soup = self.parser
        job_description = soup.find('div', id="jobDescriptionText").get_text()
        return job_description

    def get_listing_dict(self) -> dict[str, str]:
        """ 
        Turns listing HTML into a dictionary representation of the listing,
        with the job title, company and job description.
        """
        return {"title": self.title,
                "company": self.company,
                "content": self.content}
